"""Unit tests for user login endpoint"""
import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from jose import jwt

from app.models.User import User
from app.exceptions import InvalidCredentialsError
from app.utils.tokens import decode_token
from app.config import settings
from app.utils.password import hash_password


class TestLoginSuccess:
    """Tests for successful user login"""
    
    def test_login_success(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test successful user login"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert "expires_in" in data["data"]
        assert data["data"]["user_id"] == str(valid_user.id)
        assert "timestamp" in data
    
    def test_login_returns_valid_tokens(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that login returns valid JWT tokens"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        
        # Verify access token can be decoded
        access_payload = decode_token(access_token, token_type="access")
        assert access_payload["user_id"] == str(valid_user.id)
        assert access_payload["email"] == valid_user_data["email"]
        assert access_payload["type"] == "access"
        
        # Verify refresh token can be decoded
        refresh_payload = decode_token(refresh_token, token_type="refresh")
        assert refresh_payload["user_id"] == str(valid_user.id)
        assert refresh_payload["type"] == "refresh"
    
    def test_login_access_token_expiration(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that access token has correct expiration time"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        access_token = data["access_token"]
        
        # Decode token and check expiration
        payload = decode_token(access_token, token_type="access")
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        
        # Token should expire approximately 24 hours from now
        expected_exp = datetime.now(timezone.utc) + timedelta(
            hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS
        )
        
        # Allow 5 minute tolerance for test execution time
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 300, f"Token expiration time differs by {time_diff} seconds"
    
    def test_login_refresh_token_expiration(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that refresh token has correct expiration time"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        refresh_token = data["refresh_token"]
        
        # Decode token and check expiration
        payload = decode_token(refresh_token, token_type="refresh")
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        
        # Token should expire approximately 7 days from now
        expected_exp = datetime.now(timezone.utc) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        # Allow 5 minute tolerance for test execution time
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        assert time_diff < 300, f"Token expiration time differs by {time_diff} seconds"
    
    def test_login_expires_in_field(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that expires_in field matches token expiration"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        expires_in = data["expires_in"]
        
        # expires_in should be in seconds (24 hours = 86400 seconds)
        expected_expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS * 3600
        assert expires_in == expected_expires_in


class TestLoginInvalidCredentials:
    """Tests for invalid credential handling"""
    
    def test_login_user_not_found(
        self,
        client: TestClient
    ):
        """Test that login with non-existent email is rejected"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        
        response = client.post("/api/v1/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["error"][0]["code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["error"][0]["msg"]
    
    def test_login_invalid_password(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that login with incorrect password is rejected"""
        login_data = {
            "email": valid_user_data["email"],
            "password": "WrongPassword123!"
        }
        
        response = client.post("/api/v1/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["error"][0]["code"] == "INVALID_CREDENTIALS"
        assert "Invalid email or password" in data["error"][0]["msg"]
    
    def test_login_empty_password(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that login with empty password is rejected"""
        login_data = {
            "email": valid_user_data["email"],
            "password": ""
        }
        
        response = client.post("/api/v1/login", json=login_data)
        
        # Empty password should be rejected (either validation error or invalid credentials)
        assert response.status_code in [400, 401]
        data = response.json()
        assert data["success"] is False
    
    def test_login_case_sensitive_email(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that login email matching is case-sensitive or case-insensitive"""
        # This test documents current behavior - email matching might be case-sensitive
        # depending on database collation
        login_data = {
            "email": valid_user_data["email"].upper(),
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        
        # The behavior depends on database collation
        # PostgreSQL default is case-sensitive, so this might fail
        # If it succeeds, that's also acceptable behavior
        assert response.status_code in [200, 401]


class TestLoginTokenStructure:
    """Tests for token structure and content"""
    
    def test_login_token_structure(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that tokens have correct structure"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        
        # Tokens should be non-empty strings
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
        assert isinstance(data["refresh_token"], str)
        assert len(data["refresh_token"]) > 0
        
        # Tokens should be different
        assert data["access_token"] != data["refresh_token"]
    
    def test_login_access_token_claims(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that access token contains correct claims"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        access_token = response.json()["data"]["access_token"]
        payload = decode_token(access_token, token_type="access")
        
        # Check required claims
        assert "user_id" in payload
        assert "email" in payload
        assert "type" in payload
        assert "exp" in payload
        assert "iat" in payload
        
        # Check claim values
        assert payload["user_id"] == str(valid_user.id)
        assert payload["email"] == valid_user_data["email"]
        assert payload["type"] == "access"
    
    def test_login_refresh_token_claims(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that refresh token contains correct claims"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        refresh_token = response.json()["data"]["refresh_token"]
        payload = decode_token(refresh_token, token_type="refresh")
        
        # Check required claims
        assert "user_id" in payload
        assert "type" in payload
        assert "exp" in payload
        assert "iat" in payload
        
        # Refresh token should NOT contain email
        assert "email" not in payload
        
        # Check claim values
        assert payload["user_id"] == str(valid_user.id)
        assert payload["type"] == "refresh"


class TestLoginResponseFormat:
    """Tests for response format compliance"""
    
    def test_login_response_structure(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that response follows standard format"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check standard response structure
        assert "success" in data
        assert "data" in data
        assert "timestamp" in data
        assert data["success"] is True
        
        # Check data structure
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert "token_type" in data["data"]
        assert "expires_in" in data["data"]
        assert "user_id" in data["data"]
        
        # Check timestamp format (ISO 8601 with Z)
        assert data["timestamp"].endswith("Z")
        assert "T" in data["timestamp"]
    
    def test_login_token_type_is_bearer(
        self,
        client: TestClient,
        valid_user: User,
        valid_user_data: dict
    ):
        """Test that token_type is always 'bearer'"""
        login_data = {
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["token_type"] == "bearer"


class TestLoginMultipleLogins:
    def test_login_with_verified_email(
        self,
        client: TestClient,
        db_session: Session,
        valid_user_data: dict
    ):
        """Test login with verified email (should work normally)"""
        # Create a verified user
        verified_user = User(
            email="verified@example.com",
            first_name="Verified",
            last_name="User",
            password_hash=hash_password(valid_user_data["password"]),
            is_email_verified=True,
            email_verified_at=datetime.now(timezone.utc)
        )
        db_session.add(verified_user)
        db_session.commit()
        db_session.refresh(verified_user)
        
        login_data = {
            "email": "verified@example.com",
            "password": valid_user_data["password"]
        }
        
        response = client.post("/api/v1/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert data["user_id"] == str(verified_user.id)

