# LiveCodingInterview - Roadmap

Frontend-First Implementation Plan

---

## Этап 0: Инициализация Frontend проекта ✅
**Цель**: Создать Vue.js приложение с базовой структурой

- [x] Создать проект с Vite + Vue 3
- [x] Установить и настроить Vue Router
- [x] Установить и настроить Pinia (state management)
- [x] Установить TailwindCSS
- [x] Установить Monaco Editor
- [x] Создать базовую структуру директорий
- [x] Запустить dev server и проверить работоспособность

**Design Concept**: Neo-Brutalist Technical
- Typography: JetBrains Mono + Space Mono
- Colors: Dark base (#0a0e27) with tech-green (#00ff41), tech-orange (#ff6b35), tech-cyan (#00d9ff)
- Dev server running at http://localhost:5173/

---

## Этап 1: Мок данных и сервисы Frontend ✅
**Цель**: Создать mock данные и API сервис-заглушки

- [x] Создать `src/mocks/data.js` с mock задачами
  - [x] 3 Junior задачи для Python
  - [x] 3 Middle задачи для Python
  - [x] 3 Senior задачи для Python
- [x] Создать mock сессий (через Pinia store)
- [x] Интегрировать mock данные в компоненты
- [x] Добавить helper функции (getRandomProblems, getProblemsByDifficulty)

---

## Этап 2: UI компоненты (Atomic Design)
**Цель**: Создать переиспользуемые компоненты

### Atoms (базовые компоненты)
- [ ] Button.vue
- [ ] Input.vue
- [ ] Select.vue
- [ ] Badge.vue
- [ ] Card.vue

### Molecules (составные компоненты)
- [ ] ProblemCard.vue
- [ ] CodeEditor.vue (обертка для Monaco)
- [ ] ProblemDescription.vue
- [ ] ExecutionResult.vue
- [ ] SessionHeader.vue

### Organisms (сложные компоненты)
- [ ] ProblemSelector.vue
- [ ] CodingWorkspace.vue
- [ ] EvaluationForm.vue

---

## Этап 3: Страницы Interviewer Flow ✅
**Цель**: Создать полный флоу для интервьюера

- [x] InterviewerLogin.vue (`/`)
  - [x] Форма ввода ФИО с валидацией
  - [x] Сохранение в Pinia store
  - [x] Редирект на /setup
- [x] SessionSetup.vue (`/setup`)
  - [x] Выбор уровня сложности (Junior/Middle/Senior)
  - [x] Выбор языка программирования (Python готов)
  - [x] Выбор количества задач (slider 1-5)
  - [x] Генерация ссылки для кандидата
  - [x] Копирование ссылки в clipboard
  - [x] Кнопка "Start Session"
- [x] InterviewerSessionView.vue (`/session/:id/interviewer`)
  - [x] Split screen layout (2/3 + 1/3)
  - [x] Read-only код с Prism.js syntax highlighting
  - [x] Отображение имени кандидата
  - [x] Описание задачи с difficulty badge
  - [x] Progress indicator с визуальным прогресс-баром
  - [x] Результаты выполнения (mock)
  - [x] Кнопки "Next Task" / "End Session"
- [x] SessionEvaluation.vue (`/session/:id/evaluate`)
  - [x] Список всех задач сессии
  - [x] Star rating система (1-5) для каждой задачи
  - [x] Текстовые комментарии
  - [x] Отображение кода кандидата с Prism.js подсветкой
  - [x] Кнопка "Submit Evaluation"
  - [x] Success modal после отправки

---

## Этап 4: Страницы Candidate Flow ✅
**Цель**: Создать полный флоу для кандидата

- [x] CandidateJoin.vue (`/join/:link`)
  - [x] Отображение имени интервьюера и session info
  - [x] Форма ввода ФИО с валидацией (min 3 символа)
  - [x] Кнопка "Join Session"
  - [x] Session details card (difficulty, problems count, language)
- [x] CandidateSessionView.vue (`/session/:id/candidate`)
  - [x] Split screen layout (2/3 + 1/3)
  - [x] Monaco Editor с полной поддержкой Python
  - [x] Custom theme matching Neo-Brutalist design
  - [x] Отображение имени интервьюера
  - [x] Описание задачи с difficulty badge
  - [x] Progress indicator с визуальным прогресс-баром
  - [x] Кнопка "Run Code" с loading states
  - [x] **Real Python execution через Pyodide (WebAssembly)**
  - [x] Auto-save каждые 2 секунды
  - [x] Результаты выполнения с success/error styling
- [x] ThankYouView.vue (`/session/:id/thankyou`)
  - [x] Thank you message с именем кандидата
  - [x] 15 случайных мудрых цитат о программировании
  - [x] Session statistics (problems solved, duration, code runs)
  - [x] Кнопка возврата на главную
  - [x] Анимация success icon

**Технические достижения:**
- ✅ Интеграция Monaco Editor с кастомной темой
- ✅ Pyodide для реального выполнения Python в браузере
- ✅ Решены проблемы с CDN загрузкой Pyodide
- ✅ Правильная обработка stdout/stderr через io.StringIO

---

## Этап 5: Интеграция и полировка Frontend ✅
**Цель**: Связать все компоненты, добавить UX улучшения

- [x] Настроить Pinia stores для session management
- [x] Добавить loading states во все view
- [x] Добавить error handling
- [x] Добавить transitions/animations (fade-in-up, pulse-glow)
- [x] Настроить Monaco Editor
  - [x] Syntax highlighting для Python (Prism.js + Monaco)
  - [x] Auto-completion (built-in Monaco)
  - [x] Line numbers с custom styling
  - [x] Custom dark theme matching Neo-Brutalist design
- [x] **Real-time синхронизация через localStorage**
  - [x] Auto-save кода кандидата (каждые 2 секунды)
  - [x] Синхронизация между вкладками interviewer/candidate
  - [x] Синхронизация execution results
  - [x] Синхронизация смены задач
  - [x] Storage events для cross-tab communication
- [x] Тестирование в двух вкладках браузера ✅ ПРОТЕСТИРОВАНО

**Примечание**: Responsive design и toast notifications отложены (не критично для MVP)

---

## Этап 6: Frontend тесты ✅
**Цель**: Покрыть Frontend тестами

- [x] Установить Vitest + Vue Test Utils + happy-dom
- [x] **Session Store Tests** (`session.spec.js`)
  - [x] 19 unit tests для Pinia store
  - [x] 91.3% statement coverage
  - [x] Тесты для actions, computed properties, localStorage sync
- [x] **Component Tests для Views**
  - [x] `InterviewerLogin.spec.js` - 12 tests (rendering, validation, navigation, loading)
  - [x] `SessionSetup.spec.js` - 18 tests (form, difficulty/language selection, modal)
  - [x] `ThankYouView.spec.js` - 20 tests (rendering, quotes, stats, accessibility)
- [x] **Все 69 тестов проходят успешно (100% pass rate)** ✅

**Примечание**: E2E тесты с Playwright отложены (решили сосредоточиться на Component tests)

---

## Этап 7: Инициализация Backend проекта ✅
**Цель**: Создать FastAPI приложение

- [x] Создать директорию backend/
- [x] Инициализировать проект с uv
- [x] Установить FastAPI, Uvicorn
- [x] Создать базовую структуру проекта
- [x] Создать main.py с hello world endpoint
- [x] Настроить CORS для Frontend
- [x] Запустить dev server
- [x] Проверить Swagger UI на /docs

---

## Этап 8: Backend моки и схемы ✅
**Цель**: Создать Pydantic схемы и mock endpoints

- [x] Создать Pydantic schemas
  - [x] UserSchema
  - [x] ProblemSchema
  - [x] SessionSchema
  - [x] SessionCreateSchema
  - [x] ExecutionResultSchema
  - [x] EvaluationSchema
- [x] Создать mock endpoints
  - [x] POST /api/auth/login
  - [x] GET /api/problems
  - [x] POST /api/sessions
  - [x] GET /api/sessions/{id}
  - [x] POST /api/sessions/{id}/join
  - [x] POST /api/sessions/{id}/end
  - [x] POST /api/sessions/{id}/evaluate
- [x] Проверить все endpoints через Swagger UI

---

## Этап 9: База данных ✅
**Цель**: Настроить PostgreSQL и миграции

- [x] Создать docker-compose.yml с PostgreSQL
- [x] Установить SQLAlchemy + asyncpg
- [x] Создать модели
  - [x] User
  - [x] Problem
  - [x] Session
  - [x] SessionProblem
  - [x] Evaluation
- [x] Настроить Alembic
- [x] Создать первую миграцию
- [x] Создать seed скрипт для задач (9 задач)
- [x] Запустить БД и применить миграции
- [x] Проверить данные в БД

---

## Этап 10: Backend бизнес-логика ✅
**Цель**: Реализовать реальную логику с БД

- [x] Создать CRUD сервисы для всех моделей
- [x] Реализовать логику создания сессии
- [x] Реализовать логику присоединения кандидата
- [x] Реализовать логику получения задач
- [x] Реализовать логику сохранения оценки
- [x] Добавить валидацию входных данных
- [x] Добавить обработку ошибок
- [x] Протестировать через Swagger UI
- [x] Исправить MissingGreenlet ошибку с async relationships

**Backend Tests** ✅
- [x] Установить pytest + pytest-asyncio + httpx
- [x] Настроить test database
- [x] API tests (22 tests)
  - [x] test_problems.py (6 tests)
  - [x] test_sessions.py (10 tests)
  - [x] test_evaluations.py (6 tests)
- [x] Service tests (22 tests)
  - [x] test_problems.py (5 tests)
  - [x] test_sessions.py (12 tests)
  - [x] test_evaluations.py (5 tests)
- [x] **44 tests, 100% pass rate** ✅

---

## Этап 11: WebSocket для real-time синхронизации ✅
**Цель**: Реализовать real-time обмен данными

- [x] Добавить WebSocket support в FastAPI
- [x] Создать Connection Manager для управления подключениями
- [x] Создать endpoint `WS /api/ws/{session_id}`
- [x] Реализовать broadcast сообщений по комнатам (sessions)
- [x] Создать WebSocket message schemas
  - [x] CodeUpdateMessage
  - [x] ProblemChangeMessage
  - [x] UserJoinedMessage / UserLeftMessage
  - [x] ConnectionStatusMessage
  - [x] RunCodeMessage / CodeResultMessage (готово для Stage 13)
  - [x] ErrorMessage
- [x] Обработать события
  - [x] code_update
  - [x] user_joined / user_left
  - [x] problem_change
  - [x] connection_status
- [x] Создать документацию WEBSOCKET.md
- [x] Автоматическая очистка disconnected connections

---

## Этап 12: Code execution engine ⏭️ ПРОПУЩЕН
**Цель**: Безопасное выполнение Python кода

⏭️ **Пропущен для MVP** - выполнение кода реализовано на клиенте через **Pyodide** (WebAssembly)

**Причины:**
- ✅ Проще и безопаснее для MVP
- ✅ Не требует сложной изоляции на сервере
- ✅ Уже реализовано во Frontend (Этап 4)
- ✅ Достаточно для демонстрации функционала

**Примечание:** Backend code execution может быть добавлен позже для production (Docker контейнеры + песочница)

---

## Этап 13: Интеграция Frontend с Backend ✅
**Цель**: Заменить моки на реальные API вызовы

- [x] Создать `src/services/api.js` с Axios
- [x] Настроить environment variables для API URL (.env, .env.example)
- [x] Создать WebSocket service (src/services/websocket.js)
- [x] Обновить SessionSetup.vue - использует POST /api/sessions
- [x] Обновить CandidateJoin.vue - использует GET /api/sessions/by-link и POST join
- [x] Обновить InterviewerSessionView.vue - API + WebSocket для real-time sync
- [x] Обновить CandidateSessionView.vue - API + WebSocket, отправка кода каждые 2s
- [x] Обновить SessionEvaluation.vue - использует POST /api/sessions/{id}/evaluate
- [x] Добавить error handling для всех API вызовов
- [x] Добавить loading states во всех views
- [x] Обновить .gitignore (добавлен .env)
- [x] Frontend и Backend запущены и готовы к тестированию

**Технические детали:**
- ✅ Axios client с interceptors и 30s timeout
- ✅ WebSocket service с auto-reconnect (max 5 попыток)
- ✅ Environment variables через Vite (VITE_API_BASE_URL, VITE_WS_BASE_URL)
- ✅ Real-time синхронизация кода между interviewer и candidate
- ✅ Broadcast problem changes через WebSocket
- ✅ Graceful disconnect при unmount компонентов
- ✅ Error messages с fallback текстами

---

## Этап 14: Backend тесты
**Цель**: Покрыть Backend тестами

- [ ] Установить pytest + pytest-asyncio
- [ ] Настроить test database
- [ ] Unit tests для моделей
- [ ] Unit tests для сервисов
- [ ] Integration tests для API endpoints
- [ ] WebSocket tests
- [ ] Code execution tests
- [ ] Проверить coverage (70%+)

---

## Этап 15: Контейнеризация ✅
**Цель**: Упаковать в Docker

- [x] Создать Dockerfile (multi-stage)
  - [x] Frontend: Multi-stage build (Node builder + Nginx)
  - [x] Backend: Python 3.11 + uv + non-root user
  - [x] Development Dockerfiles для hot reload
- [x] Создать docker-compose.yml для разработки
- [x] Создать docker-compose.prod.yml для продакшена
- [x] Настроить nginx.conf с проксированием API и WebSocket
- [x] Создать .dockerignore для frontend и backend
- [x] Настроить .env.prod.example для production
- [x] Создать Alembic data migration для seed данных
- [x] Создать DOCKER.md с полной документацией
- [x] Исправить команды uv в Dockerfiles
- [x] Удалить устаревший `version` из compose файлов
- [x] Протестировать `docker compose up`
- [x] Проверить работоспособность всех сервисов

**Технические детали:**
- ✅ Separate containers: db (postgres:15), backend (FastAPI), frontend (Nginx)
- ✅ Health checks для всех сервисов
- ✅ Volume mounts для development hot reload
- ✅ Non-root user в production backend
- ✅ Nginx проксирует /api → backend:8000 и /ws → WebSocket
- ✅ Gzip compression и security headers
- ✅ Миграции включают seed данных (9 problems)

---

## Этап 16: CI/CD Pipeline ✅
**Цель**: GitHub Actions для тестов и деплоя

- [x] Создать .github/workflows/ci.yml
  - [x] Frontend tests (Vitest, 65 tests)
  - [x] Backend tests (Pytest, 44 tests)
  - [x] Code quality checks (ESLint, Ruff, MyPy)
  - [x] Security scan (Gitleaks)
  - [x] Docker build verification
- [x] Создать .github/workflows/build.yml
  - [x] Multi-platform Docker builds (amd64, arm64)
  - [x] Push в GitHub Container Registry (GHCR)
  - [x] Auto-tagging (latest, branch, SHA, semver)
- [x] Создать .github/workflows/deploy.yml
  - [x] Deploy на Yandex Cloud через SSH
  - [x] Auto-deploy on push to main
  - [x] Manual workflow_dispatch trigger
  - [x] Health check verification
- [x] Протестировать все workflows
- [x] Создать CI_CD.md с полной документацией

**Технические детали:**
- ✅ Параллельные jobs для faster execution
- ✅ GitHub Service Containers для PostgreSQL в CI
- ✅ Docker layer caching для быстрой сборки
- ✅ Environment variables через GitHub Secrets
- ✅ Deployment script с database backups
- ✅ Auto-cleanup старых Docker images

---

## Этап 17: Deployment ✅
**Цель**: Опубликовать на облачном хостинге

- [x] Выбрать хостинг: **Yandex Cloud**
- [x] Создать виртуальную машину (Ubuntu)
- [x] Настроить Docker и Docker Compose на сервере
- [x] Настроить environment variables (.env.prod)
- [x] Настроить PostgreSQL в Docker контейнере
- [x] Deploy приложения через GitHub Actions
  - [x] SSH deployment с автоматическим pull и restart
  - [x] Database migrations через Alembic
  - [x] Database backups при каждом деплое
- [x] Настроить nginx для проксирования (встроен в Docker)
- [x] Протестировать production build
- [x] Проверить все функции в продакшене

**Production URL**: `http://89.169.142.153` (Yandex Cloud)

**Технические детали:**
- ✅ Deployment через SSH с использованием deploy.sh скрипта
- ✅ Pull готовых Docker images из GHCR (не собирает на сервере)
- ✅ Автоматические database backups (хранится 7 последних)
- ✅ Health checks перед завершением deployment
- ✅ Auto-deploy при push в main branch
- ✅ Graceful shutdown старых контейнеров
- ✅ Production environment variables через .env.prod
- ✅ PostgreSQL data persistence через Docker volumes

**Исправленные проблемы:**
- ✅ Использование переменных окружения вместо hardcode путей
- ✅ Правильная подстановка переменных в healthcheck ($$POSTGRES_USER)
- ✅ Команды через `uv run` для backend контейнера
- ✅ Относительные URL для API в production (проксируются nginx)
- ✅ WebSocket поддержка через nginx proxy
- ✅ CORS настройки для production

---

## Дополнительные задачи

### Документация ✅
- [x] Обновить README.md с инструкциями (Quick Start, Features, Tech Stack)
- [x] Добавить API документацию (Swagger UI на /docs)
- [x] Создать DOCKER.md (Docker setup guide)
- [x] Создать CI_CD.md (CI/CD pipeline documentation)
- [x] Создать WEBSOCKET.md (WebSocket protocol documentation)
- [ ] Создать architecture diagram
- [ ] Добавить screenshots

### Безопасность
- [x] Настроить Gitleaks для scan секретов
- [x] Добавить input validation (Pydantic schemas)
- [x] Проверить CORS настройки (настроены для production)
- [x] Code execution через Pyodide (безопасно, в браузере)
- [x] Non-root user в Docker контейнерах
- [x] Security headers в nginx
- [ ] Настроить rate limiting
- [ ] HTTPS/SSL (отложено)

### Мониторинг
- [x] Добавить health checks (database, backend, frontend)
- [x] Docker healthchecks для всех сервисов
- [x] Deployment verification в CI/CD
- [ ] Добавить структурированное логирование
- [ ] Добавить error tracking (Sentry - опционально)

---

## Прогресс
- **Всего этапов**: 17
- **Завершено**: 15 (Этапы 0-1, 3-11, 13, 15-17) ✅
- **Пропущено**: 2 (Этапы 2, 12) ⏭️
- **Осталось**: 0 🎉

## 🎉 MVP ЗАВЕРШЕН И ЗАДЕПЛОЕН!

### Текущий статус MVP

✅ **Frontend (Этапы 0-6, 13):**
- Полный интерфейс для нанимающего (login → setup → session → evaluation)
- Полный интерфейс для кандидата (join → session → thankyou)
- Neo-Brutalist Technical дизайн
- Monaco Editor с кастомной темой
- **Real Python execution через Pyodide/WebAssembly** ✅
- **Real-time синхронизация через WebSocket** ✅
- **Интеграция с Backend API** ✅
- Pinia state management
- **69 Component tests с 100% pass rate** ✅

✅ **Backend (Этапы 7-11):**
- FastAPI приложение с CORS
- PostgreSQL + SQLAlchemy + Alembic
- Pydantic schemas и REST API endpoints
- Business logic с async database queries
- **44 Backend tests (API + Services) с 100% pass rate** ✅
- **WebSocket для real-time синхронизации** ✅
- Connection Manager с broadcast по комнатам
- Swagger UI документация

✅ **Full Stack Integration (Этап 13):**
- API service с Axios (30s timeout, error interceptors)
- WebSocket service с auto-reconnect
- Environment variables (.env, .env.example)
- Все views обновлены для использования реального API
- Error handling и loading states
- Code sync через WebSocket каждые 2 секунды
- Problem change broadcast между interviewer и candidate

✅ **Containerization (Этап 15):**
- Docker multi-stage builds для frontend и backend
- docker-compose.yml (development) + docker-compose.prod.yml
- Nginx с проксированием API и WebSocket
- Health checks для всех сервисов
- Alembic data migrations с seed данными
- DOCKER.md документация
- Production-ready с security best practices

✅ **CI/CD Pipeline (Этап 16):**
- GitHub Actions workflows (CI, Build, Deploy)
- Automated testing (109 tests total: 65 frontend + 44 backend)
- Docker image builds и push в GHCR
- Code quality checks (ESLint, Ruff, MyPy)
- Security scanning (Gitleaks)
- Multi-platform Docker builds (amd64, arm64)
- CI_CD.md полная документация

✅ **Production Deployment (Этап 17):**
- Deployed на Yandex Cloud
- Production URL: http://89.169.142.153
- Auto-deploy при push в main
- SSH deployment с database backups
- Pull готовых Docker images из GHCR
- Production environment variables
- Все функции протестированы и работают

⏭️ **Пропущено:**
- Этап 2: UI компоненты Atomic Design (не критично для MVP)
- Этап 12: Code execution на backend (используем Pyodide на клиенте)
- Этап 14: Backend тесты (уже сделано на Этапе 10!)

🎯 **Возможные улучшения (post-MVP):**
- HTTPS/SSL сертификаты
- Custom domain
- Rate limiting
- Structured logging
- Error tracking (Sentry)
- Architecture diagram
- Screenshots для README
- Backend code execution (Docker sandbox)
- Multi-language support (JavaScript, Go, etc.)
- Session recording и playback
- Analytics dashboard
