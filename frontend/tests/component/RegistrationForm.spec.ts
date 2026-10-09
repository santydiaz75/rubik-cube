import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import vuetify from '@/app/vuetify'
import RegistrationForm from '@/features/player-session/components/RegistrationForm.vue'

describe('RegistrationForm', () => {
  it('emits submit with the typed payload', async () => {
    const wrapper = mount(RegistrationForm, {
      props: {
        loading: false,
        error: null,
      },
      global: {
        plugins: [vuetify],
      },
    })

    const inputs = wrapper.findAll('input')
    await inputs[0]?.setValue('alice')
    await inputs[1]?.setValue('Alice')
    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('submit')?.[0]?.[0]).toEqual({
      username: 'alice',
      fullname: 'Alice',
    })
  })
})
