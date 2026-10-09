import { defineStore } from 'pinia'

import {
  cloneCube,
  createSolvedCube,
  paintSticker,
  type CubeColor,
  type CubeDraft,
  type CubeFace,
  validateCubeDraft,
} from '@/domain/cube/cubeState'

interface CubeEditorState {
  cube: CubeDraft
  selectedColor: CubeColor
}

export const useCubeEditorStore = defineStore('cube-editor', {
  state: (): CubeEditorState => ({
    cube: createSolvedCube(),
    selectedColor: 'white',
  }),
  getters: {
    validationMessages: (state) => validateCubeDraft(state.cube),
    canResolve(): boolean {
      return this.validationMessages.length === 0
    },
  },
  actions: {
    setSelectedColor(color: CubeColor) {
      this.selectedColor = color
    },
    paint(face: CubeFace, index: number) {
      this.cube = paintSticker(this.cube, face, index, this.selectedColor)
    },
    replaceCube(cube: CubeDraft) {
      this.cube = cloneCube(cube)
    },
    resetToSolved() {
      this.cube = createSolvedCube()
    },
  },
})
