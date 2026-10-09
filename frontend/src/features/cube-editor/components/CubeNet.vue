<script setup lang="ts">
import { cubeFaces, type CubeDraft, type CubeFace } from '@/domain/cube/cubeState'

const props = withDefaults(defineProps<{
  cube: CubeDraft
  readonly?: boolean
}>(), {
  readonly: false,
})

const emit = defineEmits<{
  stickerSelected: [payload: { face: CubeFace; index: number }]
}>()

const faceLabels: Record<CubeFace, string> = {
  u: 'U',
  d: 'D',
  f: 'F',
  b: 'B',
  l: 'L',
  r: 'R',
}

const faceAreas: Record<CubeFace, string> = {
  u: 'u',
  l: 'l',
  f: 'f',
  r: 'r',
  b: 'b',
  d: 'd',
}

function handleSticker(face: CubeFace, index: number) {
  if (!props.readonly) {
    emit('stickerSelected', { face, index })
  }
}
</script>

<template>
  <div class="cube-net">
    <section
      v-for="face in cubeFaces"
      :key="face"
      class="face-panel"
      :style="{ gridArea: faceAreas[face] }"
    >
      <header class="face-header">{{ faceLabels[face] }}</header>
      <div class="face-grid">
        <button
          v-for="(color, index) in props.cube.faces[face]"
          :key="`${face}-${index}`"
          type="button"
          class="sticker"
          :style="{ backgroundColor: `var(--rubik-${color})` }"
          :disabled="props.readonly"
          @click="handleSticker(face, index)"
        >
          <span class="sr-only">{{ faceLabels[face] }} {{ index + 1 }}</span>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.cube-net {
  display: grid;
  grid-template-areas:
    ". u . ."
    "l f r b"
    ". d . .";
  gap: 1rem;
  justify-content: center;
}

.face-panel {
  display: grid;
  gap: 0.5rem;
}

.face-header {
  text-align: center;
  font-weight: 700;
}

.face-grid {
  display: grid;
  grid-template-columns: repeat(3, 3rem);
  gap: 0.35rem;
}

.sticker {
  width: 3rem;
  height: 3rem;
  border: 2px solid #111827;
  border-radius: 0.35rem;
  cursor: pointer;
}

.sticker:disabled {
  cursor: default;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
