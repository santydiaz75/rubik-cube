export interface UserSession {
  userId: string
  username: string
  fullname: string
  score: number
}

export interface UserGateway {
  upsertUser(username: string, fullname: string): Promise<UserSession>
}
