import { useEffect } from 'react';
import { useStore } from './store';

export function useKeyboard() {
  const setKeys = useStore((state) => state.setKeys);
  const toggleCameraMode = useStore((state) => state.toggleCameraMode);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.code) {
        case 'Space':
          setKeys({ forward: true });
          break;
        case 'KeyS':
        case 'ArrowDown':
          setKeys({ backward: true });
          break;
        case 'KeyA':
        case 'ArrowLeft':
          setKeys({ left: true });
          break;
        case 'KeyD':
        case 'ArrowRight':
          setKeys({ right: true });
          break;
        case 'KeyR':
          useStore.getState().resetGame();
          break;
        case 'Tab':
          e.preventDefault();
          toggleCameraMode();
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch (e.code) {
        case 'Space':
          setKeys({ forward: false });
          break;
        case 'KeyS':
        case 'ArrowDown':
          setKeys({ backward: false });
          break;
        case 'KeyA':
        case 'ArrowLeft':
          setKeys({ left: false });
          break;
        case 'KeyD':
        case 'ArrowRight':
          setKeys({ right: false });
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [setKeys, toggleCameraMode]);
}
