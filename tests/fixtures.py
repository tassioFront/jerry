"""Shared test fixtures for authentication tests"""
import pytest
from uuid import uuid4
from app.models.User import User
from app.utils.password import hash_password


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing"""
    return {
        "email": "sample@example.com",
        "password": "TestPassword123!",
        "password_confirmation": "TestPassword123!",
        "first_name": "nice",
        "last_name": "name"
    }


@pytest.fixture
def weak_password_data() -> dict:
    """User data with weak password"""
    return {
        "email": "weak@example.com",
        "password": "weak",
        "password_confirmation": "weak",
        "first_name": "nice",
        "last_name": "name"
    }


@pytest.fixture
def mismatched_password_data() -> dict:
    """User data with mismatched passwords"""
    return {
        "email": "mismatch@example.com",
        "password": "SecurePassword123!",
        "password_confirmation": "DifferentPassword123!",
        "first_name": "nice",
        "last_name": "name"
    }


@pytest.fixture
def invalid_email_data() -> dict:
    """User data with invalid email format"""
    return {
        "email": "not-an-email",
        "password": "SecurePassword123!",
        "password_confirmation": "SecurePassword123!",
        "first_name": "nice",
        "last_name": "name"
    }

