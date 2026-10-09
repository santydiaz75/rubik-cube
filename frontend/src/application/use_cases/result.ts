export class AppError extends Error {
  readonly code: string
  readonly details: Array<{ face?: string; index?: number; issue?: string }>

  constructor(
    message: string,
    code = 'APP_ERROR',
    details: Array<{ face?: string; index?: number; issue?: string }> = [],
  ) {
    super(message)
    this.name = 'AppError'
    this.code = code
    this.details = details
  }
}

export function toAppError(error: unknown): AppError {
  if (error instanceof AppError) {
    return error
  }

  if (typeof error === 'object' && error !== null && 'response' in error) {
    const response = (error as { response?: { data?: { code?: string; message?: string; details?: Array<{ face?: string; index?: number; issue?: string }> } } }).response
    const payload = response?.data
    return new AppError(payload?.message ?? 'Unexpected request failure', payload?.code ?? 'REQUEST_ERROR', payload?.details ?? [])
  }

  return new AppError(error instanceof Error ? error.message : 'Unexpected application error')
}
