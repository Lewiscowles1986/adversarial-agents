I have built a modern JS racing game demo using **React**, **Three.js** (`@react-three/fiber`), and **Rapier** physics.

### Key Features
- **Physics-Based Driving:** A custom arcade vehicle controller using RigidBody physics.
- **Surface Detection:** Real-time raycasting detects whether the car is on the **road**, **rumble strips**, **offroad (grass)**, or hitting a **barrier**, adjusting handling and speed accordingly.
- **Multiple Camera Modes:** 
  - **Chase:** Classic behind-the-car follow view.
  - **First Person:** Immersive driver's seat perspective.
  - **Top-Down:** Bird's-eye view for tactical positioning.
- **Track System:** A modular track environment with concrete barriers and alternating surfaces.
- **Controls:**
  - `Space`: Accelerate
  - `W` / `Up Arrow`: Accelerate
  - `S` / `Down Arrow`: Reverse / Brake
  - `A` / `Left Arrow`: Turn Left
  - `D` / `Right Arrow`: Turn Right
  - `Tab`: Cycle Camera Modes
  - `R`: Reset Vehicle (teleport to start)

### Technical Highlights
- **Framework:** Vite + React + TypeScript.
- **Rendering:** `@react-three/fiber` for the 3D scene, `@react-three/drei` for environment and helpers.
- **Physics:** `@react-three/rapier` for high-performance collision and rigid body simulation.
- **State:** `zustand` for ultra-fast, reactive input and game state management.

The project is fully implemented, TypeScript-verified, and ready for further track expansion.