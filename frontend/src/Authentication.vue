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
    <div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
        
        <div class="flex flex-col md:flex-row w-full max-w-4xl bg-gray-800 rounded-xl shadow-2xl overflow-hidden border border-gray-700">

            <div class="w-full md:w-1/2 p-10 space-y-6">
                <h1 class="text-3xl font-bold text-teal-400 text-center mb-6">Login</h1>
                
                <form @submit.prevent="handleLogin" class="space-y-4">
                    <div>
                        <label for="l_username" class="block text-sm font-medium text-gray-300 mb-1">Username</label>
                        <input 
                            type="text" 
                            id="l_username" 
                            v-model="l_username" 
                            required
                            class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-teal-500 focus:border-teal-500"
                        />
                    </div>
                    <div>
                        <label for="l_password" class="block text-sm font-medium text-gray-300 mb-1">Password</label>
                        <input 
                            type="password" 
                            id="l_password" 
                            v-model="l_password" 
                            required
                            class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-teal-500 focus:border-teal-500"
                        />
                    </div>
                    
                    <button type="submit" class="w-full bg-teal-600 hover:bg-teal-700 text-white font-semibold py-2 rounded-lg transition duration-200 shadow-md">
                        Sign In
                    </button>
                    
                    <p v-if="l_errorMessage" class="text-sm text-red-400 text-center mt-3">{{ l_errorMessage }}</p>
                </form>
            </div>

            <div class="md:w-px bg-gray-700 hidden md:block"></div>

            <div class="w-full md:w-1/2 p-10 space-y-6 relative">
                <h1 class="text-3xl font-bold text-teal-400 text-center mb-6">Register</h1>
                
                <form @submit.prevent="handleRegister" class="space-y-4">
                    <div>
                        <label for="r_username" class="block text-sm font-medium text-gray-300 mb-1">New Username</label>
                        <input 
                            type="text" 
                            id="r_username" 
                            v-model="r_username" 
                            required
                            class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-teal-500 focus:border-teal-500"
                        />
                    </div>
                    <div>
                        <label for="r_password" class="block text-sm font-medium text-gray-300 mb-1">New Password</label>
                        <input 
                            type="password" id="r_password" 
                            v-model="r_password" 
                            required
                            class="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-teal-500 focus:border-teal-500"
                        />
                    </div>
                    
                    <button type="submit" class="w-full bg-teal-600 hover:bg-teal-700 text-white font-semibold py-2 rounded-lg transition duration-200 shadow-md">
                        Create Account
                    </button>
                    
                    <p v-if="r_errorMessage" class="text-sm text-red-400 text-center mt-3">{{ r_errorMessage }}</p>
                    <p v-if="r_successMessage" class="text-sm text-green-400 text-center mt-3">{{ r_successMessage }}</p>
                </form>
            </div>
            
        </div>
    </div>
</template>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
