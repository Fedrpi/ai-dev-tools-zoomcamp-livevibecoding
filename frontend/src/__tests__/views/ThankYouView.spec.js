import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ThankYouView from '../../views/ThankYouView.vue'
import { useSessionStore } from '../../stores/session'

describe('ThankYouView', () => {
  let store

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useSessionStore()
    localStorage.clear()
    // Reset store to clear any data from previous tests
    store.reset()
  })

  const mountComponent = () => {
    return mount(ThankYouView)
  }

  describe('Rendering', () => {
    it('should render thank you message', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('SESSION_COMPLETE')
      expect(wrapper.text()).toContain('Thank you for your time and effort')
    })

    it('should display success icon', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('✓')
    })

    it('should display candidate name', () => {
      store.setSession({
        candidate: {
          name: 'John Smith'
        }
      })

      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('Thank You, John Smith!')
    })

    it('should display default name if candidate not set', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('Thank You, Candidate!')
    })
  })

  describe('Wise Quote', () => {
    it('should display a wise quote', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('// Wise Words')
      // Should contain quotes
      expect(wrapper.text()).toMatch(/[""].*[""]/)
    })

    it('should display quote author', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('—')
    })

    // Note: Random quote is selected onMounted, which may not trigger in all test environments
    // The presence of the Wise Words section and quote structure is verified in other tests
  })

  // Note: Session statistics tests have been removed
  // Statistics are shown only in SessionEvaluation view for the interviewer

  describe('Layout and Styling', () => {
    it('should have centered layout', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('.flex.items-center.justify-center').exists()).toBe(true)
    })

    it('should have animated elements', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('.animate-fade-in-up').exists()).toBe(true)
      expect(wrapper.find('.animate-pulse-glow').exists()).toBe(true)
    })

    it('should use proper color scheme', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('.text-tech-green').exists()).toBe(true)
      expect(wrapper.find('.border-tech-green').exists()).toBe(true)
    })
  })

  describe('Thank You Message', () => {
    it('should display completion message', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('Your coding session has been completed successfully')
    })

    it('should display encouragement message', () => {
      const wrapper = mountComponent()

      expect(wrapper.text()).toContain('We appreciate your participation')
      expect(wrapper.text()).toContain('wish you the best of luck')
    })
  })

  describe('No Navigation', () => {
    it('should not have navigation buttons', () => {
      const wrapper = mountComponent()
      const buttons = wrapper.findAll('button')

      expect(buttons.length).toBe(0)
    })

    it('should not have links to other pages', () => {
      const wrapper = mountComponent()

      // Check that there are no router-link or anchor tags
      expect(wrapper.findAll('a').length).toBe(0)
    })
  })

  describe('Accessibility', () => {
    it('should have proper heading structure', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('h1').exists()).toBe(true)
      expect(wrapper.find('h2').exists()).toBe(true)
    })

    it('should use blockquote for quote', () => {
      const wrapper = mountComponent()

      expect(wrapper.find('blockquote').exists()).toBe(true)
    })
  })
})
