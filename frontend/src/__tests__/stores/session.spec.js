import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useSessionStore } from '../../stores/session'

describe('Session Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance before each test
    setActivePinia(createPinia())
    // Clear localStorage
    localStorage.clear()
    // Clear all mocks
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const store = useSessionStore()

      expect(store.currentUser).toBeNull()
      expect(store.currentSession).toBeNull()
      expect(store.sessionLink).toBeNull()
      expect(store.currentProblemIndex).toBe(0)
      expect(store.candidateCode).toBe('')
      expect(store.executionResult).toBeNull()
      expect(store.sessionEnded).toBe(false)
    })
  })

  describe('setUser', () => {
    it('should set user correctly', () => {
      const store = useSessionStore()
      const user = { name: 'John Doe', role: 'interviewer' }

      store.setUser(user)

      expect(store.currentUser).toEqual(user)
    })

    it('should save to localStorage', () => {
      const store = useSessionStore()
      const user = { name: 'John Doe', role: 'interviewer' }

      store.setUser(user)

      const stored = JSON.parse(localStorage.getItem('livecoding_session'))
      expect(stored.currentUser).toEqual(user)
    })
  })

  describe('setSession', () => {
    it('should set session correctly', () => {
      const store = useSessionStore()
      const session = {
        id: 'test123',
        difficulty: 'junior',
        language: 'python',
        problems: []
      }

      store.setSession(session)

      expect(store.currentSession).toEqual(session)
    })

    it('should reset currentProblemIndex to 0 when setting new session', () => {
      const store = useSessionStore()

      // First session - move to problem 2
      const session1 = {
        id: 'session1',
        difficulty: 'junior',
        language: 'python',
        problems: [{ id: 1 }, { id: 2 }, { id: 3 }]
      }
      store.setSession(session1)
      store.nextProblem()
      store.nextProblem()
      expect(store.currentProblemIndex).toBe(2)

      // Create new session - should reset to 0
      const session2 = {
        id: 'session2',
        difficulty: 'middle',
        language: 'python',
        problems: [{ id: 4 }, { id: 5 }, { id: 6 }]
      }
      store.setSession(session2)

      expect(store.currentProblemIndex).toBe(0)
      expect(store.candidateCode).toBe('')
      expect(store.executionResult).toBeNull()
      expect(store.sessionEnded).toBe(false)
    })
  })

  describe('updateCode', () => {
    it('should update candidate code', () => {
      const store = useSessionStore()
      const code = 'print("Hello World")'

      store.updateCode(code)

      expect(store.candidateCode).toBe(code)
    })
  })

  describe('setExecutionResult', () => {
    it('should set execution result', () => {
      const store = useSessionStore()
      const result = { success: true, output: 'Hello World' }

      store.setExecutionResult(result)

      expect(store.executionResult).toEqual(result)
    })
  })

  describe('nextProblem', () => {
    it('should increment problem index', () => {
      const store = useSessionStore()
      store.setSession({
        problems: [{}, {}, {}]
      })

      store.nextProblem()

      expect(store.currentProblemIndex).toBe(1)
    })

    it('should clear code and execution result', () => {
      const store = useSessionStore()
      store.setSession({
        problems: [{}, {}, {}]
      })
      store.updateCode('some code')
      store.setExecutionResult({ success: true, output: 'test' })

      store.nextProblem()

      expect(store.candidateCode).toBe('')
      expect(store.executionResult).toBeNull()
    })

    it('should not increment beyond total problems', () => {
      const store = useSessionStore()
      store.setSession({
        problems: [{}]
      })

      store.nextProblem()

      expect(store.currentProblemIndex).toBe(0)
    })
  })

  describe('endSession', () => {
    it('should set sessionEnded to true', () => {
      const store = useSessionStore()

      store.endSession()

      expect(store.sessionEnded).toBe(true)
    })

    it('should save to localStorage', () => {
      const store = useSessionStore()

      store.endSession()

      const stored = JSON.parse(localStorage.getItem('livecoding_session'))
      expect(stored.sessionEnded).toBe(true)
    })
  })

  describe('reset', () => {
    it('should reset all state', () => {
      const store = useSessionStore()

      // Set some data
      store.setUser({ name: 'Test', role: 'candidate' })
      store.updateCode('test code')
      store.endSession()

      // Reset
      store.reset()

      // Check all values are reset
      expect(store.currentUser).toBeNull()
      expect(store.currentSession).toBeNull()
      expect(store.sessionLink).toBeNull()
      expect(store.currentProblemIndex).toBe(0)
      expect(store.candidateCode).toBe('')
      expect(store.executionResult).toBeNull()
      expect(store.sessionEnded).toBe(false)
    })

    it('should clear localStorage', () => {
      const store = useSessionStore()
      store.setUser({ name: 'Test' })

      store.reset()

      expect(localStorage.getItem('livecoding_session')).toBeNull()
    })
  })

  describe('Computed Properties', () => {
    it('should compute isInterviewer correctly', () => {
      const store = useSessionStore()

      store.setUser({ name: 'Test', role: 'interviewer' })
      expect(store.isInterviewer).toBe(true)

      store.setUser({ name: 'Test', role: 'candidate' })
      expect(store.isInterviewer).toBe(false)
    })

    it('should compute isCandidate correctly', () => {
      const store = useSessionStore()

      store.setUser({ name: 'Test', role: 'candidate' })
      expect(store.isCandidate).toBe(true)

      store.setUser({ name: 'Test', role: 'interviewer' })
      expect(store.isCandidate).toBe(false)
    })

    it('should compute currentProblem correctly', () => {
      const store = useSessionStore()
      const problems = [
        { id: 1, title: 'Problem 1' },
        { id: 2, title: 'Problem 2' }
      ]

      store.setSession({ problems })

      expect(store.currentProblem).toEqual(problems[0])

      store.nextProblem()

      expect(store.currentProblem).toEqual(problems[1])
    })

    it('should compute totalProblems correctly', () => {
      const store = useSessionStore()

      expect(store.totalProblems).toBe(0)

      store.setSession({ problems: [{}, {}, {}] })

      expect(store.totalProblems).toBe(3)
    })

    it('should compute progressText correctly', () => {
      const store = useSessionStore()
      store.setSession({ problems: [{}, {}, {}] })

      expect(store.progressText).toBe('Task 1 of 3')

      store.nextProblem()

      expect(store.progressText).toBe('Task 2 of 3')
    })
  })

  describe('localStorage Sync', () => {
    it('should load from localStorage on init', () => {
      const data = {
        currentUser: { name: 'Test', role: 'interviewer' },
        currentProblemIndex: 2,
        candidateCode: 'test code',
        sessionEnded: false
      }
      localStorage.setItem('livecoding_session', JSON.stringify(data))

      // Create new store (will trigger loadFromStorage)
      setActivePinia(createPinia())
      const store = useSessionStore()

      expect(store.currentUser).toEqual(data.currentUser)
      expect(store.currentProblemIndex).toBe(data.currentProblemIndex)
      expect(store.candidateCode).toBe(data.candidateCode)
    })
  })
})
