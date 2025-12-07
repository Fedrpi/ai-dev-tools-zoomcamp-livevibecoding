# Docker Setup Guide

This guide explains how to run the LiveCoding Interview Platform using Docker.

## Architecture

The application is containerized with separate services:
- **db** - PostgreSQL 16 database
- **backend** - FastAPI application (Python 3.11)
- **frontend** - Vue.js application (Node 20)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Development Setup

### 1. Start All Services

```bash
docker compose up
```

Or run in detached mode:
```bash
docker compose up -d
```

### 2. View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### 3. Access Services

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

### 4. Stop Services

```bash
docker compose down
```

To remove volumes (database data):
```bash
docker compose down -v
```

## Production Setup

### 1. Create Environment File

```bash
cp .env.prod.example .env.prod
```

Edit `.env.prod` and set strong passwords:
```env
POSTGRES_USER=livecoding
POSTGRES_PASSWORD=STRONG_PASSWORD_HERE
POSTGRES_DB=livecoding_db
DATABASE_URL=postgresql+asyncpg://livecoding:STRONG_PASSWORD_HERE@db:5432/livecoding_db
```

### 2. Build and Run

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3. Run Database Migrations

**IMPORTANT**: Migrations are NOT run automatically. You must run them manually.

```bash
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

This command will:
- Create all database tables (User, Problem, Session, SessionProblem, Evaluation)
- Seed 9 initial coding problems (3 Junior, 3 Middle, 3 Senior for Python)
- All through Alembic migrations (version-controlled)

**Note**: The seed data is included in the migration `6134c4b0bc33_seed_initial_coding_problems.py`

### 4. Access Production

- **Application**: http://localhost (port 80)
- **Backend API**: http://localhost:8000 (internal, proxied through nginx)

## Useful Commands

### Rebuild Containers

```bash
# Development
docker compose build

# Production
docker compose -f docker-compose.prod.yml build

# Rebuild without cache
docker compose build --no-cache
```

### Execute Commands in Containers

```bash
# Backend shell
docker compose exec backend bash

# Database shell
docker compose exec db psql -U livecoding -d livecoding_db

# Frontend shell
docker compose exec frontend sh
```

### View Container Status

```bash
docker compose ps
```

### Clean Up

```bash
# Stop and remove containers, networks
docker compose down

# Also remove volumes (database data)
docker compose down -v

# Remove unused Docker resources
docker system prune -a
```

## Troubleshooting

### Port Already in Use

If ports 5173, 8000, or 5432 are already in use:

1. Stop conflicting services
2. Or change ports in `docker-compose.yml`:
   ```yaml
   ports:
     - "5174:5173"  # Changed host port
   ```

### Database Connection Errors

Ensure database is healthy:
```bash
docker compose logs db
docker compose ps db
```

Wait for health check to pass:
```bash
docker compose exec db pg_isready -U livecoding
```

### Frontend Build Errors

Clear node_modules volume and rebuild:
```bash
docker compose down -v
docker compose build frontend
docker compose up frontend
```

### Backend Dependency Errors

Rebuild backend with fresh dependencies:
```bash
docker compose build --no-cache backend
docker compose up backend
```

## Development Workflow

### Hot Reload

Both frontend and backend support hot reload in development mode:

- **Frontend**: Changes to `frontend/src/**` auto-reload
- **Backend**: Changes to `backend/app/**` auto-reload (uvicorn --reload)

### Database Migrations

Create new migration:
```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
docker compose exec backend alembic upgrade head
```

Rollback migration:
```bash
docker compose exec backend alembic downgrade -1
```

View migration history:
```bash
docker compose exec backend alembic history
```

### Running Tests

```bash
# Backend tests
docker compose exec backend pytest

# Frontend tests
docker compose exec frontend npm test
```

## Security Notes

### Development
- Simple passwords are OK for local development
- Database exposed on host port 5432 for debugging

### Production
- **NEVER** commit `.env.prod` to git
- Use strong passwords (20+ characters)
- Consider using Docker secrets for sensitive data
- Don't expose database port in production
- Use environment variables from hosting platform

## Performance Optimization

### Production Build
- Frontend uses multi-stage build (builder + nginx)
- Backend runs with 4 uvicorn workers
- Static files cached for 1 year
- Gzip compression enabled

### Resource Limits

Add to `docker-compose.prod.yml` if needed:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Monitoring

### Health Checks

All services have health checks:
```bash
docker compose ps
```

Look for "healthy" status.

### View Resource Usage

```bash
docker stats
```

## Next Steps

After containers are running:
1. Access frontend at http://localhost:5173
2. Check API docs at http://localhost:8000/docs
3. Run database migrations
4. Seed database with coding problems
5. Start coding interview session!
