import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const api = {
  sessions: {
    create: async (data) => {
      const response = await apiClient.post('/api/sessions', {
        interviewerName: data.interviewerName,
        difficulty: data.difficulty,
        language: data.language,
        numberOfProblems: data.numberOfProblems,
      })
      return response.data
    },

    getByLink: async (linkCode) => {
      const response = await apiClient.get(`/api/sessions/by-link/${linkCode}`)
      return response.data
    },

    getById: async (sessionId) => {
      const response = await apiClient.get(`/api/sessions/${sessionId}`)
      return response.data
    },

    join: async (sessionId, candidateName) => {
      const response = await apiClient.post(`/api/sessions/${sessionId}/join`, {
        candidateName,
      })
      return response.data
    },

    end: async (sessionId) => {
      const response = await apiClient.post(`/api/sessions/${sessionId}/end`)
      return response.data
    },
  },

  problems: {
    getAll: async (params = {}) => {
      const response = await apiClient.get('/api/problems', { params })
      return response.data
    },
  },

  evaluations: {
    submit: async (sessionId, evaluations) => {
      const response = await apiClient.post(`/api/sessions/${sessionId}/evaluate`, {
        evaluations,
      })
      return response.data
    },
  },
}

export default api
