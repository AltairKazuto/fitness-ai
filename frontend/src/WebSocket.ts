import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { io, Socket } from 'socket.io-client' // Import the specific 'io' function

export function useSocketIO(url: string) {
  const socket = ref<Socket | null>(null)
  const data = ref<string | null>(null)
  const results = ref([])
  const beatsObject = reactive({
    beats: [0],
    pose: [0],
    ready: false,
  })
  const beats = ref('')
  const status = ref('DISCONNECTED')

  const connect = () => {
    // The Socket.IO client handles connection logic
    socket.value = io(url)
    status.value = 'CONNECTING'

    socket.value.on('connect', () => {
      status.value = 'CONNECTED'
      console.log('Socket.IO connected')
    })

    socket.value.on('disconnect', () => {
      status.value = 'DISCONNECTED'
      console.log('Socket.IO disconnected')
    })

    socket.value.on('error', (err: Error) => {
      status.value = 'ERROR'
      console.error('Socket.IO error:', err)
    })

    socket.value.on('send_results', (message: any) => {
      results.value = message
      console.log('results', message)
    })

    socket.value.on('send_beats', (message: any) => {
      let prev = message.shift()
      let processed_beats: Array<number> = [prev]
      let poses: Array<number> = []
      message.forEach((beat: number, index: number) => {
        if (beat - prev > 2) {
          processed_beats.push(beat)
          poses.push(Math.floor(Math.random() * 4))
          prev = beat
        }
      })
      beatsObject.beats = processed_beats
      beatsObject.pose = poses
      beatsObject.ready = true
      console.log('beats: ', processed_beats)
      console.log('poses: ', poses)
    })
  }

  // Function to emit custom events to the Flask server
  const sendEvent = (eventName: string, payload: any) => {
    if (socket.value && socket.value.connected) {
      // Use socket.emit() to send named events
      socket.value.emit(eventName, payload)
    }
  }

  const close = () => {
    socket.value?.disconnect()
  }

  onMounted(connect)
  onUnmounted(close)

  // Expose the sendEvent function
  return { socket, data, results, beatsObject, status, sendEvent, close, connect }
}
