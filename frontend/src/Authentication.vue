<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import useAuth from './auth'
const router = useRouter()
const props = defineProps(['results', 'beatsObject'])
const emits = defineEmits(['event'])

const { state } = useAuth()
const l_username = ref('')
const l_password = ref('')
const l_errorMessage = ref('')

const r_username = ref('')
const r_password = ref('')
const r_errorMessage = ref('')

const handleLogin = async () => {
  l_errorMessage.value = ''
  emits('event', 'login', {
    username: l_username.value,
    password: l_password.value,
  })
}
const handleRegister = async () => {
  r_errorMessage.value = ''
  emits('event', 'register', {
    username: r_username.value,
    password: r_password.value,
  })
}

watch(
  () => state.authenticated,
  (newVal, oldVal) => {
    console.log('b')
    if (newVal) {
      router.push('/dashboard')
    }
  },
)
</script>

<template>
  <form @submit.prevent="handleLogin">
    <div>
      <label for="l_username">Username:</label>
      <input type="text" id="l_username" v-model="l_username" required />
    </div>
    <div>
      <label for="l_password">Password:</label>
      <input type="password" id="l_password" v-model="l_password" required />
    </div>
    <button type="submit">Login</button>
    <p v-if="l_errorMessage" class="error-message">{{ l_errorMessage }}</p>
  </form>
  <form @submit.prevent="handleRegister">
    <div>
      <label for="r_username">Username:</label>
      <input type="text" id="r_username" v-model="r_username" required />
    </div>
    <div>
      <label for="r_password">Password:</label>
      <input type="r_password" id="r_password" v-model="r_password" required />
    </div>
    <button type="submit">Login</button>
    <p v-if="r_errorMessage" class="error-message">{{ r_errorMessage }}</p>
  </form>
</template>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
