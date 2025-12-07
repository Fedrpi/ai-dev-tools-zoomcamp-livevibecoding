<template>
  <div class="min-h-screen bg-dark-base">
    <!-- Header -->
    <div class="border-b-2 border-dark-border px-8 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-tech-green font-display">
            &lt; INTERVIEWER_VIEW /&gt;
          </h1>
          <p class="text-xs text-tech-cyan mt-1 font-body">// Monitoring session</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-light-base font-body">
            Candidate: <span class="text-tech-orange font-bold">{{ candidateName }}</span>
          </p>
          <p class="text-xs text-tech-cyan font-body mt-1">
            {{ progressText }}
          </p>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto p-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Code Editor (Read-only for interviewer) -->
        <div class="lg:col-span-2 space-y-4">
          <div class="border-2 border-dark-border p-4 bg-dark-elevated">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm font-bold text-tech-cyan font-display uppercase">
                CANDIDATE_CODE:
              </h2>
              <span class="text-xs text-tech-yellow font-body animate-pulse-glow">
                ● LIVE
              </span>
            </div>
            <div class="bg-dark-base border-2 border-dark-border p-4 font-code text-sm text-light-base min-h-[400px] overflow-auto">
              <pre v-if="currentCode"><code class="language-python" :ref="el => codeElement = el">{{ currentCode }}</code></pre>
              <pre v-else class="text-tech-cyan">// Waiting for candidate to start coding...</pre>
            </div>
          </div>

          <!-- Execution Results -->
          <div v-if="executionResult" class="border-2 border-tech-green p-4 bg-dark-elevated">
            <h3 class="text-sm font-bold text-tech-green font-display uppercase mb-3">
              EXECUTION_RESULT:
            </h3>
            <div class="bg-dark-base border-2 border-dark-border p-4 font-code text-sm">
              <pre class="text-tech-green whitespace-pre-wrap">{{ executionResult }}</pre>
            </div>
          </div>
        </div>

        <!-- Right Column: Problem Description & Controls -->
        <div class="space-y-4">
          <!-- Progress Indicator -->
          <div class="border-2 border-tech-orange p-4 bg-dark-elevated">
            <p class="text-xs text-tech-cyan font-body mb-2">// Progress</p>
            <p class="text-3xl font-bold text-tech-orange font-display">
              {{ currentProblemIndex + 1 }} / {{ totalProblems }}
            </p>
            <div class="mt-3 h-2 bg-dark-base">
              <div
                class="h-full bg-tech-orange transition-all duration-300"
                :style="{ width: `${((currentProblemIndex + 1) / totalProblems) * 100}%` }"
              ></div>
            </div>
          </div>

          <!-- Current Problem -->
          <div class="border-2 border-tech-green p-4 bg-dark-elevated">
            <div class="mb-4">
              <div class="flex items-center gap-2 mb-2">
                <span
                  class="text-xs px-2 py-1 border-2 font-display uppercase"
                  :class="{
                    'border-tech-green text-tech-green': currentProblem?.difficulty === 'junior',
                    'border-tech-cyan text-tech-cyan': currentProblem?.difficulty === 'middle',
                    'border-tech-orange text-tech-orange': currentProblem?.difficulty === 'senior'
                  }"
                >
                  {{ currentProblem?.difficulty }}
                </span>
              </div>
              <h2 class="text-xl font-bold text-tech-green font-display mb-3">
                {{ currentProblem?.title }}
              </h2>
            </div>

            <div class="text-sm text-light-base font-body space-y-3">
              <p class="text-xs text-tech-cyan mb-2">// Problem Description:</p>
              <pre class="whitespace-pre-wrap text-sm">{{ currentProblem?.description }}</pre>
            </div>
          </div>

          <!-- Controls -->
          <div class="space-y-3">
            <button
              v-if="currentProblemIndex < totalProblems - 1"
              @click="nextProblem"
              class="w-full px-6 py-3 border-2 border-tech-cyan text-tech-cyan font-display uppercase transition-all hover:bg-tech-cyan hover:text-dark-base"
            >
              NEXT_TASK() &gt;
            </button>
            <button
              v-else
              @click="endSession"
              class="w-full px-6 py-3 bg-tech-orange text-dark-base font-display uppercase transition-all hover:bg-tech-yellow"
            >
              END_SESSION()
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSessionStore } from '../stores/session'
import { api } from '../services/api'
import { wsService } from '../services/websocket'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-python'

const router = useRouter()
const route = useRoute()
const sessionStore = useSessionStore()

// Reactive data
const codeElement = ref(null)
const loading = ref(true)
const error = ref(null)

// Computed properties - sync from store
const candidateName = computed(() => {
  return sessionStore.currentSession?.candidate?.name || 'Waiting for candidate...'
})

const currentProblem = computed(() => {
  const problems = sessionStore.currentSession?.problems || []
  return problems[sessionStore.currentProblemIndex] || null
})

const currentProblemIndex = computed(() => sessionStore.currentProblemIndex)
const totalProblems = computed(() => sessionStore.currentSession?.problems?.length || 0)

const progressText = computed(() => {
  return `Task ${currentProblemIndex.value + 1} of ${totalProblems.value}`
})

// Real-time synced data from candidate
const currentCode = computed(() => sessionStore.candidateCode || '# Waiting for candidate to start coding...')
const executionResult = computed(() => {
  const result = sessionStore.executionResult
  if (!result) return ''
  return result.output || ''
})

// Methods
const nextProblem = () => {
  sessionStore.nextProblem()

  // Broadcast problem change via WebSocket
  const newIndex = sessionStore.currentProblemIndex
  const newProblem = sessionStore.currentSession?.problems?.[newIndex]
  if (newProblem) {
    wsService.sendProblemChange(newIndex, newProblem.id)
  }
}

const endSession = async () => {
  try {
    sessionStore.endSession()

    const sessionId = route.params.id
    await api.sessions.end(sessionId)

    wsService.disconnect()

    router.push(`/session/${sessionId}/evaluate`)
  } catch (err) {
    console.error('Failed to end session:', err)
    error.value = 'Failed to end session'
  }
}

// Highlight code with Prism
const highlightCode = () => {
  nextTick(() => {
    if (codeElement.value) {
      Prism.highlightElement(codeElement.value)
    }
  })
}

// Watch for code changes and re-highlight
watch(currentCode, () => {
  highlightCode()
})

// Initialize
onMounted(async () => {
  const sessionId = route.params.id

  try {
    const response = await api.sessions.getById(sessionId)
    sessionStore.setSession(response.session)

    const userName = sessionStore.currentUser?.name || 'Interviewer'
    wsService.connect(sessionId, userName, 'interviewer')

    wsService.on('code_update', (message) => {
      sessionStore.updateCode(message.code)
    })

    wsService.on('user_joined', (message) => {
      if (message.role === 'candidate' && sessionStore.currentSession) {
        sessionStore.currentSession.candidate = {
          name: message.userName,
          role: 'candidate'
        }
      }
    })

    loading.value = false
    highlightCode()
  } catch (err) {
    console.error('Failed to load session:', err)
    error.value = 'Failed to load session'
    loading.value = false
  }
})

onUnmounted(() => {
  wsService.disconnect()
})
</script>

<style>
/* Override Prism theme for our color scheme */
pre[class*="language-"] {
  background: transparent !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.875rem !important;
  line-height: 1.5 !important;
}

code[class*="language-"] {
  background: transparent !important;
  color: #f5f5f0 !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* Custom colors for Python syntax */
.token.comment {
  color: #00d9ff !important;
  font-style: italic !important;
}

.token.keyword {
  color: #ff6b35 !important;
  font-weight: bold !important;
}

.token.string {
  color: #00ff41 !important;
}

.token.number {
  color: #ffdd00 !important;
}

.token.function {
  color: #ffdd00 !important;
}

.token.builtin,
.token.class-name {
  color: #00d9ff !important;
}

.token.operator {
  color: #ff6b35 !important;
}
</style>
