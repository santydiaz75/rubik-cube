<script setup lang="ts">
import { computed, onBeforeUnmount, watch } from 'vue'

import { requestSolution } from '@/application/use_cases/requestSolution'
import type { CubeColor } from '@/domain/cube/cubeColors'
import { getColorCounts, type CubeFace } from '@/domain/cube/cubeState'
import CubeEditor from '@/features/cube-editor/components/CubeEditor.vue'
import RegistrationForm from '@/features/player-session/components/RegistrationForm.vue'
import CubeStatePreview from '@/features/solution-player/components/CubeStatePreview.vue'
import SolutionPlayer from '@/features/solution-player/components/SolutionPlayer.vue'
import { httpGameGateway } from '@/infrastructure/mappers/gameMappers'
import { useCubeEditorStore } from '@/stores/cubeEditorStore'
import { useGameStore } from '@/stores/gameStore'
import { usePlayerStore } from '@/stores/playerStore'
import { useSolutionStore } from '@/stores/solutionStore'

const playerStore = usePlayerStore()
const cubeEditorStore = useCubeEditorStore()
const gameStore = useGameStore()
const solutionStore = useSolutionStore()

const colorCounts = computed(() => getColorCounts(cubeEditorStore.cube))
const currentCubeState = computed(() => solutionStore.currentStep?.cubeState ?? null)
const canResolve = computed(() => cubeEditorStore.canResolve && Boolean(playerStore.currentUser))

let timer: number | null = null

async function handleRegister(payload: { username: string; fullname: string }) {
  await playerStore.register(payload.username, payload.fullname)
}

function handleSelectColor(color: CubeColor) {
  cubeEditorStore.setSelectedColor(color)
}

function handlePaintSticker(payload: { face: CubeFace; index: number }) {
  cubeEditorStore.paint(payload.face, payload.index)
}

async function handleResolve() {
  if (!playerStore.currentUser) {
    gameStore.failResolving('Debes registrar una sesión antes de resolver.')
    return
  }

  gameStore.startResolving()
  try {
    const result = await requestSolution(httpGameGateway, playerStore.currentUser.userId, cubeEditorStore.cube)
    gameStore.finishResolving(result.game)
    solutionStore.setSteps(result.steps)
  } catch (error) {
    const message = error instanceof Error ? error.message : 'No se pudo resolver el cubo'
    gameStore.failResolving(message)
  }
}

function stopPlayback() {
  solutionStore.setPlaying(false)
  if (timer !== null) {
    window.clearInterval(timer)
    timer = null
  }
}

watch(
  () => [solutionStore.isPlaying, solutionStore.speedMs, solutionStore.currentIndex, solutionStore.steps.length] as const,
  ([isPlaying, speedMs, currentIndex, totalSteps]) => {
    if (timer !== null) {
      window.clearInterval(timer)
      timer = null
    }

    if (!isPlaying || totalSteps === 0) {
      return
    }

    if (currentIndex >= totalSteps - 1) {
      solutionStore.setPlaying(false)
      return
    }

    timer = window.setInterval(() => {
      if (solutionStore.currentIndex >= solutionStore.steps.length - 1) {
        stopPlayback()
      } else {
        solutionStore.next()
      }
    }, speedMs)
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  stopPlayback()
})
</script>

<template>
  <VMain class="solver-page">
    <VContainer
      fluid
      class="solver-container"
    >
      <div class="solver-grid">
        <RegistrationForm
          :loading="playerStore.loading"
          :error="playerStore.error"
          @submit="handleRegister"
        />

        <CubeEditor
          :cube="cubeEditorStore.cube"
          :selected-color="cubeEditorStore.selectedColor"
          :messages="cubeEditorStore.validationMessages"
          :color-counts="colorCounts"
          :can-resolve="cubeEditorStore.canResolve"
          :resolving="gameStore.resolving"
          :disabled="!canResolve"
          @select-color="handleSelectColor"
          @paint-sticker="handlePaintSticker"
          @resolve="handleResolve"
        />

        <SolutionPlayer
          :game="gameStore.currentGame"
          :steps="solutionStore.steps"
          :current-index="solutionStore.currentIndex"
          :is-playing="solutionStore.isPlaying"
          :speed-ms="solutionStore.speedMs"
          @previous="solutionStore.previous()"
          @next="solutionStore.next()"
          @toggle-playing="solutionStore.setPlaying($event)"
          @select-step="solutionStore.select($event)"
          @speed-change="solutionStore.setSpeed($event)"
        />

        <CubeStatePreview :cube="currentCubeState" />
      </div>

      <VAlert
        v-if="gameStore.error"
        type="error"
        variant="tonal"
        class="page-alert"
      >
        {{ gameStore.error }}
      </VAlert>
    </VContainer>
  </VMain>
</template>

<style scoped>
.solver-page {
  min-height: 100vh;
  background: #f5f7fb;
}

.solver-container {
  min-height: 100vh;
  padding: 1.5rem;
}

.solver-grid {
  display: grid;
  grid-template-columns: minmax(18rem, 22rem) minmax(28rem, 1fr) minmax(22rem, 28rem);
  grid-template-areas:
    'registration editor player'
    'preview editor player';
  gap: 1.5rem;
  align-items: start;
}

.solver-grid :deep(.panel-card:nth-child(1)) {
  grid-area: registration;
}

.solver-grid :deep(.panel-card:nth-child(2)) {
  grid-area: editor;
}

.solver-grid :deep(.panel-card:nth-child(3)) {
  grid-area: player;
}

.solver-grid :deep(.panel-card:nth-child(4)) {
  grid-area: preview;
}

.page-alert {
  margin-top: 1rem;
}

@media (max-width: 1280px) {
  .solver-grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      'registration'
      'editor'
      'player'
      'preview';
  }
}
</style>
