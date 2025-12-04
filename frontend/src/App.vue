<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useSocketIO } from './WebSocket'
import Camera from 'simple-vue-camera'

const { data, status, sendEvent } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
const camera_ref = ref<InstanceType<typeof Camera>>()

const sendCustomMessage = () => {
  sendEvent('my_custom_event', {
    message: 'Hello from Vue client!',
    timestamp: Date.now(),
  })
}
const url = ref('')

const snapshot = async () => {
  const blob = await camera_ref.value?.snapshot()
  if (blob instanceof Blob) {
    url.value = URL.createObjectURL(blob)
  }
}

const sen = () => {
  sendEvent('send_image', {
    message: 'Hello from Vue client!'
    // timestamp: Date.now(),
  })
}

const play = () => {
  camera_ref.value?.start()
}
</script>

<template>
  <div class="camera-container">
    <camera
      style="{width: 640px, height: 480px}"
      :resolution="{ width: 1280, height: 720 }"
      ref="camera_ref"
      :autoplay="true"
      :playsinline="true"
      :constraints="{
        video: {
          width: { ideal: 1280 }, // Lowering resolution can sometimes enable higher FPS
          height: { ideal: 720 },
          frameRate: { ideal: 60 }, // Request 60 FPS
        },
      }"
    ></camera>
  </div>
  <button @click="snapshot">snapshot</button>
  <button @click="sen">send</button>
  <button @click="sendCustomMessage" :disabled="status !== 'CONNECTED'">Send Custom Event</button>
  <img :src="url" />
</template>

<style scoped>
.camera-container {
  /* Set the display size you want here */
  width: 1280px;
  height: 720px;
  /* Optional: Add a border or other styling for visualization */
  border: 2px solid black;
  /* Ensure the video element inside fits the container */
  position: relative;
}

/* Target the actual video element within the container */
.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover; /* or 'fill', 'contain', 'none', 'scale-down' depending on desired behavior */
}
</style>
