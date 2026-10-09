import type { CubeDraft } from '@/domain/cube/cubeState'

export interface GameSummary {
  idGame: string
  userId: string
  idCube: string
  status: 'created' | 'solving' | 'completed' | 'failed'
  score: number
  currentStep: number
  createdAt: string
  errorMessage?: string | null
}

export interface SolutionStep {
  idGame: string
  idCube: string
  movement: number
  notation: string
  cubeState: CubeDraft
}
