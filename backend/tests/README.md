# Backend Tests

This directory contains tests for the LiveCoding Interview backend API.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_api/                # API endpoint tests
│   ├── test_problems.py     # Tests for /api/problems endpoints
│   ├── test_sessions.py     # Tests for /api/sessions endpoints
│   └── test_evaluations.py  # Tests for /api/sessions/{id}/evaluate endpoints
└── test_services/           # Service layer tests
    ├── test_problems.py     # Tests for problems service
    ├── test_sessions.py     # Tests for sessions service
    └── test_evaluations.py  # Tests for evaluations service
```

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run specific test file
```bash
uv run pytest tests/test_api/test_sessions.py
```

### Run specific test
```bash
uv run pytest tests/test_api/test_sessions.py::test_create_session
```

### Run with coverage (if pytest-cov is installed)
```bash
uv run pytest --cov=app --cov-report=term-missing
```

## Test Database

Tests use a separate PostgreSQL database: `livecoding_test_db`

The test database is automatically created and cleaned up for each test function.

## Writing Tests

All async tests should use the `@pytest.mark.asyncio` decorator:

```python
@pytest.mark.asyncio
async def test_example(client, sample_problems):
    response = await client.get("/api/problems")
    assert response.status_code == 200
```

## Available Fixtures

- `client` - AsyncClient for making HTTP requests to the API
- `db_session` - Database session for direct database operations
- `sample_problems` - Pre-populated test problems (3 problems: junior, middle, senior)
- `test_engine` - SQLAlchemy async engine for test database

## Test Coverage

Current test coverage:
- **API Tests**: 22 tests covering all endpoints
- **Service Tests**: 22 tests covering business logic
- **Total**: 44 tests, 100% passing
