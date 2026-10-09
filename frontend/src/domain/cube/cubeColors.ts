export const cubeColors = ['white', 'yellow', 'green', 'blue', 'orange', 'red'] as const

export type CubeColor = (typeof cubeColors)[number]

export const cubeColorLabels: Record<CubeColor, string> = {
  white: 'Blanco',
  yellow: 'Amarillo',
  green: 'Verde',
  blue: 'Azul',
  orange: 'Naranja',
  red: 'Rojo',
}
