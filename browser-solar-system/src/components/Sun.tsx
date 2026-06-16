const Sun = () => {
  return (
    <group>
      <pointLight position={[0, 0, 0]} intensity={500} decay={2} castShadow shadow-mapSize-width={2048} shadow-mapSize-height={2048} shadow-bias={-0.0001} />
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[2.5, 32, 32]} />
        <meshStandardMaterial
          emissive="#FDB813"
          emissiveIntensity={2}
          color="#FDB813"
        />
      </mesh>
    </group>
  )
}

export default Sun
