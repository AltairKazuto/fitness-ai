
<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { reactive } from 'vue'
import { useSocketIO } from './WebSocket'

const { data, status, dailyLogs, results, beatsObject, sendEvent, userInfo } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
</script>
<template>
  <!--  <div class="flex flex-col h-dvh w-dvw bg-zinc-950 text-white">
-->
  <RouterView v-slot="{ Component }">
    <component
      :is="Component"
      :results="results"
      :dailyLogs="dailyLogs"
      :userInfo="userInfo"
      :beatsObject="beatsObject"
      @event="(event: string, data: any) => sendEvent(event, data)"
    />
  </RouterView>
  <!--  </div>
--></template>

