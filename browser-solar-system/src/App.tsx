import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import SolarSystem from './components/SolarSystem'

function App() {
  return (
    <Canvas shadows camera={{ position: [0, 20, 50], fov: 45 }}>
      <color attach="background" args={['#000']} />
      <Stars radius={300} depth={60} count={20000} factor={7} saturation={0} fade speed={1} />
      <ambientLight intensity={0.1} />
      <SolarSystem />
      <OrbitControls makeDefault />
      <EffectComposer>
        <Bloom luminanceThreshold={1} mipmapBlur intensity={1.5} />
      </EffectComposer>
    </Canvas>
  )
}

export default App
