export interface PlanetData {
  name: string;
  color: string;
  size: number;
  distance: number;
  speed: number;
}

export const PLANETS: PlanetData[] = [
  { name: 'Mercury', color: '#A5A5A5', size: 0.4, distance: 5, speed: 0.4 },
  { name: 'Venus', color: '#E3BB76', size: 0.9, distance: 8, speed: 0.15 },
  { name: 'Earth', color: '#2271B3', size: 1, distance: 11, speed: 0.1 },
  { name: 'Mars', color: '#E27B58', size: 0.5, distance: 14, speed: 0.08 },
  { name: 'Jupiter', color: '#D39C7E', size: 2.5, distance: 20, speed: 0.02 },
  { name: 'Saturn', color: '#C5AB6E', size: 2.1, distance: 26, speed: 0.009 },
  { name: 'Uranus', color: '#B5E3E3', size: 1.2, distance: 32, speed: 0.004 },
  { name: 'Neptune', color: '#6081FF', size: 1.1, distance: 38, speed: 0.001 },
  { name: 'Pluto', color: '#D3B6AA', size: 0.3, distance: 42, speed: 0.0007 },
];
