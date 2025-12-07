import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/InterviewerLogin.vue')
    },
    {
      path: '/setup',
      name: 'setup',
      component: () => import('../views/SessionSetup.vue')
    },
    {
      path: '/session/:id/interviewer',
      name: 'interviewer-session',
      component: () => import('../views/InterviewerSessionView.vue')
    },
    {
      path: '/session/:id/evaluate',
      name: 'evaluate',
      component: () => import('../views/SessionEvaluation.vue')
    },
    {
      path: '/join/:link',
      name: 'candidate-join',
      component: () => import('../views/CandidateJoin.vue')
    },
    {
      path: '/session/:id/candidate',
      name: 'candidate-session',
      component: () => import('../views/CandidateSessionView.vue')
    },
    {
      path: '/session/:id/thankyou',
      name: 'thankyou',
      component: () => import('../views/ThankYouView.vue')
    }
  ]
})

export default router
