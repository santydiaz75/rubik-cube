<script setup lang="ts">
import type { CubeColor } from '@/domain/cube/cubeColors'
import type { CubeValidationMessage } from '@/domain/cube/cubeState'

const props = defineProps<{
  messages: CubeValidationMessage[]
  colorCounts: Record<CubeColor, number>
  canResolve: boolean
}>()
</script>

<template>
  <div class="summary">
    <VAlert
      :type="props.canResolve ? 'success' : 'warning'"
      variant="tonal"
    >
      {{ props.canResolve ? 'El cubo está listo para resolverse.' : 'Corrige los errores antes de resolver.' }}
    </VAlert>

    <div class="counts">
      <VChip
        v-for="(count, color) in props.colorCounts"
        :key="color"
        class="count-chip"
      >
        {{ color }}: {{ count }}/9
      </VChip>
    </div>

    <VList
      v-if="props.messages.length > 0"
      density="comfortable"
      lines="two"
    >
      <VListItem
        v-for="message in props.messages"
        :key="message.code + message.message"
        :title="message.message"
      />
    </VList>
  </div>
</template>

<style scoped>
.summary {
  display: grid;
  gap: 1rem;
}

.counts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.count-chip {
  text-transform: capitalize;
}
</style>
