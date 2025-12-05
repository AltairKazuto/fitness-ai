<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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

 interface UserInfo {
    user_id: number
    username: string
    password: string
  }

const props = defineProps<{
    dailyLogs: DailyLog[]
    userInfo: UserInfo
    results?: any
    beatsObject?: any
}>()
const emits = defineEmits(['event'])

onMounted(() => {
    emits('event', 'get_logs', {
        id: state.user,
    })
    emits('event', 'get_user_info', {
        id: state.user,
    })
})


const getProgressPercentage = (log: DailyLog): string => {
    if (log.goal_points === 0) return '0%'
    const percentage = (log.earned_points / log.goal_points) * 100
    return `${Math.min(percentage, 100)}%`
}

const getProgressValue = (log: DailyLog): number => {
    if (log.goal_points === 0) return 0
    const value = (log.earned_points / log.goal_points) * 100
    return Math.min(value, 100)
}


// Compute the is_goal_met status based on points
const isGoalMetComputed = (log: DailyLog): boolean => {
    return log.earned_points >= log.goal_points
}


const currentDayLog = computed<DailyLog | undefined>(() => {
    if (!props.dailyLogs || props.dailyLogs.length === 0) return undefined;
    
    // Sort logs by date descending
    const sortedLogs = [...props.dailyLogs].sort((a, b) => 
        new Date(b.log_date).getTime() - new Date(a.log_date).getTime()
    );

    // Get the latest log entry
    return sortedLogs[0];
});


const strokeDashoffset = computed<number>(() => {
    const log = currentDayLog.value;
    if (!log) return 283; 
    
    const percentage = getProgressValue(log);
    // Formula: 283 - (283 * percentage / 100)
    return 283 - (283 * percentage / 100);
});


// Calculate the status text and color for the progress bar
const statusText = computed<string>(() => {
    const log = currentDayLog.value;
    if (!log) return "No Data";
    
    return isGoalMetComputed(log) ? "GOAL MET!" : "Active Goal";
});

const statusColor = computed<string>(() => {
    const log = currentDayLog.value;
    if (!log) return 'text-gray-400';
    
    return isGoalMetComputed(log) ? 'text-green-400' : 'text-yellow-400';
});

</script>

<template>
    <div class="min-h-screen bg-gray-900 text-gray-100 p-8">
        
        <header class="flex justify-between items-center mb-8">
            <h1 class="text-4xl font-extrabold text-teal-400 tracking-tight">Daily Logs</h1>
            <div class="space-x-4">
                <RouterLink to="/game">
                    <button class="bg-teal-600 hover:bg-teal-500 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-lg">
                        Go to Game
                    </button>
                </RouterLink>
                <RouterLink to="/">
                    <button @click="state.authenticated = false" class="bg-red-600 hover:bg-red-500 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-lg">
                        Logout
                    </button>
                </RouterLink>
            </div>
        </header>

        <div class="mb-12 bg-gray-800 p-6 py-10 rounded-xl shadow-2xl border border-gray-700">
            
            <div class="flex">
              <div v-if="currentDayLog" class="relative w-40 h-40 ml-10">
                  <svg viewBox="0 0 100 100" class="w-full h-full transform -rotate-90">
                      <circle 
                          cx="50" cy="50" r="45" 
                          fill="transparent" 
                          stroke="#374151" 
                          stroke-width="10"
                      ></circle>
                      <circle 
                          cx="50" cy="50" r="45" 
                          fill="transparent" 
                          stroke-width="10"
                          stroke-dasharray="283"
                          :stroke-dashoffset="strokeDashoffset"
                          class="transition-all duration-1000 ease-out"
                          :stroke="isGoalMetComputed(currentDayLog) ? '#10B981' : '#F59E0B'" 
                      ></circle>
                  </svg>

                  <div class="absolute inset-0 flex flex-col items-center justify-center">
  
                      <p class="text-3xl font-extrabold" :class="statusColor">
                          {{ getProgressValue(currentDayLog).toFixed(0) }}%
                      </p>
                      <p class="text-sm font-medium mt-1 uppercase" :class="statusColor">{{ statusText }}</p>
                      <p class="text-xs text-gray-400 mt-1">
                          {{ currentDayLog.earned_points }} / {{ currentDayLog.goal_points }} pts
                      </p>
                  </div>
              </div>
              <div v-else class="text-lg text-gray-400 p-4">
                  No log found for the current day. Start a game to generate one!
              </div>
<div class="flex flex-col justify-begin mx-6 my-4 mb-4">
  <h2 class="text-4xl font-semibold text-white mb-3 leading-none">
            Welcome <span class="text-teal-400"> {{ userInfo?.username }} </span>!
        </h2>
  <h2 class="text-2xl font-semibold text-white mb-1 leading-none">
            Progress for Today
        </h2>
  <h2 class="text-xl font-medium text-gray-400 mt-0 leading-none">
            {{ new Date(currentDayLog?.log_date || Date.now()).toLocaleDateString() }}
        </h2>
        
    </div>
            </div>
        </div>
        
        <div class="bg-gray-800 p-6 rounded-xl shadow-2xl overflow-x-auto border border-gray-700">
            <table class="min-w-full divide-y divide-gray-700">
                <thead class="bg-gray-700">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Goal Progress</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Points</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
                    </tr>
                </thead>
                <tbody class="bg-gray-800 divide-y divide-gray-700">
                    <tr v-for="log in props.dailyLogs" :key="log.id" class="hover:bg-gray-700 transition duration-100">
                        
                        <td class="px-6 py-4 whitespace-nowrap text-s font-medium text-gray-100">
                            {{ new Date(log.log_date).toLocaleDateString() }}
                        </td>

                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center space-x-3">
                                <div class="w-full bg-gray-600 rounded-full h-5">
                                    <div 
                                        class="h-5 rounded-full transition-all duration-500"
                                        :style="{ width: getProgressPercentage(log) }"
                                        :class="{
                                            'bg-green-400': isGoalMetComputed(log),
                                            'bg-yellow-400': !isGoalMetComputed(log),
                                        }"
                                    ></div>
                                </div>
                                <span class="text-s font-semibold" :class="isGoalMetComputed(log) ? 'text-green-400' : 'text-yellow-400'">
                                    {{ getProgressPercentage(log) }}
                                </span>
                            </div>
                        </td>

                        <td class="px-6 py-4 whitespace-nowrap text-s text-gray-300">
                            <span class="font-bold text-white">{{ log.earned_points }}</span> / {{ log.goal_points }}
                        </td>

                        <td class="px-6 py-4 whitespace-nowrap text-s font-medium">
                            <div v-if="isGoalMetComputed(log)" class="flex items-center text-green-400">
                                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                Goal Met
                            </div>
                            <div v-else class="text-yellow-400">
                                Still Working
                            </div>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>