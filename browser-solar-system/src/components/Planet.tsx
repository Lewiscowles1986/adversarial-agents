import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { Line } from '@react-three/drei'
import { PlanetData } from '../data/planets'

interface PlanetProps {
  data: PlanetData
}

const Planet = ({ data }: PlanetProps) => {
  const planetRef = useRef<THREE.Mesh>(null)
  
  const orbitPoints = useMemo(() => {
    const points = []
    for (let i = 0; i <= 64; i++) {
      const angle = (i / 64) * 2 * Math.PI
      points.push(new THREE.Vector3(Math.cos(angle) * data.distance, 0, Math.sin(angle) * data.distance))
    }
    return points
  }, [data.distance])

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime() * data.speed
    const x = Math.cos(t) * data.distance
    const z = Math.sin(t) * data.distance
    if (planetRef.current) {
      planetRef.current.position.set(x, 0, z)
      planetRef.current.rotation.y += 0.01
    }
  })

  return (
    <group>
      {/* Orbit path */}
      <Line points={orbitPoints} color="#333" lineWidth={1} transparent opacity={0.3} />
      
      {/* Planet */}
      <mesh ref={planetRef} castShadow receiveShadow>
        <sphereGeometry args={[data.size, 32, 32]} />
        <meshStandardMaterial color={data.color} />
        {data.name === 'Saturn' && (
          <mesh rotation={[Math.PI / 2, 0, 0]} receiveShadow castShadow>
            <ringGeometry args={[data.size * 1.4, data.size * 2.2, 64]} />
            <meshStandardMaterial color="#887" side={THREE.DoubleSide} transparent opacity={0.6} />
          </mesh>
        )}
      </mesh>
    </group>
  )
}

export default Planet
