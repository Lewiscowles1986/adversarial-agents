I have built a modern 3D Solar System application using **React**, **TypeScript**, and **Three.js** (via `@react-three/fiber` and `@react-three/drei`).

### Features
- **All 9 Planets:** Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto, each with unique colors and sizes.
- **Dynamic Animation:** Planets orbit the Sun at relative speeds.
- **Asteroid Belt:** A realistic asteroid belt positioned between Mars and Jupiter.
- **The Sun:** A central, glowing star that serves as the light source for the system.
- **Interactive Controls:** Full support for pan, zoom, and drag using your mouse or touch.
- **Visual Polish:** Includes orbit paths, Saturn's rings, and a starfield background.

### Project Structure
- `src/App.tsx`: Main entry point setting up the 3D Canvas and camera.
- `src/components/SolarSystem.tsx`: Orchestrates the planets and Sun.
- `src/components/Planet.tsx`: Handles individual planet rendering and orbital logic.
- `src/components/AsteroidBelt.tsx`: Efficiently renders thousands of asteroids using instanced meshes.
- `src/data/planets.ts`: Configuration data for the planetary bodies.

### How to Run
1. Install dependencies: `npm install`
2. Start the development server: `npm run dev`