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
const targetBarLit = ref(false); 



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
    targetBarLit.value = true;
    prevTimer.value = beatsObject.beats.shift()!
    currentPrediction.value = beatsObject.pose.shift()

    setTimeout(() => {
      targetBarLit.value = false;
    }, 500); 
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
    <div class="min-h-screen bg-gray-900 text-white flex flex-col items-center p-4 relative">
  <div style="position: absolute; right: 50px">
    <h1>Score: {{ score }} + {{ added }}</h1>
  </div>

  <audio ref="audio_ref"></audio>
  

 <div class="camera-container" ref="container_ref">
  <camera
    style="{width: 640px, height: 480px}"
    :resolution="{ width: 1280, height: 720 }"
    ref="camera_ref"
    :autoplay="true"
    :playsinline="true"
    :constraints="{
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 60 },
      },
    }"
  ></camera>

  

  <div
    class="center-bar"
    :class="{ 'lit': targetBarLit }"
  ></div>
<h1 v-if="targetBarLit" class="floating-accuracy">  {{ accuracy }}
</h1>

  <div v-for="beat in incomingBeats" :key="beat[0]">
    <p
      :style="{
        position: 'absolute',
        top: '90%',
        left: `${(1280 / 2) + (beat[0]! - timer) * 500}px`, 
        transform: 'translate(-50%, -50%)',
        color: 'blue',
        fontWeight: 'bold',
      }"
    >
      {{ poses[beat[1]!] }}
    </p>
  </div>
</div>
  <input type="file" accept="audio/*" @change="handleFileChange" />


  <p>Class: {{ results[1] }}</p>
  <p>Confidence: {{ results[0] }}</p>
  <button @click="snapshot">snapshot</button>
  <button @click="request_beats">Request Beats</button>
  <!-- <img :src="url" /> -->
   </div>
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

.center-bar {
  position: absolute;
  top: 90%;
  left: 50%;
  width: 300px;
  height: 20px;
  transform: translate(-50%, -50%);
  border-radius: 10px;
  background: linear-gradient(90deg, #f5f5f5, #fcfdfd, #ececec);
  opacity: 0.2;
  box-shadow: 0 0 10px #02fff2, 0 0 20px #02fff2, 0 0 30px #02fff2;
  transition: opacity 0.1s, box-shadow 0.1s;
}

.center-bar.lit {
  opacity: 1;
  /* Neon glow layers */
  box-shadow:
    0 0 5px #02fff2,
    0 0 10px #02fff2,
    0 0 20px #02fff2,
    0 0 40px #02fff2,
    0 0 80px #02fff2,
    0 0 120px #02fff2;
  animation: neon-pulse 0.3s ease-in-out;
}

@keyframes neon-pulse {
  0% { box-shadow: 0 0 5px #02fff2, 0 0 10px #02fff2, 0 0 20px #02fff2; }
  50% { box-shadow: 0 0 30px #02fff2, 0 0 60px #02fff2, 0 0 120px #02fff2; }
  100% { box-shadow: 0 0 5px #02fff2, 0 0 10px #02fff2, 0 0 20px #02fff2; }
}

.floating-accuracy {
  position: absolute;
  top: 30%;
  left: 80%;
  transform: translate(-50%, -50%);
  color: #0ff;
  font-weight: bold;
  font-size: 40px;
  text-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 20px #0ff;
  animation: floatFade 0.8s ease-out forwards;
}

@keyframes floatFade {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -150%);
  }
}
</style>


