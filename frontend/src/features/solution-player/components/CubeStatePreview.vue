<script setup lang="ts">
import CubeNet from '@/features/cube-editor/components/CubeNet.vue'
import type { CubeDraft } from '@/domain/cube/cubeState'

defineProps<{
  cube: CubeDraft | null
}>()
</script>

<template>
  <VCard class="panel-card">
    <VCardTitle>Vista del paso actual</VCardTitle>
    <VCardText>
      <CubeNet
        v-if="cube"
        :cube="cube"
        readonly
      />
      <VAlert
        v-else
        type="info"
        variant="tonal"
      >
        La vista del cubo aparecerá cuando exista una solución o cuando selecciones un paso.
      </VAlert>
    </VCardText>
  </VCard>
</template>

<style scoped>
.panel-card {
  height: 100%;
}
</style>
