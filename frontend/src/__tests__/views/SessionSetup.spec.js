import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import SessionSetup from '../../views/SessionSetup.vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import { useSessionStore } from '../../stores/session'
import * as apiModule from '../../services/api'

const createMockRouter = () => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } },
      { path: '/setup', component: { template: '<div>Setup</div>' } },
      { path: '/session/:id/interviewer', component: { template: '<div>Session</div>' } }
    ]
  })
}

// Mock API
vi.mock('../../services/api', () => ({
  api: {
    sessions: {
      create: vi.fn()
    }
  }
}))

describe('SessionSetup', () => {
  let router
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    router = createMockRouter()
    store = useSessionStore()
    store.setUser({ name: 'Test Interviewer', role: 'interviewer' })
    localStorage.clear()
    vi.clearAllTimers()

    // Reset mock
    vi.clearAllMocks()

    // Setup default mock response
    apiModule.api.sessions.create.mockResolvedValue({
      session: {
        id: 'test-session-id',
        status: 'waiting',
        interviewerName: 'Test Interviewer',
        difficulty: 'junior',
        language: 'python',
        numberOfProblems: 3
      },
      linkCode: 'ABC123'
    })
  })

  const mountComponent = () => {
    return mount(SessionSetup, {
      global: {
        plugins: [router]
      }
    })
  }

  describe('Rendering', () => {
    it('should render the setup form', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('h1').text()).toContain('Session Setup')
      expect(wrapper.text()).toContain('SELECT_DIFFICULTY:')
      expect(wrapper.text()).toContain('SELECT_LANGUAGE:')
      expect(wrapper.text()).toContain('NUMBER_OF_PROBLEMS:')
    })

    it('should display interviewer name', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('Test Interviewer')
    })

    it('should render difficulty buttons', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const difficultyButtons = buttons.filter(btn =>
        ['Junior', 'Middle', 'Senior'].includes(btn.text())
      )

      expect(difficultyButtons.length).toBe(3)
    })

    it('should render language buttons', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('Python')
      expect(wrapper.text()).toContain('JavaScript')
      expect(wrapper.text()).toContain('Java')
    })

    it('should show Python as available and others as coming soon', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('// Coming Soon')
    })
  })

  describe('Difficulty Selection', () => {
    it('should have Junior selected by default', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const juniorButton = buttons.find(btn => btn.text() === 'Junior')

      expect(juniorButton.classes()).toContain('border-tech-green')
    })

    it('should change difficulty when button clicked', async () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const middleButton = buttons.find(btn => btn.text() === 'Middle')

      await middleButton.trigger('click')

      expect(middleButton.classes()).toContain('border-tech-green')
    })
  })

  describe('Language Selection', () => {
    it('should have Python selected by default', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const pythonButton = buttons.find(btn => btn.text() === 'Python')

      expect(pythonButton.classes()).toContain('border-tech-green')
    })

    it('should not allow selecting unavailable languages', async () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const jsButton = buttons.find(btn => btn.text().includes('JavaScript'))

      // Button should be disabled
      expect(jsButton.attributes('disabled')).toBeDefined()
    })
  })

  describe('Number of Problems', () => {
    it('should render slider for problem count', () => {
      const wrapper = mountComponent()
      const slider = wrapper.find('input[type="range"]')

      expect(slider.exists()).toBe(true)
      expect(slider.attributes('min')).toBe('1')
      expect(slider.attributes('max')).toBe('5')
    })

    it('should default to 3 problems', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('3')
    })

    it('should update display when slider moved', async () => {
      const wrapper = mountComponent()
      const slider = wrapper.find('input[type="range"]')

      await slider.setValue('5')

      expect(wrapper.text()).toContain('5')
    })
  })

  describe('Session Creation', () => {
    it('should show create button', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const createButton = buttons.find(btn => btn.text().includes('CREATE_SESSION'))

      expect(createButton.exists()).toBe(true)
    })

    it('should show back button', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const backButton = buttons.find(btn => btn.text().includes('BACK'))

      expect(backButton.exists()).toBe(true)
    })

    it('should navigate back when back button clicked', async () => {
      const wrapper = mountComponent()
      const pushSpy = vi.spyOn(router, 'push')

      const buttons = wrapper.findAll('button')
      const backButton = buttons.find(btn => btn.text().includes('BACK'))

      await backButton.trigger('click')

      expect(pushSpy).toHaveBeenCalledWith('/')
    })
  })

  describe('Session Link Modal', () => {
    it('should not show modal initially', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('.fixed.inset-0').exists()).toBe(false)
    })

    it('should show modal after creating session', async () => {
      vi.useFakeTimers()
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const createButton = buttons.find(btn => btn.text().includes('CREATE_SESSION'))

      await createButton.trigger('click')

      // Fast forward time for the setTimeout (800ms in createSession)
      await vi.advanceTimersByTimeAsync(1000)
      await flushPromises()
      await wrapper.vm.$nextTick()

      expect(wrapper.find('.fixed.inset-0').exists()).toBe(true)

      vi.useRealTimers()
    })
  })

  describe('Copy Link Functionality', () => {
    it('should have copy button in modal', async () => {
      vi.useFakeTimers()
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')
      const createButton = buttons.find(btn => btn.text().includes('CREATE_SESSION'))

      await createButton.trigger('click')
      await vi.advanceTimersByTimeAsync(1000)
      await flushPromises()
      await wrapper.vm.$nextTick()

      const copyButton = wrapper.findAll('button').find(btn => btn.text().includes('COPY'))
      expect(copyButton.exists()).toBe(true)

      vi.useRealTimers()
    })
  })
})
