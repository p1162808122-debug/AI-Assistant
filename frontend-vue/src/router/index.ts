import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/MainContent.vue'),
    },
    {
      path: '/create',
      name: 'create',
      component: () => import('@/views/CreateTask.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/TaskHistory.vue'),
    },
    {
      path: '/task/:id',
      name: 'detail',
      component: () => import('@/views/TaskDetail.vue'),
    },
  ],
})

export default router
