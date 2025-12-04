import { createRouter, createWebHistory } from 'vue-router'

import Game from '../src/Game.vue'
import Dashboard from '../Dashboard.vue'
import Authentication from '../Authentication.vue'
import useAuth from '../auth'

const { state } = useAuth()


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/',
      name: 'auth',
      component: Authentication,
    },
    {
      path: '/dashboard',
      name: 'dasboard',
      component: Dashboard,
    },
    {
      path: '/game',
      name: 'game',
      component: Game,
    },
  ],
})
router.beforeEach(async (to, _from) => {
      if (!state.authenticated) {
        if (to.name!== 'auth') {
          return { name: 'auth' }
        }
      }
      else {
        if (to.name== 'auth') {
          return { name: 'dashboard' }
        }
      }

})
export default router
