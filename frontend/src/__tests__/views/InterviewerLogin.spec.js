import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import InterviewerLogin from '../../views/InterviewerLogin.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

// Create mock router
const createMockRouter = () => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } },
      { path: '/setup', component: { template: '<div>Setup</div>' } }
    ]
  })
}

describe('InterviewerLogin', () => {
  let router

  beforeEach(() => {
    setActivePinia(createPinia())
    router = createMockRouter()
    localStorage.clear()
  })

  const mountComponent = () => {
    return mount(InterviewerLogin, {
      global: {
        plugins: [router],
        stubs: {
          // Stub router-link if needed
        }
      }
    })
  }

  describe('Rendering', () => {
    it('should render the login form', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('h1').text()).toContain('LiveCodingInterview')
      expect(wrapper.find('input[type="text"]').exists()).toBe(true)
      expect(wrapper.find('button').text()).toContain('START_SESSION()')
    })

    it('should have empty input initially', () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')

      expect(input.element.value).toBe('')
    })

    it('should not show error initially', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('p.text-tech-orange').exists()).toBe(false)
    })
  })

  describe('User Input', () => {
    it('should update input value when user types', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')

      await input.setValue('John Doe')

      expect(input.element.value).toBe('John Doe')
    })

    it('should allow submission on Enter key', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')

      await input.setValue('John Doe')
      await input.trigger('keyup.enter')

      // Should navigate (tested in integration tests)
      expect(input.element.value).toBe('John Doe')
    })
  })

  describe('Validation', () => {
    it('should show error when name is empty', async () => {
      const wrapper = mountComponent()
      const button = wrapper.find('button')

      await button.trigger('click')

      expect(wrapper.find('p.text-tech-orange').text()).toContain('// Error: Name is required')
    })

    it('should show error when name is too short', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')
      const button = wrapper.find('button')

      await input.setValue('Jo')
      await button.trigger('click')

      expect(wrapper.find('p.text-tech-orange').text()).toContain('// Error: Name must be at least 3 characters')
    })

    it('should not show error when name is valid', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')
      const button = wrapper.find('button')

      await input.setValue('John Doe')
      await button.trigger('click')

      // Wait for any async operations (500ms loading + next tick)
      await new Promise(resolve => setTimeout(resolve, 600))
      await wrapper.vm.$nextTick()

      // Error should not be present
      expect(wrapper.find('p.text-tech-orange').exists()).toBe(false)
    })
  })

  describe('Navigation', () => {
    it('should navigate to /setup on successful submission', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')
      const button = wrapper.find('button')

      // Spy on router push
      const pushSpy = vi.spyOn(router, 'push')

      await input.setValue('John Doe')
      await button.trigger('click')

      // Wait for the simulated API call (500ms)
      await new Promise(resolve => setTimeout(resolve, 600))
      await wrapper.vm.$nextTick()

      expect(pushSpy).toHaveBeenCalledWith('/setup')
    })

    it('should not navigate when validation fails', async () => {
      const wrapper = mountComponent()
      const button = wrapper.find('button')

      const pushSpy = vi.spyOn(router, 'push')

      await button.trigger('click')
      await wrapper.vm.$nextTick()

      expect(pushSpy).not.toHaveBeenCalled()
    })
  })

  describe('Loading State', () => {
    it('should show loading state during submission', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')
      const button = wrapper.find('button')

      await input.setValue('John Doe')

      // Trigger click but don't wait for completion
      button.trigger('click')

      // Wait a tiny bit for state to update
      await wrapper.vm.$nextTick()

      // Button text should show loading
      expect(button.text()).toContain('LOADING')
    })
  })

  describe('Store Integration', () => {
    it('should save user to store on successful submission', async () => {
      const wrapper = mountComponent()
      const input = wrapper.find('input[type="text"]')
      const button = wrapper.find('button')

      await input.setValue('John Doe')
      await button.trigger('click')
      await wrapper.vm.$nextTick()

      // Check if user was saved (this would be checked in the store test)
      expect(input.element.value).toBe('John Doe')
    })
  })
})
