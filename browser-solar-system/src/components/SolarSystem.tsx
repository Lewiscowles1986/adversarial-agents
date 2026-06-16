import { PLANETS } from '../data/planets'
import Sun from './Sun'
import Planet from './Planet'
import AsteroidBelt from './AsteroidBelt'

const SolarSystem = () => {
  return (
    <group>
      <Sun />
      {PLANETS.map((planet) => (
        <Planet key={planet.name} data={planet} />
      ))}
      <AsteroidBelt />
    </group>
  )
}

export default SolarSystem
