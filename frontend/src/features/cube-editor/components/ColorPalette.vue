<script setup lang="ts">
import { cubeColorLabels, type CubeColor } from '@/domain/cube/cubeColors'

const props = defineProps<{
  selectedColor: CubeColor
}>()

const emit = defineEmits<{
  select: [color: CubeColor]
}>()

const colors = Object.keys(cubeColorLabels) as CubeColor[]
</script>

<template>
  <div class="palette">
    <VBtn
      v-for="color in colors"
      :key="color"
      :class="['palette-button', { 'palette-button--selected': props.selectedColor === color }]"
      :style="{ backgroundColor: `var(--rubik-${color})`, color: color === 'white' ? '#111827' : '#ffffff' }"
      size="small"
      @click="emit('select', color)"
    >
      {{ cubeColorLabels[color] }}
    </VBtn>
  </div>
</template>

<style scoped>
.palette {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.palette-button {
  min-width: 7rem;
}

.palette-button--selected {
  outline: 3px solid #111827;
}
</style>
