import { ref, onMounted, onUnmounted } from 'vue'
import { io, Socket } from 'socket.io-client' // Import the specific 'io' function

export function useSocketIO(url: string) {
  const socket = ref<Socket | null>(null)
  const data = ref<string | null>(null)
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

    socket.value.on('send_conf', (message: string) => {
      console.log('confidence', message)
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
  return { socket, data, status, sendEvent, close, connect }
}
