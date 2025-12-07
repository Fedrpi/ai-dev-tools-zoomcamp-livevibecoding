import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'livecoding_session'

export const useSessionStore = defineStore('session', () => {
  // State
  const currentUser = ref(null)
  const currentSession = ref(null)
  const sessionLink = ref(null)
  const currentProblemIndex = ref(0)
  const candidateCode = ref('')
  const executionResult = ref(null)
  const sessionEnded = ref(false)

  // Load initial state from localStorage
  const loadFromStorage = () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const data = JSON.parse(stored)
        if (data.currentSession) currentSession.value = data.currentSession
        if (data.currentUser) currentUser.value = data.currentUser
        if (data.currentProblemIndex !== undefined) currentProblemIndex.value = data.currentProblemIndex
        if (data.candidateCode !== undefined) candidateCode.value = data.candidateCode
        if (data.executionResult !== undefined) executionResult.value = data.executionResult
        if (data.sessionEnded !== undefined) sessionEnded.value = data.sessionEnded
        console.log('Session loaded from localStorage')
      }
    } catch (error) {
      console.error('Failed to load session from localStorage:', error)
    }
  }

  // Save state to localStorage
  const saveToStorage = () => {
    try {
      const data = {
        currentSession: currentSession.value,
        currentUser: currentUser.value,
        currentProblemIndex: currentProblemIndex.value,
        candidateCode: candidateCode.value,
        executionResult: executionResult.value,
        sessionEnded: sessionEnded.value,
        timestamp: Date.now()
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data))

      // Trigger storage event manually for same-window updates
      window.dispatchEvent(new StorageEvent('storage', {
        key: STORAGE_KEY,
        newValue: JSON.stringify(data),
        url: window.location.href
      }))
    } catch (error) {
      console.error('Failed to save session to localStorage:', error)
    }
  }

  // Listen for storage events from other tabs
  const setupStorageListener = () => {
    window.addEventListener('storage', (event) => {
      if (event.key === STORAGE_KEY && event.newValue) {
        try {
          const data = JSON.parse(event.newValue)
          console.log('Session updated from another tab')

          // Update state without triggering watchers again
          if (data.currentSession) currentSession.value = data.currentSession
          if (data.currentProblemIndex !== undefined) currentProblemIndex.value = data.currentProblemIndex
          if (data.candidateCode !== undefined) candidateCode.value = data.candidateCode
          if (data.executionResult !== undefined) executionResult.value = data.executionResult
          if (data.sessionEnded !== undefined) sessionEnded.value = data.sessionEnded
        } catch (error) {
          console.error('Failed to parse storage event:', error)
        }
      }
    })
  }

  // Initialize
  loadFromStorage()
  setupStorageListener()

  // Getters
  const isInterviewer = computed(() => currentUser.value?.role === 'interviewer')
  const isCandidate = computed(() => currentUser.value?.role === 'candidate')
  const currentProblem = computed(() => {
    if (!currentSession.value?.problems) return null
    return currentSession.value.problems[currentProblemIndex.value]
  })
  const totalProblems = computed(() => currentSession.value?.problems?.length || 0)
  const progressText = computed(() => {
    if (!currentSession.value) return ''
    return `Task ${currentProblemIndex.value + 1} of ${totalProblems.value}`
  })

  // Actions
  function setUser(user) {
    currentUser.value = user
    saveToStorage()
  }

  function setSession(session) {
    currentSession.value = session
    // Reset to first problem when starting a new session
    currentProblemIndex.value = 0
    candidateCode.value = ''
    executionResult.value = null
    sessionEnded.value = false
    saveToStorage()
  }

  function setSessionLink(link) {
    sessionLink.value = link
    // Don't save link to storage, it's temporary
  }

  function updateCode(code) {
    candidateCode.value = code
    saveToStorage()
  }

  function setExecutionResult(result) {
    executionResult.value = result
    saveToStorage()
  }

  function nextProblem() {
    if (currentProblemIndex.value < totalProblems.value - 1) {
      currentProblemIndex.value++
      candidateCode.value = ''
      executionResult.value = null
      saveToStorage()
    }
  }

  function endSession() {
    sessionEnded.value = true
    saveToStorage()
  }

  function reset() {
    currentUser.value = null
    currentSession.value = null
    sessionLink.value = null
    currentProblemIndex.value = 0
    candidateCode.value = ''
    executionResult.value = null
    sessionEnded.value = false
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    // State
    currentUser,
    currentSession,
    sessionLink,
    currentProblemIndex,
    candidateCode,
    executionResult,
    sessionEnded,
    // Getters
    isInterviewer,
    isCandidate,
    currentProblem,
    totalProblems,
    progressText,
    // Actions
    setUser,
    setSession,
    setSessionLink,
    updateCode,
    setExecutionResult,
    nextProblem,
    endSession,
    reset
  }
})
