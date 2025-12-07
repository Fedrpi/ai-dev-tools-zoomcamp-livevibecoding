<template>
  <div class="min-h-screen bg-dark-base">
    <!-- Header -->
    <div class="border-b-2 border-dark-border px-8 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-tech-cyan font-display">
            &lt; CANDIDATE_VIEW /&gt;
          </h1>
          <p class="text-xs text-tech-green mt-1 font-body">// Coding session in progress</p>
        </div>
        <div class="text-right">
          <p class="text-sm text-light-base font-body">
            Interviewer: <span class="text-tech-green font-bold">{{ interviewerName }}</span>
          </p>
          <p class="text-xs text-tech-cyan font-body mt-1">
            {{ progressText }}
          </p>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto p-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Code Editor -->
        <div class="lg:col-span-2 space-y-4">
          <div class="border-2 border-dark-border p-4 bg-dark-elevated">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm font-bold text-tech-cyan font-display uppercase">
                YOUR_CODE:
              </h2>
              <span class="text-xs text-tech-green font-body">
                ✓ Auto-sync enabled
              </span>
            </div>
            <!-- Monaco Editor Container -->
            <div
              ref="editorContainer"
              class="border-2 border-dark-border"
              style="height: 400px;"
            ></div>
          </div>

          <!-- Run Button & Results -->
          <div class="space-y-4">
            <button
              @click="runCode"
              :disabled="running || !pythonReady"
              class="w-full px-6 py-3 bg-tech-green text-dark-base font-display uppercase transition-all hover:bg-tech-cyan disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <span v-if="running || !pythonReady" class="spinner">⟳</span>
              <span v-if="!pythonReady && !executionResult">LOADING_PYTHON... (this may take 30-60s)</span>
              <span v-else-if="running">RUNNING...</span>
              <span v-else>RUN_CODE()</span>
            </button>

            <!-- Execution Results -->
            <div v-if="executionResult" class="border-2 p-4 bg-dark-elevated" :class="executionResult.success ? 'border-tech-green' : 'border-tech-orange'">
              <h3 class="text-sm font-bold font-display uppercase mb-3" :class="executionResult.success ? 'text-tech-green' : 'text-tech-orange'">
                {{ executionResult.success ? '✓ OUTPUT:' : '✗ ERROR:' }}
              </h3>
              <div class="bg-dark-base border-2 border-dark-border p-4 max-h-64 overflow-auto">
                <pre class="font-code text-sm whitespace-pre-wrap" :class="executionResult.success ? 'text-tech-green' : 'text-tech-orange'">{{ executionResult.output }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Problem Description -->
        <div class="space-y-4">
          <!-- Progress Indicator -->
          <div class="border-2 border-tech-cyan p-4 bg-dark-elevated">
            <p class="text-xs text-tech-cyan font-body mb-2">// Progress</p>
            <p class="text-3xl font-bold text-tech-cyan font-display">
              {{ currentProblemIndex + 1 }} / {{ totalProblems }}
            </p>
            <div class="mt-3 h-2 bg-dark-base">
              <div
                class="h-full bg-tech-cyan transition-all duration-300"
                :style="{ width: `${((currentProblemIndex + 1) / totalProblems) * 100}%` }"
              ></div>
            </div>
          </div>

          <!-- Current Problem -->
          <div class="border-2 border-tech-green p-4 bg-dark-elevated max-h-[600px] overflow-y-auto">
            <div class="mb-4">
              <div class="flex items-center gap-2 mb-2">
                <span
                  class="text-xs px-2 py-1 border-2 font-display uppercase"
                  :class="{
                    'border-tech-green text-tech-green': currentProblem?.difficulty === 'junior',
                    'border-tech-cyan text-tech-cyan': currentProblem?.difficulty === 'middle',
                    'border-tech-orange text-tech-orange': currentProblem?.difficulty === 'senior'
                  }"
                >
                  {{ currentProblem?.difficulty }}
                </span>
              </div>
              <h2 class="text-xl font-bold text-tech-green font-display mb-3">
                {{ currentProblem?.title }}
              </h2>
            </div>

            <div class="text-sm text-light-base font-body space-y-3">
              <p class="text-xs text-tech-cyan mb-2">// Problem Description:</p>
              <pre class="whitespace-pre-wrap text-sm">{{ currentProblem?.description }}</pre>
            </div>
          </div>

          <!-- Tips -->
          <div class="border-2 border-dark-border p-4 bg-dark-elevated">
            <p class="text-xs text-tech-cyan font-body mb-2">// Tips</p>
            <ul class="text-xs text-light-base font-body space-y-1">
              <li>• Real Python execution in browser</li>
              <li>• Test your code before submitting</li>
              <li>• Code syncs automatically every 2s</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSessionStore } from '../stores/session'
import { api } from '../services/api'
import { wsService } from '../services/websocket'
import * as monaco from 'monaco-editor'
import loader from '@monaco-editor/loader'

const router = useRouter()
const route = useRoute()
const sessionStore = useSessionStore()
const loading = ref(true)
const error = ref(null)

// Mock mode for faster development (set to false for production)
const USE_MOCK_PYTHON = false

// Load Pyodide from CDN dynamically
const loadPyodideFromCDN = async () => {
  // Check if already loaded
  if (window.loadPyodide) {
    return window.loadPyodide
  }

  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js'
    script.onload = () => {
      console.log('Pyodide script loaded')
      resolve(window.loadPyodide)
    }
    script.onerror = () => {
      reject(new Error('Failed to load Pyodide script from CDN'))
    }
    document.head.appendChild(script)
  })
}

// Reactive data
let editor = null
const editorContainer = ref(null)
const executionResult = ref(null)
const running = ref(false)
const pythonReady = ref(false)
let pyodide = null
let autoSaveInterval = null

// Computed properties
const interviewerName = computed(() => {
  return sessionStore.currentUser?.name || 'Technical Interviewer'
})

const currentProblem = computed(() => {
  const problems = sessionStore.currentSession?.problems || []
  return problems[sessionStore.currentProblemIndex] || null
})

const currentProblemIndex = computed(() => sessionStore.currentProblemIndex)
const totalProblems = computed(() => sessionStore.currentSession?.problems?.length || 0)

const progressText = computed(() => {
  return `Task ${currentProblemIndex.value + 1} of ${totalProblems.value}`
})

// Initialize Pyodide
const initPython = async () => {
  if (USE_MOCK_PYTHON) {
    // Mock mode - instant ready
    pythonReady.value = true
    console.log('Python ready (MOCK MODE)!')
    return
  }

  try {
    console.log('Starting Pyodide initialization...')
    console.log('Step 1: Loading Pyodide script from CDN...')

    // Load the Pyodide loader script
    const loadPyodide = await loadPyodideFromCDN()

    console.log('Step 2: Initializing Pyodide (this may take 30-60 seconds)...')

    // Try loading with longer timeout
    const timeout = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Pyodide initialization timeout (60s)')), 60000)
    )

    const loadPromise = loadPyodide()

    pyodide = await Promise.race([loadPromise, timeout])

    pythonReady.value = true
    console.log('✓ Python ready!')
  } catch (error) {
    console.error('Pyodide initialization error:', error)
    console.error('Error details:', error.message, error.stack)
    pythonReady.value = false
    executionResult.value = {
      success: false,
      output: `Failed to initialize Python environment: ${error.message}\n\nTip: Try refreshing the page or check your internet connection.\nPyodide requires downloading ~6-10 MB on first load.`
    }
  }
}

// Run Python code
const runCode = async () => {
  if (!editor) return
  if (!USE_MOCK_PYTHON && !pyodide) return

  running.value = true
  executionResult.value = null

  const code = editor.getValue()

  // Simulate delay
  await new Promise(resolve => setTimeout(resolve, 500))

  if (USE_MOCK_PYTHON) {
    // Mock Python execution
    try {
      let output = '// MOCK MODE - Python not actually executed\n\n'

      // Simple mock: detect print statements
      const printMatches = code.match(/print\((.*?)\)/g)
      if (printMatches) {
        printMatches.forEach(match => {
          const content = match.match(/print\((.*?)\)/)[1]
          output += `${content.replace(/['"]/g, '')}\n`
        })
      } else {
        output += 'Code executed successfully (no output)'
      }

      executionResult.value = {
        success: true,
        output: output
      }
    } catch (error) {
      executionResult.value = {
        success: false,
        output: error.message
      }
    }
  } else {
    // Real Python execution with Pyodide
    try {
      // Capture stdout using io module
      await pyodide.runPythonAsync(`
import sys
from io import StringIO
sys.stdout = StringIO()
sys.stderr = StringIO()
      `)

      // Run the user code
      let result = await pyodide.runPythonAsync(code)

      // Get the captured output
      const stdout = await pyodide.runPythonAsync('sys.stdout.getvalue()')
      const stderr = await pyodide.runPythonAsync('sys.stderr.getvalue()')

      // Reset stdout/stderr
      await pyodide.runPythonAsync(`
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
      `)

      let output = ''
      if (stdout) output += stdout
      if (stderr) output += stderr
      if (result !== undefined && result !== null && !stdout && !stderr) {
        output = String(result)
      }

      executionResult.value = {
        success: true,
        output: output || '// Code executed successfully (no output)'
      }
    } catch (error) {
      // Reset stdout/stderr even on error
      try {
        await pyodide.runPythonAsync(`
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
        `)
      } catch (e) {
        // Ignore reset errors
      }

      executionResult.value = {
        success: false,
        output: error.message
      }
    }
  }

  running.value = false

  // Save code and result to session
  sessionStore.updateCode(code)
  sessionStore.setExecutionResult(executionResult.value)
}

// Initialize Monaco Editor
const initEditor = () => {
  if (!editorContainer.value) return

  loader.config({ monaco })

  // Define custom theme that matches our design
  monaco.editor.defineTheme('custom-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '00d9ff', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'ff6b35', fontStyle: 'bold' },
      { token: 'string', foreground: '00ff41' },
      { token: 'number', foreground: 'ffdd00' },
      { token: 'function', foreground: 'ffdd00' }
    ],
    colors: {
      'editor.background': '#0a0e27',
      'editor.foreground': '#f5f5f0',
      'editor.lineHighlightBackground': '#1a1e3f',
      'editorLineNumber.foreground': '#00d9ff',
      'editorLineNumber.activeForeground': '#00ff41',
      'editorGutter.background': '#0a0e27',
      'editor.selectionBackground': '#1a1e3f',
      'editor.inactiveSelectionBackground': '#1a1e3f'
    }
  })

  editor = monaco.editor.create(editorContainer.value, {
    value: currentProblem.value?.starterCode || '# Write your code here\n',
    language: 'python',
    theme: 'custom-dark',
    fontSize: 14,
    fontFamily: 'JetBrains Mono, monospace',
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    automaticLayout: true,
    tabSize: 4,
    insertSpaces: true,
    lineNumbers: 'on',
    lineNumbersMinChars: 3,
    renderWhitespace: 'selection',
    bracketPairColorization: { enabled: true }
  })

  // Auto-save and broadcast code changes via WebSocket
  autoSaveInterval = setInterval(() => {
    if (editor) {
      const code = editor.getValue()
      sessionStore.updateCode(code)

      wsService.sendCodeUpdate(
        code,
        currentProblem.value?.id,
        currentProblemIndex.value
      )
    }
  }, 2000)
}

// Cleanup
onUnmounted(() => {
  if (editor) {
    editor.dispose()
  }
  if (autoSaveInterval) {
    clearInterval(autoSaveInterval)
  }
  wsService.disconnect()
})

// Watch for session end from interviewer
watch(() => sessionStore.sessionEnded, (ended) => {
  if (ended) {
    console.log('Session ended by interviewer, redirecting to thank you page...')
    const sessionId = route.params.id
    router.push(`/session/${sessionId}/thankyou`)
  }
})

// Watch for problem changes from interviewer
watch(() => sessionStore.currentProblemIndex, (newIndex, oldIndex) => {
  if (newIndex !== oldIndex && editor && currentProblem.value) {
    // Update editor with new problem's starter code
    editor.setValue(currentProblem.value.starterCode || '# Write your code here\n')
    executionResult.value = null
  }
})

// Initialize everything
onMounted(async () => {
  const sessionId = route.params.id

  try {
    const response = await api.sessions.getById(sessionId)
    sessionStore.setSession(response.session)

    // Check if session already ended
    if (sessionStore.sessionEnded) {
      router.push(`/session/${sessionId}/thankyou`)
      return
    }

    const userName = sessionStore.currentUser?.name || 'Candidate'
    wsService.connect(sessionId, userName, 'candidate')

    wsService.on('problem_change', (message) => {
      sessionStore.currentProblemIndex = message.problemIndex
    })

    wsService.on('user_joined', (message) => {
      console.log(`${message.userName} joined as ${message.role}`)
    })

    loading.value = false

    initEditor()
    initPython()
  } catch (err) {
    console.error('Failed to load session:', err)
    error.value = 'Failed to load session'
    loading.value = false
  }
})
</script>

<style>
/* Monaco Editor custom styling */
.monaco-editor {
  --vscode-editor-background: #0a0e27 !important;
  --vscode-editor-foreground: #f5f5f0 !important;
}

.monaco-editor .margin {
  background-color: #0a0e27 !important;
}

.monaco-editor .line-numbers {
  color: #00d9ff !important;
}

.monaco-editor .current-line ~ .line-numbers {
  color: #00ff41 !important;
}

/* Reduce gutter width */
.monaco-editor .margin-view-overlays {
  width: 40px !important;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: var(--color-dark-base);
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: var(--color-tech-green);
}

/* Spinning animation */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}
</style>
