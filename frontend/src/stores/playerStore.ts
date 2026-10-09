import { defineStore } from 'pinia'

import type { UserSession } from '@/application/ports/userGateway'
import { registerPlayer } from '@/application/use_cases/registerPlayer'
import type { AppError } from '@/application/use_cases/result'
import { httpUserGateway } from '@/infrastructure/mappers/gameMappers'

interface PlayerState {
  currentUser: UserSession | null
  loading: boolean
  error: string | null
}

export const usePlayerStore = defineStore('player', {
  state: (): PlayerState => ({
    currentUser: null,
    loading: false,
    error: null,
  }),
  actions: {
    async register(username: string, fullname: string) {
      this.loading = true
      this.error = null
      try {
        this.currentUser = await registerPlayer(httpUserGateway, username, fullname)
      } catch (error) {
        this.error = (error as AppError).message
        throw error
      } finally {
        this.loading = false
      }
    },
  },
})
