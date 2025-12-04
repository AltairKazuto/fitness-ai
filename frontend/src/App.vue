<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useSocketIO } from './WebSocket'
import Camera from 'simple-vue-camera'

const { data, status, results, sendEvent } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
const camera_ref = ref<InstanceType<typeof Camera>>()
const selectedSong = ref<File | undefined | null>()

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
  sendEvent('send_image', {
    message: blob,
  })
}

const request_beats = (song: any) => {
  sendEvent('request_beats', {
    path: song,
  })
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const fileList = target.files
  if (fileList && fileList.length > 0) {
    selectedSong.value = fileList[0]
    console.log('b')
    request_beats(fileList[0])
    console.log('c')
  } else {
    selectedSong.value = null
  }
}

watch(results, (newVal, oldVal) => {
  console.log('bbb')
  console.log(newVal.value, oldVal)
})
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
  <input type="file" accept="audio/*" @change="handleFileChange" />

  <button @click="snapshot">snapshot</button>
  <button @click="request_beats">Request Beats</button>
  <button @click="sen">send</button>
  <button @click="sendCustomMessage" :disabled="status !== 'CONNECTED'">Send Custom Event</button>
  <img :src="url" />
</template>

<style scoped>
.camera-container {
  width: 1280px;
  height: 720px;
  border: 2px solid black;
  position: relative;
}
.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
