# Testing Guide

This document describes how to run tests for the LiveCoding Interview application.

## Table of Contents
- [Quick Start](#quick-start)
- [Running Tests Locally](#running-tests-locally)
- [Running Tests in Docker](#running-tests-in-docker)
- [Test Structure](#test-structure)
- [CI/CD Integration](#cicd-integration)
- [Coverage Reports](#coverage-reports)

## Quick Start

Run all tests using Docker (recommended for CI/CD):

```bash
./run-tests.sh
```

## Running Tests Locally

### Frontend Tests

```bash
cd frontend

# Run tests once
npm test -- --run

# Run tests in watch mode
npm test

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

### Backend Tests

**Prerequisites**: PostgreSQL test database must be running.

```bash
cd backend

# Run tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_api/test_sessions.py

# Run specific test
uv run pytest tests/test_api/test_sessions.py::test_create_session
```

## Running Tests in Docker

The project includes a Docker Compose configuration for running tests in isolated containers. This is the **recommended approach for CI/CD**.

### Prerequisites

- Docker and Docker Compose installed
- No need for local dependencies

### Commands

```bash
# Run all tests (frontend + backend)
./run-tests.sh

# Run only backend tests
./run-tests.sh --backend-only

# Run only frontend tests
./run-tests.sh --frontend-only

# Run tests and keep containers for debugging
./run-tests.sh --no-cleanup
```

### What Happens

1. **Test Database**: Spins up a PostgreSQL container with tmpfs for fast I/O
2. **Migrations**: Runs Alembic migrations to set up schema and seed data
3. **Backend Tests**: Runs pytest in isolated container
4. **Frontend Tests**: Runs Vitest in isolated container
5. **Cleanup**: Removes all test containers and volumes

## Test Structure

### Frontend Tests (Vitest + Vue Test Utils)

```
frontend/src/__tests__/
├── views/
│   ├── InterviewerLogin.spec.js      # Login page tests (12 tests)
│   ├── SessionSetup.spec.js          # Setup page tests (18 tests)
│   └── ThankYouView.spec.js          # Thank you page tests (24 tests)
└── stores/
    └── session.spec.js                # Pinia store tests (36 tests)
```

**Total**: 70 tests
- **Passing**: 63 ✓
- **Failing**: 7 ✗ (known issues with modals and statistics display)

### Backend Tests (Pytest)

```
backend/tests/
├── conftest.py                       # Test fixtures and configuration
├── test_api/
│   ├── test_evaluations.py          # Evaluation API tests (6 tests)
│   ├── test_problems.py              # Problems API tests (6 tests)
│   └── test_sessions.py              # Sessions API tests (9 tests)
└── test_services/
    ├── test_evaluations.py          # Evaluation service tests (5 tests)
    ├── test_problems.py              # Problems service tests (5 tests)
    └── test_sessions.py              # Sessions service tests (13 tests)
```

**Total**: 44 tests
- **Passing**: 44 ✓
- **Failing**: 0 ✗

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run tests
        run: ./run-tests.sh

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: always()
```

### GitLab CI Example

```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - chmod +x run-tests.sh
    - ./run-tests.sh
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/coverage-final.json
```

## Coverage Reports

### Frontend Coverage

Frontend tests use Vitest with v8 coverage provider.

```bash
cd frontend
npm run test:coverage
```

Coverage reports are generated in:
- `frontend/coverage/index.html` - HTML report
- `frontend/coverage/coverage-final.json` - JSON report

### Backend Coverage

Backend tests use pytest-cov for coverage reporting.

```bash
cd backend
uv run pytest --cov=app --cov-report=html --cov-report=term
```

Coverage reports are generated in:
- `backend/htmlcov/index.html` - HTML report
- `backend/coverage.json` - JSON report

## Test Database Configuration

### Local Development

For local testing, you need a PostgreSQL database:

```bash
# Using Docker
docker run -d \
  --name livecoding_test_db \
  -e POSTGRES_USER=livecoding \
  -e POSTGRES_PASSWORD=livecoding_password \
  -e POSTGRES_DB=livecoding_test_db \
  -p 5433:5432 \
  postgres:15-alpine
```

### Environment Variables

Backend tests use the following environment variable:

```bash
TEST_DATABASE_URL=postgresql+asyncpg://livecoding:livecoding_password@localhost:5433/livecoding_test_db
```

This is automatically set in `docker-compose.test.yml`.

## Known Issues

### Frontend

1. **Modal Display**: 2 tests failing related to session link modal display
2. **Statistics Display**: 5 tests failing in ThankYouView for statistics grid

These are UI-related issues that need to be addressed.

### Backend

No known issues. All 44 tests passing.

## Writing New Tests

### Frontend Test Example

```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.text()).toContain('Expected Text')
  })
})
```

### Backend Test Example

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_my_endpoint(client: AsyncClient):
    response = await client.get("/api/my-endpoint")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

## Troubleshooting

### "Database connection failed"

Ensure PostgreSQL is running and accessible:
```bash
docker compose -f docker-compose.test.yml up -d test_db
```

### "Permission denied: ./run-tests.sh"

Make the script executable:
```bash
chmod +x run-tests.sh
```

### "Port already in use"

Check if dev containers are running:
```bash
docker compose down
```

### Frontend tests timing out

Increase test timeout in `vitest.config.js`:
```javascript
test: {
  testTimeout: 10000
}
```

## Best Practices

1. **Always run tests before committing**
2. **Write tests for new features**
3. **Keep tests isolated and independent**
4. **Use fixtures for common test data**
5. **Mock external dependencies**
6. **Test edge cases and error scenarios**
7. **Maintain high test coverage (>80%)**

## Support

For issues or questions about testing:
- Check the [GitHub Issues](https://github.com/yourusername/livevibecoding/issues)
- Review test examples in the codebase
- Consult the framework documentation:
  - [Vitest](https://vitest.dev/)
  - [Pytest](https://docs.pytest.org/)
  - [Vue Test Utils](https://test-utils.vuejs.org/)
