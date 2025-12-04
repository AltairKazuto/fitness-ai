<template>
  <div>
    <h1>Music Tempo Detection (TypeScript)</h1>
    <input type="file" @change="handleFileUpload" accept="audio/*" />
    <p v-if="loading">Detecting tempo... please wait.</p>
    <p vif="bpm">Detected BPM: {{ bpm }}</p>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// The import vvworks correctly because the package includes type definitions.
// @ts-ignore
import MusicTempo from 'music-tempo'

// Explicitly type refs
const bpm = ref<number | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Type the event handler and access HTMLInputElement properties
const handleFileUpload = async (event: Event): Promise<void> => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] // Access the first file

  if (!file) return

  loading.value = true
  bpm.value = null
  error.value = null

  try {
    // Standard Web Audio API usage
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    const arrayBuffer: ArrayBuffer = await file.arrayBuffer()
    const audioBuffer: AudioBuffer = await audioContext.decodeAudioData(arrayBuffer)

    const channelData: Float32Array = audioBuffer.getChannelData(0)

    // Instantiate MusicTempo (types are inferred correctly here)
    const mt = new MusicTempo(channelData)

    // The detect() method returns a number (BPM)
    bpm.value = mt.detect()
  } catch (err) {
    console.error('Error processing audio file:', err)
    error.value = 'Failed to process audio file.'
  } finally {
    loading.value = false
  }
}
</script>
