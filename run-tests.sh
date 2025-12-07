#!/bin/bash
# Test runner script for LiveCoding Interview application
# This script runs all tests using Docker Compose

set -e  # Exit on error

echo "========================================="
echo "LiveCoding Interview - Test Runner"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
RUN_BACKEND=true
RUN_FRONTEND=true
CLEANUP=true

while [[ $# -gt 0 ]]; do
  case $1 in
    --backend-only)
      RUN_FRONTEND=false
      shift
      ;;
    --frontend-only)
      RUN_BACKEND=false
      shift
      ;;
    --no-cleanup)
      CLEANUP=false
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--backend-only] [--frontend-only] [--no-cleanup]"
      exit 1
      ;;
  esac
done

# Cleanup function
cleanup() {
  if [ "$CLEANUP" = true ]; then
    echo ""
    echo -e "${YELLOW}Cleaning up test containers...${NC}"
    docker compose -f docker-compose.test.yml down -v
  fi
}

# Register cleanup on exit
trap cleanup EXIT

# Build images
echo -e "${YELLOW}Building test images...${NC}"
docker compose -f docker-compose.test.yml build

# Start test database
echo ""
echo -e "${YELLOW}Starting test database...${NC}"
docker compose -f docker-compose.test.yml up -d test_db

# Wait for database to be healthy
echo -e "${YELLOW}Waiting for database to be ready...${NC}"
sleep 5

# Run migrations
echo ""
echo -e "${YELLOW}Running database migrations...${NC}"
docker compose -f docker-compose.test.yml run --rm test_migrations

# Run backend tests
if [ "$RUN_BACKEND" = true ]; then
  echo ""
  echo -e "${YELLOW}=========================================${NC}"
  echo -e "${YELLOW}Running Backend Tests${NC}"
  echo -e "${YELLOW}=========================================${NC}"

  if docker compose -f docker-compose.test.yml run --rm backend_test; then
    echo ""
    echo -e "${GREEN}✓ Backend tests PASSED${NC}"
    BACKEND_EXIT=0
  else
    echo ""
    echo -e "${RED}✗ Backend tests FAILED${NC}"
    BACKEND_EXIT=1
  fi
fi

# Run frontend tests
if [ "$RUN_FRONTEND" = true ]; then
  echo ""
  echo -e "${YELLOW}=========================================${NC}"
  echo -e "${YELLOW}Running Frontend Tests${NC}"
  echo -e "${YELLOW}=========================================${NC}"

  if docker compose -f docker-compose.test.yml run --rm frontend_test; then
    echo ""
    echo -e "${GREEN}✓ Frontend tests PASSED${NC}"
    FRONTEND_EXIT=0
  else
    echo ""
    echo -e "${RED}✗ Frontend tests FAILED${NC}"
    FRONTEND_EXIT=1
  fi
fi

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="

if [ "$RUN_BACKEND" = true ]; then
  if [ $BACKEND_EXIT -eq 0 ]; then
    echo -e "Backend:  ${GREEN}✓ PASSED${NC}"
  else
    echo -e "Backend:  ${RED}✗ FAILED${NC}"
  fi
fi

if [ "$RUN_FRONTEND" = true ]; then
  if [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "Frontend: ${GREEN}✓ PASSED${NC}"
  else
    echo -e "Frontend: ${RED}✗ FAILED${NC}"
  fi
fi

echo "========================================="

# Exit with error if any tests failed
if [ "$RUN_BACKEND" = true ] && [ $BACKEND_EXIT -ne 0 ]; then
  exit 1
fi

if [ "$RUN_FRONTEND" = true ] && [ $FRONTEND_EXIT -ne 0 ]; then
  exit 1
fi

exit 0
