<template>
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
        <tr v-for="log in dailyLogs" :key="log.id">
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

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface DailyLog {
  id: number
  user_id: number
  log_date: string
  goal_points: number
  earned_points: number
  is_goal_met: boolean
}

const dailyLogs = ref<DailyLog[]>([])

onMounted(async () => {
  try {
    const response = await axios.get<DailyLog[]>('http://localhost:8000/daily_logs/1')
    dailyLogs.value = response.data
  } catch (err) {
    console.error('Error fetching daily logs:', err)
  }
})
</script>
