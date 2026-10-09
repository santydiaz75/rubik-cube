import { createRouter, createWebHistory } from 'vue-router'

import SolverPage from '@/presentation/pages/SolverPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'solver',
      component: SolverPage,
    },
  ],
})

export default router
