<template>
  <div class="min-h-screen bg-dark-base flex items-center justify-center p-4">
    <div class="max-w-2xl w-full text-center animate-fade-in-up">
      <!-- Success Icon -->
      <div class="mb-8">
        <div class="text-8xl text-tech-green mb-4 animate-pulse-glow">✓</div>
        <h1 class="text-4xl font-bold text-tech-green font-display mb-2">
          SESSION_COMPLETE
        </h1>
        <p class="text-sm text-tech-cyan font-body">
          // Thank you for your time and effort
        </p>
      </div>

      <!-- Thank You Message -->
      <div class="border-2 border-tech-green p-8 bg-dark-elevated mb-6">
        <h2 class="text-2xl font-bold text-light-base font-display mb-4">
          Thank You, {{ candidateName }}!
        </h2>
        <p class="text-base text-light-base font-body leading-relaxed mb-4">
          Your coding session has been completed successfully. The interviewer has received your solutions and will review them shortly.
        </p>
        <p class="text-sm text-tech-cyan font-body italic">
          We appreciate your participation and wish you the best of luck!
        </p>
      </div>

      <!-- Wise Quote -->
      <div class="border-2 border-dark-border p-6 bg-dark-elevated">
        <p class="text-xs text-tech-cyan font-body mb-2">// Wise Words</p>
        <blockquote class="text-lg text-light-base font-body italic leading-relaxed mb-3">
          "{{ randomQuote.text }}"
        </blockquote>
        <p class="text-sm text-tech-orange font-display">
          — {{ randomQuote.author }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSessionStore } from '../stores/session'

const sessionStore = useSessionStore()

// Wise quotes collection
const quotes = [
  {
    text: "The only way to do great work is to love what you do.",
    author: "Steve Jobs"
  },
  {
    text: "Code is like humor. When you have to explain it, it's bad.",
    author: "Cory House"
  },
  {
    text: "First, solve the problem. Then, write the code.",
    author: "John Johnson"
  },
  {
    text: "Experience is the name everyone gives to their mistakes.",
    author: "Oscar Wilde"
  },
  {
    text: "In order to be irreplaceable, one must always be different.",
    author: "Coco Chanel"
  },
  {
    text: "Simplicity is the soul of efficiency.",
    author: "Austin Freeman"
  },
  {
    text: "Make it work, make it right, make it fast.",
    author: "Kent Beck"
  },
  {
    text: "The best error message is the one that never shows up.",
    author: "Thomas Fuchs"
  },
  {
    text: "Programming isn't about what you know; it's about what you can figure out.",
    author: "Chris Pine"
  },
  {
    text: "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
    author: "Martin Fowler"
  },
  {
    text: "It's not a bug – it's an undocumented feature.",
    author: "Anonymous"
  },
  {
    text: "Testing leads to failure, and failure leads to understanding.",
    author: "Burt Rutan"
  },
  {
    text: "The function of good software is to make the complex appear to be simple.",
    author: "Grady Booch"
  },
  {
    text: "Walking on water and developing software from a specification are easy if both are frozen.",
    author: "Edward V. Berard"
  },
  {
    text: "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.",
    author: "Antoine de Saint-Exupery"
  }
]

// Random quote
const randomQuote = ref({})

// Get candidate name
const candidateName = computed(() => {
  return sessionStore.currentSession?.candidate?.name || 'Candidate'
})

// Select random quote on mount
onMounted(() => {
  randomQuote.value = quotes[Math.floor(Math.random() * quotes.length)]
})
</script>

<style scoped>
/* Additional animations */
@keyframes pulse-glow {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.animate-pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}
</style>
