import type { GameCreationResult, GameGateway } from '@/application/ports/gameGateway'
import type { CubeDraft } from '@/domain/cube/cubeState'
import { AppError, toAppError } from '@/application/use_cases/result'

export async function requestSolution(
  gateway: GameGateway,
  userId: string,
  cube: CubeDraft,
): Promise<GameCreationResult> {
  if (!userId) {
    throw new AppError('Debes registrar un jugador antes de resolver', 'USER_REQUIRED')
  }

  try {
    return await gateway.createGame(userId, cube)
  } catch (error) {
    throw toAppError(error)
  }
}
