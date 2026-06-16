import { useRef, useMemo, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { RigidBody, RapierRigidBody, useRapier, type CollisionPayload } from '@react-three/rapier';
import * as THREE from 'three';
import { useStore } from './store';

// Scratch variables for optimization
const _v1 = new THREE.Vector3();
const _v2 = new THREE.Vector3();
const _v3 = new THREE.Vector3();
const _v4 = new THREE.Vector3();
const _q1 = new THREE.Quaternion();

export function Car() {
  const carRef = useRef<RapierRigidBody>(null);
  const { rapier, world } = useRapier();
  const setSurface = useStore((state) => state.setSurface);
  const surface = useStore((state) => state.surface);
  const isCrashed = useStore((state) => state.isCrashed);
  const setIsCrashed = useStore((state) => state.setIsCrashed);
  
  const forward = useStore((state) => state.forward);
  const backward = useStore((state) => state.backward);
  const left = useStore((state) => state.left);
  const right = useStore((state) => state.right);
  const cameraMode = useStore((state) => state.cameraMode);
  const reset = useStore((state) => state.reset);

  useEffect(() => {
    if (carRef.current) {
      carRef.current.setTranslation({ x: 0, y: 2, z: 0 }, true);
      carRef.current.setRotation({ x: 0, y: 0, z: 0, w: 1 }, true);
      carRef.current.setLinvel({ x: 0, y: 0, z: 0 }, true);
      carRef.current.setAngvel({ x: 0, y: 0, z: 0 }, true);
      setIsCrashed(false);
    }
  }, [reset, setIsCrashed]);

  // Physics constants
  const ACCEL_FORCE = 20;
  const OFFROAD_MULT = 0.4;
  const RUMBLE_MULT = 0.8;
  const TURN_SPEED = 3.0;
  const MAX_SPEED = 35;

  const smoothedCameraPosition = useMemo(() => new THREE.Vector3(), []);
  const smoothedCameraTarget = useMemo(() => new THREE.Vector3(), []);

  const onCollisionEnter = (payload: CollisionPayload) => {
    const other = payload.other.collider.parent();
    const userData = (other as any)?.userData as { type?: string };
    
    if (userData?.type === 'barrier') {
      setIsCrashed(true);
      // Optional: Add a small bounce or screen shake trigger here
      setTimeout(() => setIsCrashed(false), 1000); // Crash lasts 1 second
    }
  };

  useFrame((state) => {
    if (!carRef.current) return;

    const velocity = carRef.current.linvel();
    const rotation = carRef.current.rotation();
    const position = carRef.current.translation();
    
    _q1.set(rotation.x, rotation.y, rotation.z, rotation.w);
    const forwardVec = _v1.set(0, 0, 1).applyQuaternion(_q1);

    // 1. Ground Surface Detection (Raycast down)
    const rayOrigin = { x: position.x, y: position.y, z: position.z };
    const rayDir = { x: 0, y: -1, z: 0 };
    const ray = new rapier.Ray(rayOrigin, rayDir);
    const hit = world.castRay(ray, 2, true);
    
    let currentSurface = 'offroad';
    if (hit) {
      const parent = hit.collider.parent();
      if (parent) {
        const userData = (parent as any).userData as { type?: string };
        // Only update surface if it's a ground type
        if (userData?.type && userData.type !== 'barrier') {
          currentSurface = userData.type;
        }
      }
    }
    if (currentSurface !== surface) setSurface(currentSurface);
    
    // 2. Movement Logic
    let multiplier = isCrashed ? 0.2 : 1.0; // Significant penalty when crashed
    if (currentSurface === 'offroad') multiplier *= OFFROAD_MULT;
    if (currentSurface === 'rumble') multiplier *= RUMBLE_MULT;
    
    const speed = _v2.set(velocity.x, velocity.y, velocity.z).length();
    
    if (forward && speed < MAX_SPEED) {
      carRef.current.applyImpulse(_v3.copy(forwardVec).multiplyScalar(ACCEL_FORCE * multiplier), true);
    }
    if (backward) {
      // Allow reverse or braking
      carRef.current.applyImpulse(_v3.copy(forwardVec).multiplyScalar(-ACCEL_FORCE * 0.6 * multiplier), true);
    }

    // Steering - allow turning even at low speed for recovery
    const turnMultiplier = Math.max(0.3, Math.min(speed / 5, 1));
    if (left) {
      carRef.current.applyTorqueImpulse({ x: 0, y: TURN_SPEED * turnMultiplier * multiplier, z: 0 }, true);
    }
    if (right) {
      carRef.current.applyTorqueImpulse({ x: 0, y: -TURN_SPEED * turnMultiplier * multiplier, z: 0 }, true);
    }

    // Dampen angular velocity to prevent spinning out too easily
    const angVel = carRef.current.angvel();
    carRef.current.setAngvel({ x: angVel.x * 0.95, y: angVel.y * 0.95, z: angVel.z * 0.95 }, true);

    // 3. Camera Logic
    const carPos = _v2.set(position.x, position.y, position.z);
    
    let targetCameraPos = _v3; // Reuse _v3 for target position
    let targetLookAt = _v4; // Use _v4 for target lookAt

    if (cameraMode === 'chase') {
      const offset = _v1.copy(forwardVec).multiplyScalar(-12).add(_v3.set(0, 5, 0)); 
      targetCameraPos.copy(carPos).add(offset);
      targetLookAt.copy(carPos).add(_v1.copy(forwardVec).multiplyScalar(5));
    } else if (cameraMode === 'firstPerson') {
      const offset = _v1.copy(forwardVec).multiplyScalar(0.5).add(_v3.set(0, 0.8, 0.5));
      targetCameraPos.copy(carPos).add(offset);
      targetLookAt.copy(carPos).add(_v1.copy(forwardVec).multiplyScalar(10));
    } else if (cameraMode === 'topDown') {
      targetCameraPos.set(carPos.x, carPos.y + 40, carPos.z);
      targetLookAt.copy(carPos);
    }

    smoothedCameraPosition.lerp(targetCameraPos, 0.1);
    smoothedCameraTarget.lerp(targetLookAt, 0.1);

    state.camera.position.copy(smoothedCameraPosition);
    state.camera.lookAt(smoothedCameraTarget);
  });

  return (
    <RigidBody
      ref={carRef}
      colliders="cuboid"
      mass={1}
      position={[0, 2, 0]}
      angularDamping={0.6}
      linearDamping={0.6}
      onCollisionEnter={onCollisionEnter}
    >
      <mesh castShadow>
        <boxGeometry args={[2, 1, 4]} />
        <meshStandardMaterial color={isCrashed ? "orange" : "red"} />
      </mesh>
      {/* Front lights / visual indicator */}
      <mesh position={[0, 0.2, 2.1]}>
        <boxGeometry args={[1.8, 0.3, 0.2]} />
        <meshStandardMaterial color="white" emissive="white" emissiveIntensity={isCrashed ? 2 : 0.5} />
      </mesh>
      {/* Wheels */}
      <mesh position={[0, -0.3, 1.5]} castShadow>
        <boxGeometry args={[2.2, 0.5, 0.5]} />
        <meshStandardMaterial color="black" />
      </mesh>
      <mesh position={[0, -0.3, -1.5]} castShadow>
        <boxGeometry args={[2.2, 0.5, 0.5]} />
        <meshStandardMaterial color="black" />
      </mesh>
    </RigidBody>
  );
}
