<script setup lang="ts">
import type { GameSummary, SolutionStep } from '@/domain/solution/solutionStep'

const props = defineProps<{
  game: GameSummary | null
  steps: SolutionStep[]
  currentIndex: number
  isPlaying: boolean
  speedMs: number
}>()

const emit = defineEmits<{
  previous: []
  next: []
  togglePlaying: [value: boolean]
  selectStep: [index: number]
  speedChange: [value: number]
}>()
</script>

<template>
  <VCard class="panel-card">
    <VCardTitle>Reproductor de solución</VCardTitle>
    <VCardText class="player-layout">
      <VAlert
        v-if="!props.game"
        type="info"
        variant="tonal"
      >
        Aquí verás la secuencia paso a paso una vez resuelto el cubo.
      </VAlert>

      <template v-else>
        <div class="player-controls">
          <VBtn
            variant="outlined"
            :disabled="props.currentIndex === 0"
            @click="emit('previous')"
          >
            Paso anterior
          </VBtn>
          <VBtn
            color="primary"
            @click="emit('togglePlaying', !props.isPlaying)"
          >
            {{ props.isPlaying ? 'Pausa' : 'Play' }}
          </VBtn>
          <VBtn
            variant="outlined"
            :disabled="props.currentIndex >= props.steps.length - 1"
            @click="emit('next')"
          >
            Paso siguiente
          </VBtn>
        </div>

        <div class="summary">
          <span>Paso {{ props.steps.length === 0 ? 0 : props.currentIndex + 1 }} de {{ props.steps.length }}</span>
          <span>Total de movimientos: {{ props.game.score }}</span>
        </div>

        <VSlider
          :model-value="props.speedMs"
          min="300"
          max="1600"
          step="100"
          label="Velocidad de reproducción"
          thumb-label="always"
          @update:model-value="emit('speedChange', Number($event))"
        />

        <div class="step-list">
          <VChip
            v-for="(step, index) in props.steps"
            :key="`${step.idGame}-${step.movement}`"
            :color="index === props.currentIndex ? 'primary' : undefined"
            variant="tonal"
            class="step-chip"
            @click="emit('selectStep', index)"
          >
            {{ step.movement }} · {{ step.notation }}
          </VChip>
        </div>
      </template>
    </VCardText>
  </VCard>
</template>

<style scoped>
.panel-card {
  height: 100%;
}

.player-layout {
  display: grid;
  gap: 1rem;
}

.player-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.summary {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-weight: 600;
}

.step-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.step-chip {
  cursor: pointer;
}
</style>
