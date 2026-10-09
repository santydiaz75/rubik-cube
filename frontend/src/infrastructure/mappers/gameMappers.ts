import type { GameCreationResult, GameGateway } from '@/application/ports/gameGateway'
import type { UserGateway, UserSession } from '@/application/ports/userGateway'
import type { CubeDraft } from '@/domain/cube/cubeState'
import type { GameSummary, SolutionStep } from '@/domain/solution/solutionStep'
import { apiClient } from '@/infrastructure/http/apiClient'

function toGameSummary(payload: GameSummary): GameSummary {
  return payload
}

function toSolutionStep(payload: SolutionStep): SolutionStep {
  return payload
}

export const httpUserGateway: UserGateway = {
  async upsertUser(username: string, fullname: string): Promise<UserSession> {
    const response = await apiClient.put<UserSession>(`/users/${username}`, { fullname })
    return response.data
  },
}

export const httpGameGateway: GameGateway = {
  async createGame(userId: string, cube: CubeDraft): Promise<GameCreationResult> {
    const response = await apiClient.post<GameCreationResult>('/games/', { userId, cube })
    return {
      game: toGameSummary(response.data.game),
      totalMoves: response.data.totalMoves,
      steps: response.data.steps.map(toSolutionStep),
    }
  },
  async getGame(gameId: string): Promise<GameSummary> {
    const response = await apiClient.get<GameSummary>(`/games/${gameId}`)
    return toGameSummary(response.data)
  },
  async getSteps(gameId: string): Promise<SolutionStep[]> {
    const response = await apiClient.get<{ steps: SolutionStep[] }>(`/games/${gameId}/steps`)
    return response.data.steps.map(toSolutionStep)
  },
}
