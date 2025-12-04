import { createRouter, createWebHistory } from 'vue-router'
import Home from '../src/Game.vue'
import Dashboard from '../src/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  ],
})

export default router
