import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

export type CameraMode = 'chase' | 'firstPerson' | 'topDown';

interface GameState {
  forward: boolean;
  backward: boolean;
  left: boolean;
  right: boolean;
  cameraMode: CameraMode;
  surface: string;
  isCrashed: boolean;
  reset: boolean;
  setKeys: (keys: Partial<Record<'forward' | 'backward' | 'left' | 'right' | 'reset', boolean>>) => void;
  setSurface: (surface: string) => void;
  setIsCrashed: (isCrashed: boolean) => void;
  toggleCameraMode: () => void;
  resetGame: () => void;
}

export const useStore = create<GameState>()(
  subscribeWithSelector((set) => ({
    forward: false,
    backward: false,
    left: false,
    right: false,
    reset: false,
    cameraMode: 'chase',
    surface: 'road',
    isCrashed: false,
    setKeys: (keys) => set((state) => ({ ...state, ...keys })),
    setSurface: (surface) => set({ surface }),
    setIsCrashed: (isCrashed) => set({ isCrashed }),
    toggleCameraMode: () =>
      set((state) => {
        const modes: CameraMode[] = ['chase', 'firstPerson', 'topDown'];
        const index = modes.indexOf(state.cameraMode);
        return { cameraMode: modes[(index + 1) % modes.length] };
      }),
    resetGame: () =>
      set((state) => ({
        ...state,
        reset: !state.reset, // toggle to trigger effect
        isCrashed: false,
      })),
  }))
);
