import type { UserGateway, UserSession } from '@/application/ports/userGateway'
import { AppError, toAppError } from '@/application/use_cases/result'

export async function registerPlayer(
  gateway: UserGateway,
  username: string,
  fullname: string,
): Promise<UserSession> {
  const normalizedUsername = username.trim().toLowerCase()
  const normalizedFullname = fullname.trim()

  if (!normalizedUsername) {
    throw new AppError('El username es obligatorio', 'USERNAME_REQUIRED')
  }

  if (!normalizedFullname) {
    throw new AppError('El nombre completo es obligatorio', 'FULLNAME_REQUIRED')
  }

  try {
    return await gateway.upsertUser(normalizedUsername, normalizedFullname)
  } catch (error) {
    throw toAppError(error)
  }
}
