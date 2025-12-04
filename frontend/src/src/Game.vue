<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useSocketIO } from '../WebSocket'
import Camera from 'simple-vue-camera'

const { data, status, results, beatsObject, sendEvent } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
const camera_ref = ref<InstanceType<typeof Camera>>()
const audio_ref = ref<HTMLAudioElement | undefined | null>()
const selectedSong = ref<File | undefined | null>()
const currentPrediction = ref<number | undefined>()
const timer = ref(0)
const prevTimer = ref<number>(0)
const poses = ['goddess pose', 'plank pose', 'tree pose', 'warrior2 pose']
const score = ref(0)
const added = ref(0)
const accuracy = ref('')

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

const incomingBeats = computed(() => {
  let incoming: Array<Array<number>> = []
  beatsObject.beats.forEach((beat, index: number) => {
    if (beat - timer.value < 3) {
      incoming.push([beat, beatsObject.pose[index]!])
    }
  })
  return incoming
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

watch(results, (newVal: Array<number>, oldVal) => {
  if (newVal[1] == currentPrediction.value) {
    added.value = Math.floor(200 * newVal[0]!)
    if (newVal[0]! > 0.98) {
      accuracy.value = 'Perfect'
    } else if (newVal[0]! > 0.9) {
      accuracy.value = 'Amazing'
    } else if (newVal[0]! > 0.75) {
      accuracy.value = 'Nice'
    } else {
      accuracy.value = 'Good'
    }
  } else {
    added.value = 50
    accuracy.value = 'Miss'
  }
  score.value += added.value
})

watch(beatDetected, (newVal, oldVal) => {
  if (newVal) {
    snapshot()
    prevTimer.value = beatsObject.beats.shift()!
    currentPrediction.value = beatsObject.pose.shift()
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
  <div style="position: absolute; right: 50px">
    <h1>Score: {{ score }} + {{ added }}</h1>
    <h1>{{ accuracy }}</h1>
  </div>

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

    <div v-for="beat in incomingBeats">
    <p
      :style="{
        position: 'absolute',
        top: '50%',
        left: '50%',
        'margin-left': (beat[0]! - timer) * 500 + 'px',
      }"
    >
      {{ poses[beat[1]!] }}
    </p>
  </div>

  <p style="position: absolute; left: 50%; top: 52%; transform: translate(-50%, 0%)">
    ^^^ Center here ^^^
  </p>
  <input type="file" accept="audio/*" @change="handleFileChange" />


  <p>Class: {{ results[1] }}</p>
  <p>Confidence: {{ results[0] }}</p>
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
