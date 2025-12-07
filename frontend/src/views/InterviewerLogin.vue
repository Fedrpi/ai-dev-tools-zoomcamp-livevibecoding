<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-dark-base">
    <div class="max-w-md w-full animate-fade-in-up">
      <h1 class="text-4xl font-bold mb-8 font-display text-light-base">
        <span class="text-tech-green">&gt;</span> LiveCoding<span class="text-tech-orange">Interview</span>
      </h1>
      <p class="text-sm mb-8 text-tech-cyan">// Interviewer Login</p>
      <div class="space-y-4">
        <div>
          <input
            v-model="fullName"
            type="text"
            placeholder="Enter your full name"
            class="w-full px-4 py-3 bg-transparent border-2 border-dark-border text-light-base outline-none focus:border-tech-green transition-colors font-body"
            @keyup.enter="handleLogin"
          />
          <p v-if="error" class="text-tech-orange text-xs mt-2 font-body">{{ error }}</p>
        </div>
        <button
          @click="handleLogin"
          :disabled="loading"
          class="w-full px-6 py-3 font-bold bg-tech-green text-dark-base font-display transition-all hover:bg-tech-cyan uppercase disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'LOADING...' : 'START_SESSION()' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '../stores/session'

const router = useRouter()
const sessionStore = useSessionStore()

const fullName = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''

  // Validation
  if (!fullName.value.trim()) {
    error.value = '// Error: Name is required'
    return
  }

  if (fullName.value.trim().length < 3) {
    error.value = '// Error: Name must be at least 3 characters'
    return
  }

  loading.value = true

  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500))

  // Save user to store
  sessionStore.setUser({
    name: fullName.value.trim(),
    role: 'interviewer'
  })

  // Navigate to setup
  router.push('/setup')
}
</script>
