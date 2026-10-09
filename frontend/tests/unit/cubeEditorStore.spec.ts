import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

import { useCubeEditorStore } from '@/stores/cubeEditorStore'

describe('cubeEditorStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('is valid when solved cube is loaded', () => {
    const store = useCubeEditorStore()
    expect(store.validationMessages).toEqual([])
    expect(store.canResolve).toBe(true)
  })

  it('updates stickers with the selected color', () => {
    const store = useCubeEditorStore()
    store.setSelectedColor('red')
    store.paint('u', 0)
    expect(store.cube.faces.u[0]).toBe('red')
  })
})
