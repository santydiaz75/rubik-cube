import { defineStore } from 'pinia'

import type { GameSummary } from '@/domain/solution/solutionStep'

interface GameState {
  currentGame: GameSummary | null
  resolving: boolean
  error: string | null
}

export const useGameStore = defineStore('game', {
  state: (): GameState => ({
    currentGame: null,
    resolving: false,
    error: null,
  }),
  actions: {
    startResolving() {
      this.resolving = true
      this.error = null
    },
    finishResolving(game: GameSummary) {
      this.currentGame = game
      this.resolving = false
      this.error = null
    },
    failResolving(message: string) {
      this.resolving = false
      this.error = message
    },
  },
})
