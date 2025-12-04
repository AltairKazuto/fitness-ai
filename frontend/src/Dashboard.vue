<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import useAuth from './auth'

const { state } = useAuth()

interface DailyLog {
  id: number
  user_id: number
  log_date: string
  goal_points: number
  earned_points: number
  is_goal_met: boolean
}
const props = defineProps(['dailyLogs', 'results', 'beatsObject'])
const emits = defineEmits(['event'])

onMounted(() => {
  emits('event', 'get_logs', {
    id: state.user,
  })
})
</script>

<template>
  <RouterLink to="/"><button @click="state.authenticated = false">Logout</button></RouterLink>
  <RouterLink to="/game">Game</RouterLink>

  <div>
    <h1>Daily Logs</h1>
    <table border="1" cellpadding="5">
      <thead>
        <tr>
          <th>ID</th>
          <th>User ID</th>
          <th>Date</th>
          <th>Goal Points</th>
          <th>Earned Points</th>
          <th>Goal Met?</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in props.dailyLogs" :key="log.id">
          <td>{{ log.id }}</td>
          <td>{{ log.user_id }}</td>
          <td>{{ log.log_date }}</td>
          <td>{{ log.goal_points }}</td>
          <td>{{ log.earned_points }}</td>
          <td>{{ log.is_goal_met ? 'Yes' : 'No' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
