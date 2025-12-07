const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'

export class WebSocketService {
  constructor() {
    this.ws = null
    this.sessionId = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.messageHandlers = new Map()
    this.isIntentionalClose = false
  }

  connect(sessionId, userName, userRole) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    this.sessionId = sessionId
    this.isIntentionalClose = false

    const wsUrl = `${WS_BASE_URL}/api/ws/${sessionId}?user_name=${encodeURIComponent(userName)}&user_role=${userRole}`

    console.log('Connecting to WebSocket:', wsUrl)

    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
      this.trigger('connected')
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        console.log('WebSocket message received:', message)

        const type = message.type
        if (this.messageHandlers.has(type)) {
          this.messageHandlers.get(type)(message)
        }

        this.trigger('message', message)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      this.trigger('error', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket disconnected')
      this.trigger('disconnected')

      if (!this.isIntentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnect(userName, userRole)
      }
    }
  }

  reconnect(userName, userRole) {
    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)

    setTimeout(() => {
      if (this.sessionId) {
        this.connect(this.sessionId, userName, userRole)
      }
    }, delay)
  }

  disconnect() {
    this.isIntentionalClose = true
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.sessionId = null
    this.messageHandlers.clear()
  }

  send(message) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket not connected, cannot send message:', message)
    }
  }

  sendCodeUpdate(code, problemId, problemIndex) {
    this.send({
      type: 'code_update',
      code,
      problemId,
      problemIndex,
    })
  }

  sendProblemChange(problemIndex, problemId) {
    this.send({
      type: 'problem_change',
      problemIndex,
      problemId,
    })
  }

  on(type, handler) {
    this.messageHandlers.set(type, handler)
  }

  off(type) {
    this.messageHandlers.delete(type)
  }

  trigger(event, data) {
    if (this.messageHandlers.has(event)) {
      this.messageHandlers.get(event)(data)
    }
  }
}

export const wsService = new WebSocketService()
