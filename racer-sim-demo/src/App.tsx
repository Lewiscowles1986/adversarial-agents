import { Canvas } from '@react-three/fiber';
import { Physics } from '@react-three/rapier';
import { Sky, Environment } from '@react-three/drei';
import { Suspense } from 'react';
import { Track } from './Track';
import { Car } from './Car';
import { useKeyboard } from './useKeyboard';
import { useStore } from './store';
import './App.css';

function Scene() {
  return (
    <>
      <Sky sunPosition={[100, 20, 100]} />
      <Environment preset="city" />
      <ambientLight intensity={0.5} />
      <directionalLight
        position={[10, 10, 10]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />
      
      <Physics gravity={[0, -9.81, 0]}>
        {/* <Debug /> */}
        <Suspense fallback={null}>
          <Track />
          <Car />
        </Suspense>
      </Physics>
    </>
  );
}

function Overlay() {
  const cameraMode = useStore((state) => state.cameraMode);
  const surface = useStore((state) => state.surface);
  const isCrashed = useStore((state) => state.isCrashed);
  
  return (
    <div className="overlay" style={{
      position: 'absolute',
      top: '20px',
      left: '20px',
      color: 'white',
      fontFamily: 'monospace',
      fontSize: '1.2rem',
      textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
      pointerEvents: 'none',
      background: 'rgba(0,0,0,0.4)',
      padding: '20px',
      borderRadius: '12px',
      border: '1px solid rgba(255,255,255,0.1)',
      backdropFilter: 'blur(4px)'
    }}>
      <div style={{ marginBottom: '10px' }}>
        Surface: <span style={{ 
          color: surface === 'road' ? '#4ade80' : surface === 'rumble' ? '#f87171' : '#fbbf24',
          fontWeight: 'bold'
        }}>{surface.toUpperCase()}</span>
      </div>
      <div>Camera: <span style={{ fontWeight: 'bold' }}>{cameraMode.toUpperCase()}</span></div>
      
      {isCrashed && (
        <div style={{ 
          marginTop: '20px', 
          color: '#ef4444', 
          fontSize: '2.5rem', 
          fontWeight: '900',
          animation: 'blink 0.4s infinite'
        }}>
          CRASHED!
        </div>
      )}

      <div style={{ marginTop: '25px', fontSize: '0.85rem', opacity: 0.7, lineHeight: '1.4' }}>
        <div>[SPACE] ACCELERATE</div>
        <div>[S/DOWN] REVERSE</div>
        <div>[A/D/LEFT/RIGHT] TURN</div>
        <div>[TAB] CHANGE CAMERA</div>
        <div>[R] RESET VEHICLE</div>
      </div>

      <style>{`
        @keyframes blink {
          0% { opacity: 1; }
          50% { opacity: 0.2; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

function App() {
  useKeyboard();

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000' }}>
      <Canvas shadows camera={{ position: [0, 5, 10], fov: 50 }}>
        <Scene />
      </Canvas>
      <Overlay />
    </div>
  );
}

export default App;
