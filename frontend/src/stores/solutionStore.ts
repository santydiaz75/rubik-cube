import { defineStore } from 'pinia'

import type { SolutionStep } from '@/domain/solution/solutionStep'

interface SolutionState {
  steps: SolutionStep[]
  currentIndex: number
  isPlaying: boolean
  speedMs: number
}

export const useSolutionStore = defineStore('solution', {
  state: (): SolutionState => ({
    steps: [],
    currentIndex: 0,
    isPlaying: false,
    speedMs: 900,
  }),
  getters: {
    currentStep: (state) => state.steps[state.currentIndex] ?? null,
    totalMoves: (state) => state.steps.length,
  },
  actions: {
    setSteps(steps: SolutionStep[]) {
      this.steps = steps
      this.currentIndex = 0
      this.isPlaying = false
    },
    next() {
      if (this.currentIndex < this.steps.length - 1) {
        this.currentIndex += 1
      }
    },
    previous() {
      if (this.currentIndex > 0) {
        this.currentIndex -= 1
      }
    },
    select(index: number) {
      if (index >= 0 && index < this.steps.length) {
        this.currentIndex = index
      }
    },
    setPlaying(value: boolean) {
      this.isPlaying = value
    },
    setSpeed(speedMs: number) {
      this.speedMs = speedMs
    },
    reset() {
      this.steps = []
      this.currentIndex = 0
      this.isPlaying = false
    },
  },
})
