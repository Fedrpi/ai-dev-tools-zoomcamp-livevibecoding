#!/bin/bash

# LiveCoding Platform - Deployment Script for Yandex Cloud
# This script is executed on the server during deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$HOME/ai-dev-tools-zoomcamp-livevibecoding"
BACKUP_DIR="$HOME/backups"
COMPOSE_FILE="docker-compose.prod.yml"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as correct user
if [ "$EUID" -eq 0 ]; then
   log_error "Please do not run this script as root"
   exit 1
fi

log_info "Starting deployment process..."

# Navigate to project directory
cd "$PROJECT_DIR" || {
    log_error "Project directory not found: $PROJECT_DIR"
    exit 1
}

# Pull latest changes
log_info "Pulling latest changes from repository..."
git fetch origin
git reset --hard origin/main
log_info "Repository updated to latest version"

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    log_error ".env.prod file not found!"
    log_error "Please create .env.prod file with production settings"
    exit 1
fi

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Backup database
log_info "Creating database backup..."
BACKUP_FILE="$BACKUP_DIR/livecoding_backup_$(date +%Y%m%d_%H%M%S).sql"
docker compose -f "$COMPOSE_FILE" exec -T db pg_dump \
    -U livecoding \
    -d livecoding_db \
    > "$BACKUP_FILE" 2>/dev/null || log_warn "Database backup skipped (database might not be running)"

if [ -f "$BACKUP_FILE" ]; then
    log_info "Database backed up to: $BACKUP_FILE"

    # Keep only last 7 backups
    log_info "Cleaning up old backups (keeping last 7)..."
    ls -t "$BACKUP_DIR"/livecoding_backup_*.sql 2>/dev/null | tail -n +8 | xargs -r rm
fi

# Pull latest Docker images from GitHub Container Registry
log_info "Pulling latest Docker images..."
docker compose -f "$COMPOSE_FILE" pull

# Build Docker images (disabled - using pre-built images from GHCR)
# log_info "Building Docker images..."
# docker compose -f "$COMPOSE_FILE" build --no-cache

# Stop old containers
log_info "Stopping old containers..."
docker compose -f "$COMPOSE_FILE" down

# Start new containers
log_info "Starting new containers..."
docker compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
log_info "Waiting for services to start..."
sleep 10

# Check if containers are running
if ! docker compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
    log_error "Containers failed to start!"
    log_info "Checking logs..."
    docker compose -f "$COMPOSE_FILE" logs --tail=50
    exit 1
fi

# Run database migrations
log_info "Running database migrations..."
docker compose -f "$COMPOSE_FILE" exec -T backend uv run alembic upgrade head

# Health check
log_info "Performing health check..."
sleep 5

if curl -f http://localhost/api/health > /dev/null 2>&1; then
    log_info "✓ Health check passed"
else
    log_warn "⚠ Health check failed, but continuing..."
fi

# Show container status
log_info "Container status:"
docker compose -f "$COMPOSE_FILE" ps

# Clean up old Docker images
log_info "Cleaning up old Docker images..."
docker image prune -f

log_info "========================================="
log_info "Deployment completed successfully!"
log_info "========================================="
log_info "Application URL: http://$(curl -s ifconfig.me)"
log_info "API Docs: http://$(curl -s ifconfig.me)/api/docs"
log_info "========================================="

# Show recent logs
log_info "Recent application logs:"
docker compose -f "$COMPOSE_FILE" logs --tail=20

exit 0
