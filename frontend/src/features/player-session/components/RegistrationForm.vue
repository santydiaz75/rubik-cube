<script setup lang="ts">
import { useRegistrationForm } from '@/features/player-session/composables/useRegistrationForm'

const props = defineProps<{
  loading: boolean
  error: string | null
}>()

const emit = defineEmits<{
  submit: [payload: { username: string; fullname: string }]
}>()

const { username, fullname, canSubmit } = useRegistrationForm()

function handleSubmit() {
  emit('submit', { username: username.value, fullname: fullname.value })
}
</script>

<template>
  <VCard class="panel-card">
    <VCardTitle>Registrar sesión</VCardTitle>
    <VCardText class="panel-content">
      <VTextField
        v-model="username"
        label="Username"
        variant="outlined"
        density="comfortable"
      />
      <VTextField
        v-model="fullname"
        label="Nombre completo"
        variant="outlined"
        density="comfortable"
      />
      <VAlert
        v-if="props.error"
        type="error"
        variant="tonal"
      >
        {{ props.error }}
      </VAlert>
    </VCardText>
    <VCardActions>
      <VBtn
        color="primary"
        :loading="props.loading"
        :disabled="!canSubmit"
        @click="handleSubmit"
      >
        Guardar sesión
      </VBtn>
    </VCardActions>
  </VCard>
</template>

<style scoped>
.panel-card {
  height: 100%;
}

.panel-content {
  display: grid;
  gap: 1rem;
}
</style>
