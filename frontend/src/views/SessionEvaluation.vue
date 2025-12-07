<template>
  <div class="min-h-screen bg-dark-base">
    <!-- Header -->
    <div class="border-b-2 border-dark-border px-8 py-4">
      <div class="max-w-5xl mx-auto">
        <h1 class="text-3xl font-bold text-tech-orange font-display">
          &lt;/ SESSION_EVALUATION &gt;
        </h1>
        <p class="text-sm text-tech-cyan font-body mt-2">
          // Rate candidate's performance on each task
        </p>
        <p class="text-sm text-light-base font-body mt-2">
          Candidate: <span class="text-tech-green font-bold">{{ candidateName }}</span>
        </p>
      </div>
    </div>

    <div class="max-w-5xl mx-auto p-8">
      <!-- Loading State -->
      <div v-if="!isLoaded" class="text-center text-tech-cyan font-body py-12">
        Loading evaluation form...
      </div>

      <!-- Evaluation Forms -->
      <div v-else class="space-y-6">
        <div
          v-for="(evaluation, index) in evaluations"
          :key="evaluation.problemId"
          class="border-2 border-dark-border bg-dark-elevated p-6 animate-fade-in-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Problem Header -->
          <div class="mb-4 pb-4 border-b-2 border-dark-border">
            <div class="flex items-center justify-between mb-2">
              <h2 class="text-xl font-bold text-tech-green font-display">
                Task {{ index + 1 }}: {{ evaluation.problem.title }}
              </h2>
              <span
                class="text-xs px-3 py-1 border-2 font-display uppercase"
                :class="{
                  'border-tech-green text-tech-green': evaluation.problem.difficulty === 'junior',
                  'border-tech-cyan text-tech-cyan': evaluation.problem.difficulty === 'middle',
                  'border-tech-orange text-tech-orange': evaluation.problem.difficulty === 'senior'
                }"
              >
                {{ evaluation.problem.difficulty }}
              </span>
            </div>
            <p class="text-xs text-tech-cyan font-body">{{ evaluation.problem.description.split('\n')[0] }}</p>
          </div>

          <!-- Candidate's Code -->
          <div class="mb-6">
            <h3 class="text-sm font-bold text-tech-cyan font-display uppercase mb-3">
              CANDIDATE_CODE:
            </h3>
            <div class="bg-dark-base border-2 border-dark-border p-4 overflow-auto max-h-64">
              <pre><code class="language-python" :ref="el => { if (el) codeRefs[index] = el }">{{ evaluation.candidateCode }}</code></pre>
            </div>
          </div>

          <!-- Rating -->
          <div class="mb-6">
            <label class="block text-sm font-bold text-tech-cyan font-display uppercase mb-3">
              RATING:
            </label>
            <div class="flex items-center gap-2">
              <button
                v-for="star in 5"
                :key="star"
                @click="evaluation.rating = star"
                class="text-3xl transition-all hover:scale-110 cursor-pointer"
                :class="star <= evaluation.rating ? 'text-tech-yellow' : 'text-dark-border'"
                type="button"
              >
                {{ star <= evaluation.rating ? '★' : '☆' }}
              </button>
              <span class="ml-4 text-tech-yellow font-bold font-display text-xl">
                {{ evaluation.rating }}/5
              </span>
            </div>
          </div>

          <!-- Comment -->
          <div>
            <label class="block text-sm font-bold text-tech-cyan font-display uppercase mb-3">
              COMMENT:
            </label>
            <textarea
              v-model="evaluation.comment"
              rows="4"
              placeholder="// Add your feedback here..."
              class="w-full px-4 py-3 bg-dark-base border-2 border-dark-border text-light-base font-body text-sm outline-none focus:border-tech-green transition-colors resize-none"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <div v-if="isLoaded" class="mt-8 flex gap-4">
        <button
          @click="router.back()"
          type="button"
          class="px-8 py-4 border-2 border-dark-border text-light-base font-display uppercase transition-all hover:border-tech-orange hover:text-tech-orange"
        >
          &lt; BACK
        </button>
        <button
          @click="submitEvaluation"
          type="button"
          :disabled="!allRated || loading"
          class="flex-1 px-8 py-4 bg-tech-green text-dark-base font-display uppercase transition-all hover:bg-tech-cyan disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'SUBMITTING...' : 'SUBMIT_EVALUATION()' }}
        </button>
      </div>

      <!-- Success Message -->
      <div
        v-if="submitted"
        class="fixed inset-0 bg-dark-base/90 flex items-center justify-center p-4 z-50"
        @click.self="submitted = false"
      >
        <div class="max-w-md w-full bg-dark-elevated border-2 border-tech-green p-8 text-center animate-fade-in-up">
          <div class="text-6xl text-tech-green mb-4">✓</div>
          <h2 class="text-2xl font-bold text-tech-green font-display mb-4">
            EVALUATION_SUBMITTED
          </h2>
          <p class="text-sm text-light-base font-body mb-6">
            Your feedback has been saved successfully.
          </p>
          <button
            @click="router.push('/')"
            type="button"
            class="w-full px-8 py-4 bg-tech-green text-dark-base font-display uppercase transition-all hover:bg-tech-cyan"
          >
            NEW_SESSION() &gt;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSessionStore } from '../stores/session'
import { api } from '../services/api'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
import 'prismjs/components/prism-python'

const router = useRouter()
const route = useRoute()
const sessionStore = useSessionStore()

// Reactive data
const evaluations = ref([])
const loading = ref(false)
const submitted = ref(false)
const isLoaded = ref(false)
const codeRefs = ref([])
const error = ref(null)

// Computed
const candidateName = computed(() => sessionStore.currentSession?.candidate?.name || 'Unknown')

const allRated = computed(() => {
  return evaluations.value.length > 0 && evaluations.value.every(e => e.rating > 0)
})

// Methods
const submitEvaluation = async () => {
  loading.value = true
  error.value = null

  try {
    const sessionId = route.params.id

    const evaluationsData = evaluations.value.map(e => ({
      problemId: e.problemId,
      rating: e.rating,
      comment: e.comment,
      candidateCode: e.candidateCode
    }))

    await api.evaluations.submit(sessionId, evaluationsData)

    submitted.value = true
  } catch (err) {
    console.error('Failed to submit evaluation:', err)
    error.value = err.response?.data?.detail?.message || 'Failed to submit evaluation'
  } finally {
    loading.value = false
  }
}

// Apply Prism highlighting
const highlightCode = () => {
  nextTick(() => {
    codeRefs.value.forEach(el => {
      if (el) {
        Prism.highlightElement(el)
      }
    })
  })
}

// Initialize evaluations
onMounted(async () => {
  const sessionId = route.params.id

  try {
    const response = await api.sessions.getById(sessionId)
    const session = response.session

    sessionStore.setSession(session)

    const sessionProblems = session.problems || []

    sessionProblems.forEach((problem) => {
      const candidateCode = sessionStore.candidateCode || problem.starterCode || '# No code available'

      evaluations.value.push({
        problemId: problem.id,
        problem: problem,
        candidateCode: candidateCode,
        rating: 0,
        comment: ''
      })
    })

    isLoaded.value = true
    highlightCode()
  } catch (err) {
    console.error('Failed to load session:', err)
    error.value = 'Failed to load session'
  }
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

button:active {
  transform: scale(0.95);
}

/* Empty star outline */
.text-dark-border {
  -webkit-text-stroke: 1px #ffdd00;
  -webkit-text-fill-color: transparent;
  color: transparent !important;
}
</style>
