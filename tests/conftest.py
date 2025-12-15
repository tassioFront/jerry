"""Pytest configuration and shared fixtures"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.models.User import User
from app.utils.password import hash_password

# Import fixtures from fixtures.py
from tests.fixtures import (
    sample_user_data,
    weak_password_data,
    mismatched_password_data,
    invalid_email_data
)


# Test database URL - use PostgreSQL in Docker, SQLite locally
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test.db"
)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Provide a test database session.
    Creates a new database for each test and cleans up after.
    """
    # Create test engine
    connect_args = {}
    if "sqlite" in TEST_DATABASE_URL:
        connect_args = {"check_same_thread": False}
    
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args=connect_args,
        echo=False
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    session = TestingSessionLocal()
    
    # Clean up any existing data at the start of each test
    try:
        session.query(User).delete()
        session.commit()
    except Exception:
        session.rollback()
    
    try:
        yield session
    finally:
        # Clean up: delete all data before closing
        try:
            session.query(User).delete()
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
            # Only drop tables if using SQLite
            if "sqlite" in TEST_DATABASE_URL:
                Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Provide a test FastAPI client with database dependency override.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Don't close session here, let db_session fixture handle it
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def valid_user_data() -> dict:
    """Provide valid registration data"""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "password_confirmation": "SecurePassword123!"
    }


@pytest.fixture
def valid_user(db_session: Session, valid_user_data: dict) -> User:
    """Create and return a valid user in the database"""
    # Check if user already exists (from previous test or fixture)
    existing_user = db_session.query(User).filter(
        User.email == valid_user_data["email"]
    ).first()
    
    if existing_user:
        return existing_user
    
    # Create new user
    user = User(
        first_name="Existing",
        last_name="User",
        email=valid_user_data["email"],
        password_hash=hash_password(valid_user_data["password"]),
        is_email_verified=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

