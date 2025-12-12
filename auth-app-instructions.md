# Jerry

Welcome to Jerry: A FastAPI Authentication Microservice Boilerplate. 

It is a production-ready, extensible authentication microservice built with FastAPI, PostgreSQL, and JWT. This boilerplate is designed to be a reusable foundation for authentication in microservices architectures.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Implementation Steps](#implementation-steps)
- [Testing](#testing)
- [Error Response Format](#error-response-format)
- [Event Publishing](#event-publishing)
- [Deployment](#deployment)
- [Future Extensions](#future-extensions)

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

## 📁 Project Structure

```
auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app initialization
│   ├── config.py                  # Configuration & env variables
│   ├── database.py                # Database session & connection
│   ├── schemas.py                 # Pydantic models (request/response)
│   ├── models.py                  # SQLAlchemy ORM models
│   ├── security.py                # JWT & password hashing logic
│   ├── dependencies.py            # FastAPI dependencies
│   ├── exceptions.py              # Custom exceptions
│   ├── events.py                  # Event publishing logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py                # Authentication endpoints
│       └── health.py              # Health check endpoints
│
├── migrations/                     # Alembic migrations
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_auth_register.py      # Register feature tests
│   ├── test_auth_login.py         # Login feature tests
│   ├── test_auth_validation.py    # Token validation tests
│   └── fixtures.py                # Shared test fixtures
│
├── docker-compose.yml             # PostgreSQL + FastAPI services
├── Dockerfile                     # FastAPI container
├── .dockerignore
├── .env.example                   # Environment template
├── .env.test                      # Test environment
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── main.py                        # Application entry point
└── README.md                      # This file
```

---

## 📦 Prerequisites

- **Python**: 3.11 or higher
- **Docker**
- **PostgreSQL**: 15+ (for local development without Docker)
- **pip**: Latest version

---

## 🚀 Setup & Installation

DO not install locally, use Docker!

### 1. Clone or Initialize Project

```bash
# Create project directory
mkdir auth-service
cd auth-service

# Initialize git
git init

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
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

---

### Database Schema

The User table will be created by Alembic migrations:

```sql
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_created_at ON "user"(created_at);
```


---

## 📚 API Documentation

### Interactive API Docs

Once running, access:
- **Swagger UI**: `http://localhost:8000/docs`

### API Endpoints

#### 1. User Registration

**Endpoint**: `POST /api/v1/auth/register`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "password_confirmation": "SecurePassword123!"
}
```

**Success Response** (201):
```json
{
  "success": true,
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "message": "Registration successful. Please verify your email."
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error Response** (400):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password confirmation does not match",
    "details": {
      "field": "password_confirmation",
      "issue": "Passwords do not match"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Verify Email

**Endpoint**: `POST /api/v1/auth/verify-email`

**Request**:
```json
{
  "token": "email-verification-token"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "message": "Email verified successfully",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 3. User Login

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 4. Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 5. Validate Token

**Endpoint**: `POST /api/v1/auth/validate-token`

**Request**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "is_valid": true,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "expires_at": "2024-01-16T10:30:00Z"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 6. Health Check

**Endpoint**: `GET /health`

**Success Response** (200):
```json
{
  "status": "healthy",
  "service": "auth-service",
  "version": "1.0.0",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔧 Implementation Steps

Follow these steps in order. Each step includes implementation details and unit tests.

### Step 1: Set Up Docker

**What to do:**
- Create `Dockerfile` for FastAPI application
- Create `docker-compose.yml` with PostgreSQL and FastAPI services
- Configure volume mounts for development
- Set up environment variables in Docker

**Files to create:**
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

**Key configurations:**
- PostgreSQL service with persistent volumes
- FastAPI service with development mode
- Health checks for both services
- Non-root user in container for security

**Testing:**
```bash
docker-compose up --build
docker-compose ps  # Verify both services are running
```

**✅ Verification:**
- PostgreSQL service is running on port 5432
- FastAPI service is running on port 8000
- Health check endpoint responds: `GET /health`

---

### Step 2: Implement Security and JWT Logic

**What to do:**
- Create password hashing functions with bcrypt
- Implement JWT token creation (access + refresh)
- Implement JWT token validation and parsing
- Create security exceptions and error handling
- Set up configuration for JWT parameters

**Files to create:**
- `app/config.py` - Configuration with environment variables
- `app/security.py` - All JWT and password logic
- `app/exceptions.py` - Custom exceptions

**Files to modify:**
- `app/main.py` - Basic FastAPI setup

**Key implementations:**

```python
# app/security.py - Core functions to implement
- hash_password(password: str) -> str
- verify_password(plain_password: str, hashed_password: str) -> bool
- create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str
- create_refresh_token(data: dict) -> str
- decode_token(token: str, token_type: str = "access") -> dict
- verify_token(token: str) -> dict
```

**JWT Token Structure:**
- Access Token: expires in 24 hours, contains user_id and email
- Refresh Token: expires in 7 days, contains user_id only
- Algorithm: HS256

**Unit Tests:**
Create `tests/test_security.py` with tests for:
- Password hashing and verification
- Access token creation and validation
- Refresh token creation and validation
- Token expiration handling
- Invalid token rejection

**✅ Verification:**
```bash
pytest tests/test_security.py -v

# Should pass all tests:
# test_hash_password
# test_verify_password_correct
# test_verify_password_incorrect
# test_create_access_token
# test_create_refresh_token
# test_decode_valid_token
# test_decode_expired_token
# test_decode_invalid_token
```

---

### Step 3: Create the Register Feature

**What to do:**
- Create User SQLAlchemy model
- Create Pydantic schemas for registration
- Implement registration endpoint with validation
- Implement email verification token generation
- Set up database migrations with Alembic
- Create unit tests for registration

**Files to create:**
- `app/models.py` - User SQLAlchemy model
- `app/schemas.py` - Pydantic schemas
- `app/database.py` - Database connection and session
- `app/dependencies.py` - FastAPI dependencies
- `migrations/versions/001_initial.py` - Alembic migration
- `tests/test_auth_register.py` - Register endpoint tests
- `tests/fixtures.py` - Database and mock fixtures

**Files to modify:**
- `app/routers/auth.py` - Add registration endpoint
- `app/main.py` - Add router and middleware

**Key implementations:**

```python
# app/models.py - User model
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# app/schemas.py - Registration schema
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str
    
    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        # Minimum 8 chars, 1 uppercase, 1 number, 1 special char
        return v

# app/routers/auth.py - Register endpoint
@router.post("/register", status_code=201, response_model=ResponseModel[UserRegisterResponse])
async def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
) -> ResponseModel[UserRegisterResponse]:
    # Validate passwords match
    # Check if email exists
    # Create user with hashed password
    # Generate email verification token
    # Publish event: UserRegisteredEvent
    # Return user_id and message
```

**Alembic Migration:**
```bash
# Initialize migrations
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial user table"

# Apply migration
alembic upgrade head
```

**Unit Tests:**
Create `tests/test_auth_register.py` with tests for:
- Successful registration
- Duplicate email rejection
- Password mismatch rejection
- Invalid email format rejection
- Invalid password format rejection
- Database integrity
- Event publishing

**✅ Verification:**
```bash
# Run migrations
alembic upgrade head

# Run tests
pytest tests/test_auth_register.py -v

# Should pass all tests:
# test_register_success
# test_register_duplicate_email
# test_register_password_mismatch
# test_register_invalid_email
# test_register_weak_password
# test_register_creates_user_in_db
# test_register_publishes_event
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "password_confirmation": "SecurePassword123!"
  }'
```

---

### Step 4: Create the Login Feature

**What to do:**
- Implement login endpoint with credential validation
- Generate access and refresh tokens on successful login
- Create error responses for invalid credentials
- Implement rate limiting (optional but recommended)
- Create unit tests for login

**Files to create:**
- `tests/test_auth_login.py` - Login endpoint tests

**Files to modify:**
- `app/schemas.py` - Add login request/response schemas
- `app/routers/auth.py` - Add login endpoint
- `app/exceptions.py` - Add login-specific exceptions

**Key implementations:**

```python
# app/schemas.py - Login schemas
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user_id: UUID

# app/routers/auth.py - Login endpoint
@router.post("/login", status_code=200, response_model=ResponseModel[TokenResponse])
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
) -> ResponseModel[TokenResponse]:
    # Find user by email
    # Verify password
    # Generate tokens
    # Publish event: UserLoggedInEvent
    # Return tokens and user_id
```

**Unit Tests:**
Create `tests/test_auth_login.py` with tests for:
- Successful login
- Invalid email (user not found)
- Invalid password
- Email not verified (optional flow)
- Token structure and content
- Token expiration times
- Refresh token generation
- Event publishing

**✅ Verification:**
```bash
pytest tests/test_auth_login.py -v

# Should pass all tests:
# test_login_success
# test_login_user_not_found
# test_login_invalid_password
# test_login_returns_valid_tokens
# test_login_access_token_expiration
# test_login_refresh_token_expiration
# test_login_publishes_event
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

---

### Step 5: Create the Token Validation Feature

**What to do:**
- Implement token validation endpoint
- Implement refresh token endpoint
- Create dependency injection for protected routes
- Add JWT middleware for automatic validation
- Create unit tests for token validation

**Files to create:**
- `tests/test_auth_validation.py` - Token validation tests

**Files to modify:**
- `app/schemas.py` - Add validation request/response schemas
- `app/routers/auth.py` - Add validation and refresh endpoints
- `app/dependencies.py` - Add get_current_user dependency
- `app/main.py` - Add JWT middleware

**Key implementations:**

```python
# app/dependencies.py - Current user dependency
async def get_current_user(
    token: Annotated[str, Depends(HTTPBearer())],
    db: Session = Depends(get_db)
) -> User:
    # Validate token
    # Extract user_id from token
    # Fetch user from database
    # Return user object

# app/routers/auth.py - Validation and refresh endpoints
@router.post("/validate-token", response_model=ResponseModel[TokenValidationResponse])
async def validate_token(
    request: ValidateTokenRequest
) -> ResponseModel[TokenValidationResponse]:
    # Validate token signature
    # Extract claims
    # Return validation result with user info

@router.post("/refresh", response_model=ResponseModel[TokenResponse])
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> ResponseModel[TokenResponse]:
    # Validate refresh token
    # Generate new access token
    # Return new tokens
```

**Unit Tests:**
Create `tests/test_auth_validation.py` with tests for:
- Valid token validation
- Invalid token rejection
- Expired token rejection
- Malformed token rejection
- Token payload extraction
- Refresh token validation
- New access token generation
- Refresh token does not change

**✅ Verification:**
```bash
pytest tests/test_auth_validation.py -v

# Should pass all tests:
# test_validate_token_success
# test_validate_token_invalid_signature
# test_validate_token_expired
# test_validate_token_malformed
# test_validate_token_missing
# test_refresh_token_success
# test_refresh_token_invalid
# test_refresh_token_expired
# test_get_current_user_success
# test_get_current_user_invalid_token
```

**Protected Route Example:**
```python
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}
```

**Example cURL:**
```bash
# Validate token
curl -X POST http://localhost:8000/api/v1/auth/validate-token \
  -H "Content-Type: application/json" \
  -d '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

---

### Step 6: Add Documentation and Examples

**What to do:**
- Create API endpoint examples
- Create Python client examples
- Document error codes and messages
- Add architecture diagrams
- Document event structure for microservices
- Create deployment guides

**Files to create:**
- `docs/API_EXAMPLES.md` - API usage examples
- `docs/ERROR_CODES.md` - Complete error code reference
- `docs/EVENT_PUBLISHING.md` - Event structure and consumption
- `docs/DEPLOYMENT.md` - Production deployment guide
- `docs/DEVELOPMENT.md` - Development setup guide

**Create example scripts:**
- `examples/register_user.py` - Python registration example
- `examples/login_user.py` - Python login example
- `examples/validate_token.py` - Token validation example

**API Examples Include:**
- cURL examples for all endpoints
- Python requests examples
- JavaScript/TypeScript examples
- Postman collection (optional)

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth_register.py -v

# Run with markers
pytest -m "unit" -v
pytest -m "integration" -v

# Run in watch mode
ptw
```

### Test Structure

```
tests/
├── conftest.py                    # Pytest configuration & fixtures
├── fixtures.py                    # Shared fixtures
├── test_auth_register.py         # Registration tests
├── test_auth_login.py            # Login tests
└── test_auth_validation.py       # Token validation tests
```

### Test Fixtures (conftest.py)

```python
@pytest.fixture
def db_session() -> Session:
    """Provide test database session"""
    # Create test database
    # Yield session
    # Cleanup

@pytest.fixture
def client(db_session) -> TestClient:
    """Provide test FastAPI client"""
    # Override dependency
    # Return client

@pytest.fixture
def valid_user_data() -> dict:
    """Provide valid registration data"""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "password_confirmation": "SecurePassword123!"
    }

@pytest.fixture
def mock_jwt_token(valid_user: User) -> str:
    """Provide mocked JWT token"""
    return create_access_token({"sub": str(valid_user.id)})
```

### Unit Test Example

```python
# tests/test_auth_register.py
def test_register_success(client: TestClient, valid_user_data: dict):
    response = client.post("/api/v1/auth/register", json=valid_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "user_id" in data["data"]
    assert data["data"]["email"] == valid_user_data["email"]

def test_register_duplicate_email(client: TestClient, valid_user_data: dict, valid_user: User):
    # User already exists
    response = client.post("/api/v1/auth/register", json=valid_user_data)
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "DUPLICATE_EMAIL"
```

### Coverage Goals

- Unit tests: >80% code coverage
- All business logic covered
- All error paths tested
- Security functions thoroughly tested

---

## 📋 Error Response Format

All API responses follow a standard format:

### Success Response (2xx)

```json
{
  "success": true,
  "data": {
    // ... response data
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response (4xx, 5xx)

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {
      "field": "field_name",
      "issue": "Specific issue description"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `DUPLICATE_EMAIL` | 400 | Email already registered |
| `PASSWORD_MISMATCH` | 400 | Passwords do not match |
| `WEAK_PASSWORD` | 400 | Password does not meet requirements |
| `INVALID_EMAIL` | 400 | Invalid email format |
| `USER_NOT_FOUND` | 404 | User does not exist |
| `INVALID_CREDENTIALS` | 401 | Email or password incorrect |
| `INVALID_TOKEN` | 401 | Token is invalid or malformed |
| `EXPIRED_TOKEN` | 401 | Token has expired |
| `EMAIL_NOT_VERIFIED` | 403 | Email verification required |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## 🔔 Event Publishing

This service is designed for event-driven microservices architecture. Events are published on specific actions:

### Event Types

#### 1. UserRegisteredEvent
```python
{
    "event_type": "user.registered",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "email_verification_token": "token-for-verification"
    }
}
```

**Publishing:** Immediately after user registration
**Consumers:** Email service, analytics service

#### 2. UserLoggedInEvent
```python
{
    "event_type": "user.logged_in",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "ip_address": "192.168.1.1"
    }
}
```

**Publishing:** Immediately after successful login
**Consumers:** Analytics service, security service

#### 3. EmailVerifiedEvent
```python
{
    "event_type": "user.email_verified",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com"
    }
}
```

**Publishing:** After email verification
**Consumers:** User profile service, notifications service

### Event Publishing Implementation

```python
# app/events.py
class EventPublisher:
    @staticmethod
    async def publish(event: dict) -> None:
        """Publish event to message broker"""
        # Kafka, RabbitMQ, or event bus implementation
        pass

# In routers
async def register(...):
    user = create_user(...)
    await EventPublisher.publish({
        "event_type": "user.registered",
        "data": {"user_id": str(user.id), "email": user.email}
    })
```

### Integration with Other Services

Other microservices can consume events:

```python
# In another service
async def handle_user_registered(event: dict):
    user_id = event["data"]["user_id"]
    email = event["data"]["email"]
    # Send verification email, create profile, etc.
```

---

## 🚀 Deployment

### Docker Build

```bash
# Build image
docker build -t auth-service:1.0.0 .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/auth \
  -e JWT_SECRET_KEY=your-secret \
  auth-service:1.0.0
```

### Production Environment Variables

```bash
# .env.production
DATABASE_URL=postgresql://user:password@prod-db.example.com:5432/auth_prod
JWT_SECRET_KEY=generate-long-random-key-use-openssl
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
ALLOWED_ORIGINS=https://app.example.com
```

### Health Checks

The application includes health check endpoints for monitoring:

```bash
# Kubernetes health check
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "database": "connected",
  "service": "auth-service"
}
```

### Scaling Considerations

- **Stateless**: Service can be horizontally scaled
- **Database**: Use connection pooling (configured in SQLAlchemy)
- **JWT**: Tokens are self-contained (no session storage)
- **Events**: Use distributed message broker (Kafka, RabbitMQ)

---

## 🔮 Future Extensions

### Ready for Addition (No Core Changes)

1. **OAuth 2.0 / Social Login**
   - Add Google, GitHub providers
   - Modify User model with oauth_provider field
   - New endpoints: `/oauth/callback`

2. **Two-Factor Authentication**
   - Add TOTP support
   - New endpoints: `/2fa/setup`, `/2fa/verify`
   - Modify login flow

3. **Password Reset**
   - Email token-based reset
   - New endpoints: `/password/reset`, `/password/reset-confirm`

4. **User Profile Service**
   - Extend with profile fields (name, phone, etc.)
   - Create separate Profile model
   - Publish UserProfileUpdatedEvent

5. **Role-Based Access Control**
   - Add Role and Permission models
   - Modify JWT claims with roles
   - Create authorization middleware

6. **API Rate Limiting**
   - Add SlowAPI or similar
   - Rate limit per user_id or IP

7. **Email Verification Reminders**
   - Scheduled tasks with Celery
   - Event-driven email service

8. **Audit Logging**
   - Log all auth events to database
   - Integration with ElasticSearch/ELK

### Extension Points in Code

```python
# app/events.py - Add new event types
# app/models.py - Add fields to User model
# app/routers/auth.py - Add new endpoints
# app/dependencies.py - Add new dependency injection
# app/security.py - Add new security functions
```

---

## 📝 Dependencies

### Production (`requirements.txt`)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
alembic==1.13.0
```

### Development (`requirements-dev.txt`)

```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.12.0
flake8==6.1.0
mypy==1.7.1
```
