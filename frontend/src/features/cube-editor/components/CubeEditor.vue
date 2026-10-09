<script setup lang="ts">
import ColorPalette from '@/features/cube-editor/components/ColorPalette.vue'
import CubeNet from '@/features/cube-editor/components/CubeNet.vue'
import CubeValidationSummary from '@/features/cube-editor/components/CubeValidationSummary.vue'
import type { CubeColor } from '@/domain/cube/cubeColors'
import type { CubeDraft, CubeFace, CubeValidationMessage } from '@/domain/cube/cubeState'

const props = defineProps<{
  cube: CubeDraft
  selectedColor: CubeColor
  messages: CubeValidationMessage[]
  colorCounts: Record<CubeColor, number>
  canResolve: boolean
  resolving: boolean
  disabled: boolean
}>()

const emit = defineEmits<{
  selectColor: [color: CubeColor]
  paintSticker: [payload: { face: CubeFace; index: number }]
  resolve: []
}>()
</script>

<template>
  <VCard class="panel-card">
    <VCardTitle>Editor del cubo</VCardTitle>
    <VCardText class="editor-layout">
      <ColorPalette
        :selected-color="props.selectedColor"
        @select="emit('selectColor', $event)"
      />
      <CubeNet
        :cube="props.cube"
        @sticker-selected="emit('paintSticker', $event)"
      />
      <CubeValidationSummary
        :messages="props.messages"
        :color-counts="props.colorCounts"
        :can-resolve="props.canResolve"
      />
    </VCardText>
    <VCardActions>
      <VBtn
        color="primary"
        :loading="props.resolving"
        :disabled="props.disabled || !props.canResolve"
        @click="emit('resolve')"
      >
        Empezar
      </VBtn>
    </VCardActions>
  </VCard>
</template>

<style scoped>
.panel-card {
  height: 100%;
}

.editor-layout {
  display: grid;
  gap: 1.5rem;
}
</style>
