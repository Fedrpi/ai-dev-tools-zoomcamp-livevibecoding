# CI/CD Pipeline Documentation

This project uses GitHub Actions for continuous integration and deployment.

## Workflows

### 1. CI Pipeline (`ci.yml`)

Runs on every push and pull request to `main`, `init`, and `develop` branches.

#### Jobs

**1. Secrets Scan**
- Tool: [Gitleaks](https://github.com/gitleaks/gitleaks)
- Scans for accidentally committed secrets, passwords, API keys
- Configuration: `.gitleaks.toml`
- Runs on: Every commit
- Fails build if: Secrets detected

**2. Lint Backend (Python)**
- Tool: Ruff (linter + formatter)
- Checks code style and common errors
- Configuration: `backend/pyproject.toml`
- Type checking: MyPy (warnings only)
- Runs: `ruff check .` and `ruff format --check .`

**3. Lint Frontend (Vue.js)**
- Tool: ESLint + Prettier
- Checks Vue.js code style
- Configuration: `frontend/.eslintrc.cjs`, `frontend/.prettierrc.json`
- Runs: `npm run lint`

**4. Test Backend**
- Framework: Pytest
- Database: PostgreSQL 15 (GitHub Service Container)
- Coverage: Available via pytest-cov
- Steps:
  1. Start PostgreSQL service container
  2. Wait for health check
  3. Install dependencies with UV
  4. Run tests (conftest.py creates tables automatically)
- Tests: 44 backend tests (API + Services)

**5. Test Frontend**
- Framework: Vitest
- Environment: happy-dom
- Tests: 65 frontend tests (Components + Stores)
- Runs: `npm test -- --run`

**6. Build Docker Images**
- Builds backend and frontend Docker images
- Verifies Dockerfiles are valid
- Uses Docker layer caching
- Does NOT push images (see Build workflow)

#### Example Run

```
┌─ Secrets Scan ✓
├─ Lint Backend ✓
├─ Lint Frontend ✓
├─ Test Backend ✓
│  └─ PostgreSQL Service (localhost:5432)
├─ Test Frontend ✓
└─ Build Docker ✓
   ├─ backend image
   └─ frontend image
```

### 2. Build and Push (`build.yml`)

Builds and pushes Docker images to GitHub Container Registry.

#### When it runs:
- Push to `main` branch
- Git tags (e.g., `v1.0.0`)
- Manual trigger via workflow_dispatch

#### What it does:
- Builds multi-platform images (amd64, arm64)
- Pushes to `ghcr.io/<your-username>/livecoding-backend`
- Pushes to `ghcr.io/<your-username>/livecoding-frontend`
- Tags:
  - `latest` (for main branch)
  - `<branch-name>` (for branches)
  - `v1.0.0` (for semver tags)
  - `<sha>` (commit SHA)

#### Example:
```bash
# After merge to main:
ghcr.io/yourusername/livecoding-backend:latest
ghcr.io/yourusername/livecoding-backend:main
ghcr.io/yourusername/livecoding-backend:sha-abc123

# After creating tag v1.0.0:
ghcr.io/yourusername/livecoding-backend:v1.0.0
ghcr.io/yourusername/livecoding-backend:1.0
ghcr.io/yourusername/livecoding-backend:latest
```

### 3. Deploy (`deploy.yml`)

Deployment workflow (manual trigger only).

#### Status:
🚧 **Placeholder** - To be configured for your cloud provider

#### Supported platforms:
- Railway
- Fly.io
- Render
- Google Cloud Run
- AWS ECS

#### How to use:
1. Go to Actions → Deploy to Cloud
2. Click "Run workflow"
3. Select environment (staging/production)
4. Click "Run"

**Note:** You need to configure this workflow with your cloud provider's deployment steps.

## GitHub Services in CI

### How PostgreSQL works in tests:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    env:
      POSTGRES_USER: livecoding
      POSTGRES_PASSWORD: test_password
      POSTGRES_DB: livecoding_test_db
    ports:
      - 5432:5432
```

**Flow:**
1. GitHub Actions runner starts
2. PostgreSQL container launches
3. Health check runs (`pg_isready`)
4. Once healthy, job steps execute
5. Tests connect to `localhost:5432`
6. After job completes, container is destroyed

**Why this works:**
- Service containers run in the same network as the job
- `localhost:5432` is mapped to the PostgreSQL container
- No docker-compose needed!

## Local Development

### Run linters locally:

**Backend:**
```bash
cd backend
uv run ruff check .          # Check code
uv run ruff format .         # Format code
uv run mypy app             # Type check
```

**Frontend:**
```bash
cd frontend
npm run lint                # ESLint + auto-fix
npm run format              # Prettier
```

### Run security scan:

```bash
# Install gitleaks
brew install gitleaks  # macOS
# or download from https://github.com/gitleaks/gitleaks

# Scan repository
gitleaks detect --source . --verbose
```

### Run tests locally:

**Backend:**
```bash
./run-tests.sh --backend-only
# or
cd backend && uv run pytest
```

**Frontend:**
```bash
./run-tests.sh --frontend-only
# or
cd frontend && npm test
```

**All tests:**
```bash
./run-tests.sh
```

## Secrets Management

### What is checked:
- Database passwords in code
- API keys
- Private keys
- Connection strings with credentials
- AWS/GCP credentials

### Allowlisted files:
- `*.env.example` - Example files are OK
- `docker-compose.test.yml` - Test credentials are OK
- Documentation files

### If secrets are detected:

1. **Remove secret from code:**
   ```bash
   # Don't commit real credentials!
   # Use environment variables instead
   ```

2. **Remove from history:**
   ```bash
   # Use BFG Repo Cleaner or git-filter-repo
   # https://github.com/newren/git-filter-repo
   ```

3. **Rotate compromised secrets:**
   - Change database passwords
   - Regenerate API keys
   - Update all deployments

## Required GitHub Secrets

For full CI/CD functionality, add these secrets to your repository:

### For Docker Build (automatic)
- `GITHUB_TOKEN` - Provided automatically by GitHub

### For Deployment (when configured)
- Platform-specific secrets (add when you configure deployment)
- Examples:
  - `RAILWAY_TOKEN` (Railway)
  - `FLY_API_TOKEN` (Fly.io)
  - `RENDER_DEPLOY_HOOK` (Render)

## Badge Status

Add these to your README.md:

```markdown
![CI](https://github.com/YOUR_USERNAME/livevibecoding/workflows/CI%20Pipeline/badge.svg)
![Build](https://github.com/YOUR_USERNAME/livevibecoding/workflows/Build%20and%20Push%20Docker%20Images/badge.svg)
```

## Troubleshooting

### Tests fail in CI but pass locally

**Check:**
- Different Python/Node versions
- Missing environment variables
- Port conflicts (unlikely in GitHub Actions)
- Database schema mismatch

**Solution:**
```bash
# Match CI environment locally
python --version  # Should be 3.11
node --version    # Should be 20
```

### Secrets scan false positive

**Solution:**
Add to `.gitleaks.toml`:
```toml
[[allowlist]]
description = "Allow specific file"
paths = [
  '''path/to/file\.ext$'''
]
```

### Docker build fails in CI

**Check:**
- Dockerfile syntax
- Missing dependencies in requirements
- Build context path

**Debug:**
```bash
# Build locally with same context
docker build -f backend/Dockerfile backend/
```

### Linter fails but code looks fine

**Backend (Ruff):**
```bash
# Auto-fix issues
cd backend
uv run ruff check --fix .
uv run ruff format .
```

**Frontend (ESLint):**
```bash
# Auto-fix issues
cd frontend
npm run lint
```

## Performance

**Average CI run time:**
- Secrets Scan: ~30 seconds
- Linting: ~1 minute
- Backend Tests: ~1-2 minutes (with DB setup)
- Frontend Tests: ~30 seconds
- Docker Builds: ~2-3 minutes

**Total: ~5-7 minutes** for full CI pipeline

## Best Practices

1. **Always run locally first:**
   ```bash
   ./run-tests.sh
   ```

2. **Use meaningful commit messages:**
   ```bash
   git commit -m "fix: resolve CORS issue in backend API"
   ```

3. **Never commit secrets:**
   - Use `.env` files (gitignored)
   - Use GitHub Secrets for CI/CD

4. **Keep dependencies updated:**
   ```bash
   cd backend && uv lock --upgrade
   cd frontend && npm update
   ```

5. **Review failed checks:**
   - Read the full error log
   - Don't just re-run - fix the issue

## Next Steps

- [ ] Configure deployment workflow for chosen cloud platform
- [ ] Add code coverage reporting (Codecov)
- [ ] Add automated dependency updates (Dependabot)
- [ ] Set up branch protection rules
- [ ] Configure required status checks
