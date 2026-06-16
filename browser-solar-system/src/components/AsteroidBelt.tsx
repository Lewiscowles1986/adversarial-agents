import { useRef, useMemo, useLayoutEffect } from 'react'
import * as THREE from 'three'

const AsteroidBelt = () => {
  const count = 1000
  const meshRef = useRef<THREE.InstancedMesh>(null)

  const particles = useMemo(() => {
    const temp = []
    for (let i = 0; i < count; i++) {
      const radius = 16 + Math.random() * 3
      const angle = Math.random() * Math.PI * 2
      const x = Math.cos(angle) * radius
      const z = Math.sin(angle) * radius
      const y = (Math.random() - 0.5) * 0.5
      
      const size = 0.02 + Math.random() * 0.05
      
      temp.push({ x, y, z, size })
    }
    return temp
  }, [])

  useLayoutEffect(() => {
    const dummy = new THREE.Object3D()
    if (meshRef.current) {
      particles.forEach((p, i) => {
        dummy.position.set(p.x, p.y, p.z)
        dummy.scale.set(p.size, p.size, p.size)
        dummy.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI)
        dummy.updateMatrix()
        meshRef.current!.setMatrixAt(i, dummy.matrix)
      })
      meshRef.current.instanceMatrix.needsUpdate = true
    }
  }, [particles])

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]} receiveShadow castShadow>
      <sphereGeometry args={[1, 4, 4]} />
      <meshStandardMaterial color="#888" />
    </instancedMesh>
  )
}

export default AsteroidBelt
