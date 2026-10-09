import type { CubeDraft } from '@/domain/cube/cubeState'
import type { GameSummary, SolutionStep } from '@/domain/solution/solutionStep'

export interface GameCreationResult {
  game: GameSummary
  totalMoves: number
  steps: SolutionStep[]
}

export interface GameGateway {
  createGame(userId: string, cube: CubeDraft): Promise<GameCreationResult>
  getGame(gameId: string): Promise<GameSummary>
  getSteps(gameId: string): Promise<SolutionStep[]>
}
