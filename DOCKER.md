# Docker Usage Guide

This project is designed to run entirely in Docker. All commands should be executed using Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Create Environment File

```bash
# Copy the example environment file (if it exists)
cp .env.example .env

# Or create a minimal .env file
cat > .env << EOF
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_password
POSTGRES_DB=auth_db
DATABASE_URL=postgresql://auth_user:auth_password@db:5432/auth_db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
EOF
```

### 2. Start Services

```bash
# Build and start all services (database + API)
docker compose up --build

# Start in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f api
```

### 3. Access the Application

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 4. Stop Services

```bash
# Stop services
docker compose down

# Stop and remove volumes (clears database)
docker compose down -v
```

## Running Migrations

Migrations run automatically when the API container starts (via `docker-entrypoint.sh`).

To run migrations manually:

```bash
# Run migrations for main database
docker compose run --rm --profile migrate migrate

# Or run migrations directly
docker compose exec api alembic upgrade head
```

## Running Tests

### Run All Tests

```bash
# Using docker compose
docker compose run --rm --profile test test

# Using the test script
./run-tests.sh

# Run specific test file
./run-tests.sh tests/test_auth_register.py

# Run with verbose output
docker compose run --rm --profile test test pytest -v
```

### Test Coverage

```bash
docker compose run --rm --profile test test pytest --cov=app --cov-report=html
```

## Development Workflow

### Start Development Environment

```bash
# Start services with hot-reload
docker compose up

# The API will auto-reload on code changes
```

### Access Container Shell

```bash
# Access API container shell
docker compose exec api bash

# Access database
docker compose exec db psql -U auth_user -d auth_db
```

### View Database

```bash
# Connect to PostgreSQL
docker compose exec db psql -U auth_user -d auth_db

# List tables
\dt

# View users
SELECT * FROM "user";
```

## Docker Compose Services

### `db` - PostgreSQL Database
- Port: 5432
- Data persisted in `postgres_data` volume
- Health check enabled

### `api` - FastAPI Application
- Port: 8000
- Auto-reload in development mode
- Runs migrations on startup
- Health check enabled

### `test` - Test Runner (profile: test)
- Runs pytest
- Uses separate test database (`auth_test_db`)
- Creates test database automatically

### `migrate` - Migration Runner (profile: migrate)
- Runs Alembic migrations
- Can be used for manual migration execution

## Environment Variables

Key environment variables (set in `.env` file):

```env
# Database
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_password
POSTGRES_DB=auth_db
DATABASE_URL=postgresql://auth_user:auth_password@db:5432/auth_db

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker compose ps

# Check database logs
docker compose logs db

# Test database connection
docker compose exec api python -c "from app.database import engine; engine.connect()"
```

### Migration Issues

```bash
# Check migration status
docker compose exec api alembic current

# View migration history
docker compose exec api alembic history

# Rollback last migration
docker compose exec api alembic downgrade -1
```

### Container Issues

```bash
# Rebuild containers
docker compose build --no-cache

# Remove all containers and volumes
docker compose down -v

# Start fresh
docker compose up --build
```

### Test Database Issues

```bash
# Recreate test database
docker compose run --rm --profile test init-test-db

# Run tests with fresh database
docker compose run --rm --profile test test pytest -v
```

## Production Deployment

For production, use the production Dockerfile:

```bash
# Build production image
docker build -f Dockerfile -t auth-service:latest .

# Run production container
docker run -d \
  --name auth-service \
  -p 8000:8000 \
  --env-file .env.production \
  auth-service:latest
```

## Useful Commands

```bash
# View all running containers
docker compose ps

# View resource usage
docker stats

# Clean up unused resources
docker system prune

# View container logs
docker compose logs -f api

# Execute command in container
docker compose exec api python -c "from app.models import User; print('OK')"

# Restart a service
docker compose restart api

# Scale services (if needed)
docker compose up -d --scale api=3
```

