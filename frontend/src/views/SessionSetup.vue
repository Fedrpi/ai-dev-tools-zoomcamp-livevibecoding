<template>
  <div class="min-h-screen bg-dark-base p-8">
    <div class="max-w-3xl mx-auto animate-fade-in-up">
      <!-- Header -->
      <div class="mb-12">
        <h1 class="text-4xl font-bold mb-2 font-display text-light-base">
          <span class="text-tech-green">&lt;/&gt;</span> Session Setup
        </h1>
        <p class="text-sm text-tech-cyan font-body">// Configure your coding interview session</p>
        <p class="text-sm text-light-base mt-4 font-body">
          Welcome, <span class="text-tech-orange">{{ sessionStore.currentUser?.name }}</span>
        </p>
      </div>

      <!-- Configuration Form -->
      <div class="space-y-8">
        <!-- Difficulty Level -->
        <div class="border-2 border-dark-border p-6 transition-colors hover:border-tech-green">
          <label class="block text-sm font-bold mb-4 text-tech-cyan font-display uppercase">
            SELECT_DIFFICULTY:
          </label>
          <div class="grid grid-cols-3 gap-4">
            <button
              v-for="level in difficulties"
              :key="level.value"
              @click="selectedDifficulty = level.value"
              :class="[
                'p-4 border-2 transition-all font-display uppercase',
                selectedDifficulty === level.value
                  ? 'border-tech-green bg-tech-green/10 text-tech-green'
                  : 'border-dark-border text-light-base hover:border-tech-cyan'
              ]"
            >
              {{ level.label }}
            </button>
          </div>
        </div>

        <!-- Language -->
        <div class="border-2 border-dark-border p-6 transition-colors hover:border-tech-green">
          <label class="block text-sm font-bold mb-4 text-tech-cyan font-display uppercase">
            SELECT_LANGUAGE:
          </label>
          <div class="grid grid-cols-3 gap-4">
            <button
              v-for="lang in languages"
              :key="lang.value"
              @click="selectedLanguage = lang.value"
              :class="[
                'p-4 border-2 transition-all font-display uppercase',
                selectedLanguage === lang.value
                  ? 'border-tech-green bg-tech-green/10 text-tech-green'
                  : 'border-dark-border text-light-base hover:border-tech-cyan'
              ]"
              :disabled="!lang.available"
            >
              {{ lang.label }}
              <span v-if="!lang.available" class="text-xs block mt-1 text-tech-orange">
                // Coming Soon
              </span>
            </button>
          </div>
        </div>

        <!-- Number of Problems -->
        <div class="border-2 border-dark-border p-6 transition-colors hover:border-tech-green">
          <label class="block text-sm font-bold mb-4 text-tech-cyan font-display uppercase">
            NUMBER_OF_PROBLEMS:
          </label>
          <div class="flex items-center gap-4">
            <input
              v-model.number="numberOfProblems"
              type="range"
              min="1"
              max="5"
              class="flex-1 h-2 bg-dark-elevated appearance-none outline-none"
              style="accent-color: var(--color-tech-green)"
            />
            <span class="text-3xl font-bold text-tech-green font-display w-16 text-center">
              {{ numberOfProblems }}
            </span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-4">
          <button
            @click="router.push('/')"
            class="px-8 py-4 border-2 border-dark-border text-light-base font-display uppercase transition-all hover:border-tech-orange hover:text-tech-orange"
          >
            &lt; BACK
          </button>
          <button
            @click="createSession"
            :disabled="loading"
            class="flex-1 px-8 py-4 bg-tech-green text-dark-base font-display uppercase transition-all hover:bg-tech-cyan disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'CREATING...' : 'CREATE_SESSION()' }}
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="border-2 border-tech-orange bg-tech-orange/10 p-4">
          <p class="text-tech-orange font-body text-sm">
            <span class="font-bold">ERROR:</span> {{ error }}
          </p>
        </div>
      </div>

      <!-- Session Link Modal -->
      <div
        v-if="showLinkModal"
        class="fixed inset-0 bg-dark-base/90 flex items-center justify-center p-4 z-50"
        @click.self="showLinkModal = false"
      >
        <div class="max-w-2xl w-full bg-dark-elevated border-2 border-tech-green p-8 animate-fade-in-up">
          <h2 class="text-2xl font-bold mb-4 text-tech-green font-display">
            // SESSION_CREATED
          </h2>
          <p class="text-sm text-light-base mb-6 font-body">
            Share this link with the candidate:
          </p>
          <div class="flex gap-2 mb-6">
            <input
              :value="sessionLink"
              readonly
              class="flex-1 px-4 py-3 bg-dark-base border-2 border-dark-border text-tech-cyan font-body text-sm"
            />
            <button
              @click="copyLink"
              class="px-6 py-3 bg-tech-cyan text-dark-base font-display uppercase transition-all hover:bg-tech-green"
            >
              {{ copied ? 'COPIED!' : 'COPY' }}
            </button>
          </div>
          <button
            @click="startSession"
            class="w-full px-8 py-4 bg-tech-green text-dark-base font-display uppercase transition-all hover:bg-tech-orange"
          >
            START_SESSION() &gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '../stores/session'
import { api } from '../services/api'

const router = useRouter()
const sessionStore = useSessionStore()

// Form data
const selectedDifficulty = ref('junior')
const selectedLanguage = ref('python')
const numberOfProblems = ref(3)

const difficulties = [
  { label: 'Junior', value: 'junior' },
  { label: 'Middle', value: 'middle' },
  { label: 'Senior', value: 'senior' }
]

const languages = [
  { label: 'Python', value: 'python', available: true },
  { label: 'JavaScript', value: 'javascript', available: false },
  { label: 'Java', value: 'java', available: false }
]

// Modal
const showLinkModal = ref(false)
const sessionLink = ref('')
const loading = ref(false)
const copied = ref(false)
const error = ref(null)

const createSession = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.sessions.create({
      interviewerName: sessionStore.currentUser?.name || 'Unknown',
      difficulty: selectedDifficulty.value,
      language: selectedLanguage.value,
      numberOfProblems: numberOfProblems.value,
    })

    const { session, linkCode } = response

    sessionLink.value = `${window.location.origin}/join/${linkCode}`

    sessionStore.setSession(session)

    showLinkModal.value = true
  } catch (err) {
    console.error('Failed to create session:', err)
    error.value = err.response?.data?.detail?.message || 'Failed to create session. Please try again.'
  } finally {
    loading.value = false
  }
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(sessionLink.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

const startSession = () => {
  const sessionId = sessionStore.currentSession.id
  router.push(`/session/${sessionId}/interviewer`)
}
</script>
