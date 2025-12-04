import { computed, reactive, ref } from 'vue'
const state = reactive({
  authenticated: false,
  user: 0,
})

export default function useAuth() {
  const authenticated = computed(() => state.authenticated)
  const user = computed(() => state.user)
  return {
      state
    // authenticated,
    // user,
  }
}
