<template>
  <div class="min-h-screen bg-dark-base flex items-center justify-center p-4">
    <div class="max-w-lg w-full animate-fade-in-up">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-4 font-display text-light-base">
          <span class="text-tech-cyan">&lt;</span> Join Interview
        </h1>
        <p class="text-sm text-tech-cyan font-body mb-6">
          // You have been invited to a coding interview
        </p>
      </div>

      <!-- Interviewer Info Card -->
      <div class="border-2 border-tech-green p-6 bg-dark-elevated mb-6">
        <p class="text-xs text-tech-cyan font-body mb-2">// Interviewer</p>
        <p class="text-2xl font-bold text-tech-green font-display">
          {{ interviewerName }}
        </p>
        <div class="mt-4 pt-4 border-t-2 border-dark-border">
          <p class="text-xs text-tech-cyan font-body mb-1">// Session Details</p>
          <p class="text-sm text-light-base font-body">
            Difficulty: <span class="text-tech-orange">{{ sessionInfo.difficulty }}</span>
          </p>
          <p class="text-sm text-light-base font-body">
            Problems: <span class="text-tech-yellow">{{ sessionInfo.numberOfProblems }}</span>
          </p>
          <p class="text-sm text-light-base font-body">
            Language: <span class="text-tech-green">{{ sessionInfo.language }}</span>
          </p>
        </div>
      </div>

      <!-- Join Form -->
      <div class="border-2 border-dark-border p-6 bg-dark-elevated">
        <label class="block text-sm font-bold text-tech-cyan font-display uppercase mb-3">
          ENTER_YOUR_NAME:
        </label>
        <div class="space-y-4">
          <div>
            <input
              v-model="candidateName"
              type="text"
              placeholder="Your full name"
              class="w-full px-4 py-3 bg-dark-base border-2 border-dark-border text-light-base font-body outline-none focus:border-tech-cyan transition-colors"
              @keyup.enter="joinSession"
            />
            <p v-if="error" class="text-tech-orange text-xs mt-2 font-body">{{ error }}</p>
          </div>
          <button
            @click="joinSession"
            :disabled="loading"
            class="w-full px-6 py-4 bg-tech-cyan text-dark-base font-display uppercase transition-all hover:bg-tech-green disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'JOINING...' : 'JOIN_SESSION() >' }}
          </button>
        </div>
      </div>

      <!-- Info -->
      <div class="mt-6 text-center">
        <p class="text-xs text-tech-cyan font-body italic">
          // Make sure you have a stable internet connection
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSessionStore } from '../stores/session'
import { api } from '../services/api'

const router = useRouter()
const route = useRoute()
const sessionStore = useSessionStore()

const candidateName = ref('')
const error = ref('')
const loading = ref(false)
const loadingSession = ref(true)
const interviewerName = ref('Loading...')
const sessionInfo = ref({
  id: null,
  difficulty: 'junior',
  numberOfProblems: 3,
  language: 'Python'
})

const joinSession = async () => {
  error.value = ''

  if (!candidateName.value.trim()) {
    error.value = '// Error: Name is required'
    return
  }

  if (candidateName.value.trim().length < 3) {
    error.value = '// Error: Name must be at least 3 characters'
    return
  }

  if (!sessionInfo.value.id) {
    error.value = '// Error: Session not found'
    return
  }

  loading.value = true

  try {
    const response = await api.sessions.join(
      sessionInfo.value.id,
      candidateName.value.trim()
    )

    sessionStore.setUser({
      name: candidateName.value.trim(),
      role: 'candidate'
    })

    sessionStore.setSession(response.session)

    router.push(`/session/${sessionInfo.value.id}/candidate`)
  } catch (err) {
    console.error('Failed to join session:', err)
    error.value = err.response?.data?.detail?.message || '// Error: Failed to join session'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const linkCode = route.params.link

  if (!linkCode) {
    error.value = '// Error: Invalid link'
    loadingSession.value = false
    return
  }

  try {
    const response = await api.sessions.getByLink(linkCode)
    const { session } = response

    sessionInfo.value = {
      id: session.id,
      difficulty: session.difficulty,
      numberOfProblems: session.numberOfProblems,
      language: session.language
    }

    interviewerName.value = session.interviewer.name
  } catch (err) {
    console.error('Failed to load session:', err)
    error.value = err.response?.data?.detail?.message || '// Error: Session not found'
    interviewerName.value = 'Unknown'
  } finally {
    loadingSession.value = false
  }
})
</script>
