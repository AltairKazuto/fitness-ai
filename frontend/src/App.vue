<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useSocketIO } from './WebSocket'
import Camera from 'simple-vue-camera'

const { data, status, results, beatsObject, sendEvent } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
const camera_ref = ref<InstanceType<typeof Camera>>()
const audio_ref = ref<HTMLAudioElement | undefined | null>()
const selectedSong = ref<File | undefined | null>()
const currentPrediction = ref<string | undefined>('')
const timer = ref(0)
const prevTimer = ref<number>(0)
const beatShow = ref('')

const incrementTimer = () => {
  if (beatsObject.beats[0]) {
    timer.value += 0.01
  }
}
setInterval(incrementTimer, 10)

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
    request_beats(fileList[0])
  } else {
    selectedSong.value = null
  }
}

watch(results, (newVal: Array<string>, oldVal) => {
  currentPrediction.value = newVal[0]
})

const beatDetected = computed(() => {
  if (beatsObject.beats[0]) {
    if (timer.value > beatsObject.beats[0]) {
      return true
    } else {
      return false
    }
  }
  return false
})

watch(beatDetected, (newVal, oldVal) => {
  if (newVal) {
    if (timer.value - prevTimer.value > 2) {
      beatShow.value += 'a'
      prevTimer.value = beatsObject.beats.shift()!
    } else {
      beatsObject.beats.shift()!
    }
    console.log(timer.value, prevTimer.value)
  }
})

watch(
  () => beatsObject.ready,
  (newVal, oldVal) => {
    if (newVal) {
      const reader = new FileReader()
      reader.onload = (e) => {
        if (audio_ref.value && typeof e.target?.result == 'string') {
          audio_ref.value.src = e.target.result
          audio_ref.value.play()
          timer.value = 0
        }
        beatsObject.ready = false
      }
      if (selectedSong.value) {
        reader.readAsDataURL(selectedSong.value)
      }
    }
  },
)
</script>

<template>
  <audio ref="audio_ref"></audio>

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
  <p>Class: {{ results[1] }}</p>
  <p>Confidence: {{ results[0] }}</p>
  <p>BeatDetect: {{ beatShow }}</p>

  <button @click="snapshot">snapshot</button>
  <button @click="request_beats">Request Beats</button>
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
