<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useSocketIO } from './WebSocket'
import Camera from 'simple-vue-camera'
import useAuth from './auth'

// const { data, status, results, beatsObject, sendEvent } = useSocketIO('http://localhost:5000') // Use http or https here for Socket.IO
const { state } = useAuth()
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

const props = defineProps(['results', 'beatsObject', 'dailyLogs'])
const emits = defineEmits(['event'])

const incrementTimer = () => {
  if (props.beatsObject.beats[0]) {
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
  emits('event', 'send_image', {
    message: blob,
  })
}

const request_beats = (song: any) => {
  emits('event', 'request_beats', {
    path: song,
  })
}

const addScore = () => {
  console.log('adding')
  emits('event', 'add_points', {
    id: state.user,
    add: score.value,
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
  props.beatsObject.beats.forEach((beat: number, index: number) => {
    if (beat - timer.value < 3) {
      incoming.push([beat, props.beatsObject.pose[index]!])
    }
  })
  return incoming
})

const beatDetected = computed(() => {
  if (props.beatsObject.beats[0]) {
    if (timer.value > props.beatsObject.beats[0]) {
      return true
    } else {
      return false
    }
  }
  return false
})

watch(
  () => props.results,
  (newVal: Array<number>, oldVal) => {
    if (newVal[1] == currentPrediction.value) {
      added.value = Math.floor(50 * newVal[0]!)
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
      added.value = 10
      accuracy.value = 'Miss'
    }
    score.value += added.value
  },
)

watch(beatDetected, (newVal, oldVal) => {
  if (newVal) {
    snapshot()
    prevTimer.value = props.beatsObject.beats.shift()!
    currentPrediction.value = props.beatsObject.pose.shift()
  }
})

watch(
  () => props.beatsObject.ready,
  (newVal, oldVal) => {
    if (newVal) {
      const reader = new FileReader()
      reader.onload = (e) => {
        if (audio_ref.value && typeof e.target?.result == 'string') {
          audio_ref.value.src = e.target.result
          audio_ref.value.play()
          timer.value = 0
        }
        props.beatsObject.ready = false
      }
      if (selectedSong.value) {
        reader.readAsDataURL(selectedSong.value)
      }
    }
  },
)
</script>

<template>
  <RouterLink to="/"><button @click="state.authenticated = false">Logout</button></RouterLink>
  <RouterLink to="/dashboard"><button @click="addScore">Logout</button></RouterLink>
  <div style="position: absolute; right: 50px">
    <h1 class="text-4xl">Score: {{ score }} + {{ added }}</h1>
    <h1 class="text-4xl">{{ accuracy }}</h1>
  </div>

  <audio ref="audio_ref"></audio>
  <p style="position: absolute; left: 50%; top: 52%; transform: translate(-50%, 0%)">
    ^^^ Center here ^^^
  </p>
  <div v-for="beat in incomingBeats">
    <p
      :style="{
        position: 'absolute',
        top: '50%',
        left: '50%',
        'margin-left': (beat[0]! - timer) * 500 + 'px',
        'white-space': 'nowrap',
      }"
    >
      {{ poses[beat[1]!] }}
    </p>
  </div>

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
  <!--  <button @click="snapshot">snapshot</button>
  <button @click="request_beats">Request Beats</button>
-->
  <!--  <img :src="url" />
--></template>

<style scoped>
.camera-container {
  width: 640px;
  height: 480px;
  border: 2px solid black;
  position: relative;
}
.camera-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
