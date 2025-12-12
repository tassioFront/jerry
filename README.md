# Jerry

Jerry is FastAPI Authentication Microservice Boilerplate. A production-ready, extensible authentication microservice built with FastAPI, PostgreSQL, and JWT. This boilerplate is designed to be a reusable foundation for authentication in microservices architectures.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Environment Configuration](#environment-configuration)

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

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### 2. Start the project using Docker

```bash
# Build and start services
docker compose up --build

# Start in detached mode
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f
```

---

## ⚙️ Environment Configuration

### `.env.example` Template

```env
# Database
DATABASE_URL=postgresql://auth_user:auth_password@localhost:5432/auth_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Email (for future email service integration)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourservice.com

# Service Info
SERVICE_NAME=auth-service
SERVICE_VERSION=1.0.0
```

### Environment-Specific Files

**`.env.test`** (for testing):
```env
DATABASE_URL=postgresql://auth_user:auth_password@localhost:5432/auth_test_db
JWT_SECRET_KEY=test-secret-key-for-testing
ENVIRONMENT=testing
DEBUG=True
LOG_LEVEL=DEBUG
```
