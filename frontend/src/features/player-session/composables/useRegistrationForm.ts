import { computed, shallowRef } from 'vue'

export function useRegistrationForm() {
  const username = shallowRef('')
  const fullname = shallowRef('')

  const canSubmit = computed(() => username.value.trim().length > 0 && fullname.value.trim().length > 0)

  return {
    username,
    fullname,
    canSubmit,
  }
}
