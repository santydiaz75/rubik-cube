import { cubeColors, type CubeColor } from '@/domain/cube/cubeColors'

export type { CubeColor } from '@/domain/cube/cubeColors'

export const cubeFaces = ['u', 'd', 'f', 'b', 'l', 'r'] as const

export type CubeFace = (typeof cubeFaces)[number]

export interface CubeFaces {
  u: CubeColor[]
  d: CubeColor[]
  f: CubeColor[]
  b: CubeColor[]
  l: CubeColor[]
  r: CubeColor[]
}

export interface CubeDraft {
  cubeId: string
  status: 'in-progress' | 'solved'
  faces: CubeFaces
}

export interface CubeValidationMessage {
  code: string
  message: string
}

export function createSolvedCube(cubeId = 'rubik-3x3-standard'): CubeDraft {
  return {
    cubeId,
    status: 'solved',
    faces: {
      u: Array.from({ length: 9 }, () => 'white'),
      d: Array.from({ length: 9 }, () => 'yellow'),
      f: Array.from({ length: 9 }, () => 'green'),
      b: Array.from({ length: 9 }, () => 'blue'),
      l: Array.from({ length: 9 }, () => 'orange'),
      r: Array.from({ length: 9 }, () => 'red'),
    },
  }
}

export function createEmptyCube(cubeId = 'rubik-3x3-standard'): CubeDraft {
  const solved = createSolvedCube(cubeId)
  return {
    cubeId,
    status: 'in-progress',
    faces: {
      u: solved.faces.u.map(() => 'white'),
      d: solved.faces.d.map(() => 'yellow'),
      f: solved.faces.f.map(() => 'green'),
      b: solved.faces.b.map(() => 'blue'),
      l: solved.faces.l.map(() => 'orange'),
      r: solved.faces.r.map(() => 'red'),
    },
  }
}

export function cloneCube(cube: CubeDraft): CubeDraft {
  return {
    cubeId: cube.cubeId,
    status: cube.status,
    faces: {
      u: [...cube.faces.u],
      d: [...cube.faces.d],
      f: [...cube.faces.f],
      b: [...cube.faces.b],
      l: [...cube.faces.l],
      r: [...cube.faces.r],
    },
  }
}

export function paintSticker(cube: CubeDraft, face: CubeFace, index: number, color: CubeColor): CubeDraft {
  const next = cloneCube(cube)
  next.faces[face][index] = color
  next.status = isSolvedCube(next) ? 'solved' : 'in-progress'
  return next
}

export function isSolvedCube(cube: CubeDraft): boolean {
  return cubeFaces.every((face) => new Set(cube.faces[face]).size === 1)
}

export function getColorCounts(cube: CubeDraft): Record<CubeColor, number> {
  const counts = Object.fromEntries(cubeColors.map((color) => [color, 0])) as Record<CubeColor, number>
  for (const face of cubeFaces) {
    for (const color of cube.faces[face]) {
      counts[color] += 1
    }
  }
  return counts
}

export function validateCubeDraft(cube: CubeDraft): CubeValidationMessage[] {
  const messages: CubeValidationMessage[] = []
  const counts = getColorCounts(cube)

  for (const face of cubeFaces) {
    if (cube.faces[face].length !== 9) {
      messages.push({
        code: 'FACE_SIZE',
        message: `La cara ${face.toUpperCase()} debe tener exactamente 9 casillas.`,
      })
    }
  }

  for (const color of cubeColors) {
    if (counts[color] !== 9) {
      messages.push({
        code: 'COLOR_COUNT',
        message: `El color ${color} debe aparecer 9 veces y ahora aparece ${counts[color]}.`,
      })
    }
  }

  return messages
}
