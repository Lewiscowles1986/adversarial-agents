import { RigidBody } from '@react-three/rapier';

interface TrackSegment {
  position: [number, number, number];
  rotation: [number, number, number];
  args: [number, number, number];
}

const TRACK_CONFIG: TrackSegment[] = [
  { position: [0, 0, 40], rotation: [0, 0, 0], args: [20, 0.1, 100] },
  { position: [60, 0, 40], rotation: [0, 0, 0], args: [20, 0.1, 100] },
  { position: [30, 0, -10], rotation: [0, Math.PI / 2, 0], args: [20, 0.1, 80] },
  { position: [30, 0, 90], rotation: [0, Math.PI / 2, 0], args: [20, 0.1, 80] },
];

export function Track() {
  return (
    <group>
      {/* Offroad / Grass */}
      <RigidBody type="fixed" colliders="cuboid" userData={{ type: 'offroad' }}>
        <mesh receiveShadow position={[0, -0.5, 0]}>
          <boxGeometry args={[400, 1, 400]} />
          <meshStandardMaterial color="#2d5a27" />
        </mesh>
      </RigidBody>

      {/* Main Road Loop */}
      <group position={[0, 0.01, 0]}>
        {TRACK_CONFIG.map((segment, index) => (
          <RoadSection key={index} {...segment} />
        ))}
      </group>
    </group>
  );
}

function RoadSection({ position, rotation, args }: TrackSegment) {
  const [width, height, length] = args;
  const rumbleWidth = 1.5;

  return (
    <group position={position} rotation={rotation}>
      {/* Road */}
      <RigidBody type="fixed" colliders="cuboid" userData={{ type: 'road' }}>
        <mesh receiveShadow>
          <boxGeometry args={[width, height, length]} />
          <meshStandardMaterial color="#333" />
        </mesh>
      </RigidBody>

      {/* Rumble Strips */}
      <RumbleStrip position={[-width / 2 - rumbleWidth / 2, 0, 0]} args={[rumbleWidth, height + 0.1, length]} />
      <RumbleStrip position={[width / 2 + rumbleWidth / 2, 0, 0]} args={[rumbleWidth, height + 0.1, length]} />

      {/* Barriers */}
      <Barrier position={[-width / 2 - rumbleWidth - 0.5, 1, 0]} args={[1, 2.5, length]} />
      <Barrier position={[width / 2 + rumbleWidth + 0.5, 1, 0]} args={[1, 2.5, length]} />
    </group>
  );
}

function RumbleStrip({ position, args }: { position: [number, number, number], args: [number, number, number] }) {
  return (
    <RigidBody type="fixed" colliders="cuboid" userData={{ type: 'rumble' }}>
      <mesh position={position} receiveShadow>
        <boxGeometry args={args} />
        <meshStandardMaterial color="#c0392b" />
      </mesh>
    </RigidBody>
  );
}

function Barrier({ position, args }: { position: [number, number, number], args: [number, number, number] }) {
  return (
    <RigidBody type="fixed" colliders="cuboid" userData={{ type: 'barrier' }}>
      <mesh position={position} castShadow receiveShadow>
        <boxGeometry args={args} />
        <meshStandardMaterial color="#7f8c8d" />
      </mesh>
    </RigidBody>
  );
}
