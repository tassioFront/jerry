# Jerry

Jerry is FastAPI Authentication Microservice Boilerplate. A production-ready, extensible authentication microservice built with FastAPI, PostgreSQL, and JWT. This boilerplate is designed to be a reusable foundation for authentication in microservices architectures.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)

---

## 🎯 Project Overview

This microservice handles:
- **User Registration** with email confirmation
- **User Login** with JWT token generation
- **Token Validation** and refresh token management
- **Email Verification** flow
- **Health checks** for service monitoring

**Design Principles:**
- Single responsibility: Authentication only
- Extensible architecture for easy feature additions
- Microservice-ready with event publishing support
- Type-safe with full type hints
- Comprehensive error handling
- Production-grade security

---

## ✨ Features

### Core Authentication
- ✅ User registration with email and password confirmation
- ✅ Email verification workflow
- ✅ User login with JWT token generation
- ✅ Refresh token functionality (24-hour access tokens, 7-day refresh tokens)
- ✅ Token validation and verification
- ✅ Password hashing with bcrypt (12 salt rounds)
- ✅ UUID-based user identification

### API & Documentation
- ✅ FastAPI with automatic OpenAPI/Swagger documentation
- ✅ Full type hints on all functions and parameters
- ✅ Standard error response format with error codes
- ✅ RESTful API design
- ✅ CORS support for development

### Database & Migrations
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ Alembic for database migrations
- ✅ UUID primary keys
- ✅ Audit fields (created_at, updated_at)

### Security
- ✅ JWT token signing with HS256
- ✅ Secure password hashing
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Environment-based configuration

### Testing & Quality
- ✅ Unit tests with pytest
- ✅ Database fixtures for testing
- ✅ Mocked JWT tokens for testing
- ✅ >80% code coverage
- ✅ Comprehensive logging

### DevOps
- ✅ Docker containerization
- ✅ Docker Compose for local development
- ✅ Health check endpoints
- ✅ Non-root user in container
- ✅ Production and development configurations

---

## 🛠 Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | FastAPI |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL 15+ |
| **ORM** | SQLAlchemy 2.0+ |
| **Migrations** | Alembic |
| **Authentication** | JWT (python-jose) |
| **Password Hashing** | bcrypt (passlib) |
| **API Server** | Uvicorn |
| **Testing** | pytest, pytest-asyncio |
| **Container** | Docker, Docker Compose |
| **Validation** | Pydantic v2 |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Router     │  │   Router     │  │   Router     │      │
│  │  /register   │  │   /login     │  │  /validate   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Security Layer (security.py)                 │   │
│  │  - Password hashing & verification                   │   │
│  │  - JWT creation & validation                         │   │
│  │  - Token parsing & claims extraction                 │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Database Layer (models.py)                   │   │
│  │  - User model with UUID, email, password_hash        │   │
│  │  - Audit fields (created_at, updated_at)            │   │
│  │  - Email verification tracking                       │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              PostgreSQL Database                            │
└─────────────────────────────────────────────────────────────┘

Microservice Communication:
Authentication Service ──[Event Publishing]──> Other Services
                                (User Created Event)
                                (Email Verification Event)
```

---

## 📦 Prerequisites

- **Python**: 3.11 or higher
- **Docker**: 20.10+ and Docker Compose 2.0+
- **PostgreSQL**: 15+ (for local development without Docker)
- **pip**: Latest version

---

## 🚀 Setup & Installation

### 1. Environment Configuration

Use the .env.example file

### 2. Start the project using Docker

```bash
# Build and start services (database + API)
docker compose up --build

# Start in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

Migrations run automatically when the API container starts.

### 3. Running Tests

All tests run in Docker - no local dependencies needed:

```bash
# Run all tests
docker compose run --rm test test

# Or use the test script
./run-tests.sh

# Run specific test file
./run-tests.sh tests/test_auth_register.py

# Run with verbose output
docker compose run --rm test test pytest -v -s
```

### 4. Running Migrations Manually

```bash
# Run migrations manually
docker compose run --rm migrate migrate

# Or execute in running container
docker compose exec api alembic upgrade head
```
