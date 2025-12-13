"""Unit tests for security functions: password hashing and JWT tokens"""
import pytest
from datetime import timedelta, datetime, timezone
from jose import jwt
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token
)
from app.exceptions import InvalidTokenError, ExpiredTokenError
from app.config import settings


class TestPasswordHashing:
    """Tests for password hashing and verification"""
    
    def test_hash_password(self):
        """Test that password hashing produces a different string"""
        password = "SecurePassword123!"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt hash format
    
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)"""
        password = "SecurePassword123!"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        
        # Hashes should be different due to salt
        assert hashed1 != hashed2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "SecurePassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self):
        """Test password verification with empty password"""
        password = "SecurePassword123!"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False


class TestAccessToken:
    """Tests for access token creation and validation"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_custom_expiry(self):
        """Test access token creation with custom expiration"""
        data = {"user_id": "123", "email": "test@example.com"}
        custom_expiry = timedelta(hours=1)
        token = create_access_token(data, expires_delta=custom_expiry)
        
        # Decode to verify expiration
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + custom_expiry
        
        # Allow 5 second tolerance
        assert abs((exp - expected_exp).total_seconds()) < 5
    
    def test_decode_valid_token(self):
        """Test decoding a valid access token"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = decode_token(token, token_type="access")
        
        assert payload["user_id"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_decode_expired_token(self):
        """Test decoding an expired token raises ExpiredTokenError"""
        data = {"user_id": "123", "email": "test@example.com"}
        # Create token with very short expiration
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(ExpiredTokenError):
            decode_token(token, token_type="access")
    
    def test_decode_invalid_token(self):
        """Test decoding an invalid token raises InvalidTokenError"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(InvalidTokenError):
            decode_token(invalid_token, token_type="access")
    
    def test_decode_token_wrong_secret(self):
        """Test decoding token with wrong secret key raises InvalidTokenError"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        # Temporarily change the secret key to simulate wrong secret
        original_secret = settings.JWT_SECRET_KEY
        try:
            settings.JWT_SECRET_KEY = "wrong-secret-key"
            # Now decode_token should fail because the secret doesn't match
            with pytest.raises(InvalidTokenError):
                decode_token(token, token_type="access")
        finally:
            # Restore original secret
            settings.JWT_SECRET_KEY = original_secret
    
    def test_decode_token_wrong_type(self):
        """Test decoding access token as refresh token raises InvalidTokenError"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)  # Creates access token
        
        with pytest.raises(InvalidTokenError):
            decode_token(token, token_type="refresh")  # Expecting refresh token


class TestRefreshToken:
    """Tests for refresh token creation and validation"""
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"user_id": "123"}
        token = create_refresh_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_valid_refresh_token(self):
        """Test decoding a valid refresh token"""
        data = {"user_id": "123"}
        token = create_refresh_token(data)
        
        payload = decode_token(token, token_type="refresh")
        
        assert payload["user_id"] == "123"
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_refresh_token_expiration(self):
        """Test that refresh token has correct expiration (7 days)"""
        data = {"user_id": "123"}
        token = create_refresh_token(data)
        
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        # Allow 5 second tolerance
        assert abs((exp - expected_exp).total_seconds()) < 5
    
    def test_decode_expired_refresh_token(self):
        """Test decoding an expired refresh token raises ExpiredTokenError"""
        data = {"user_id": "123"}
        # Manually create expired token
        to_encode = data.copy()
        to_encode.update({
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            "type": "refresh",
            "iat": datetime.now(timezone.utc) - timedelta(days=8)
        })
        token = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        with pytest.raises(ExpiredTokenError):
            decode_token(token, token_type="refresh")


class TestVerifyToken:
    """Tests for verify_token function (alias for decode_token with access type)"""
    
    def test_verify_token_success(self):
        """Test verify_token with valid access token"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        
        assert payload["user_id"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
    
    def test_verify_token_invalid(self):
        """Test verify_token with invalid token raises InvalidTokenError"""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(InvalidTokenError):
            verify_token(invalid_token)
    
    def test_verify_token_expired(self):
        """Test verify_token with expired token raises ExpiredTokenError"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(ExpiredTokenError):
            verify_token(token)


class TestTokenStructure:
    """Tests for token structure and claims"""
    
    def test_access_token_contains_required_fields(self):
        """Test that access token contains all required fields"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = decode_token(token, token_type="access")
        
        assert "user_id" in payload
        assert "email" in payload
        assert "type" in payload
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_refresh_token_contains_required_fields(self):
        """Test that refresh token contains all required fields"""
        data = {"user_id": "123"}
        token = create_refresh_token(data)
        
        payload = decode_token(token, token_type="refresh")
        
        assert "user_id" in payload
        assert "type" in payload
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_access_token_expiration_time(self):
        """Test that access token expires in correct time (24 hours)"""
        data = {"user_id": "123", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(
            hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS
        )
        
        # Allow 5 second tolerance
        assert abs((exp - expected_exp).total_seconds()) < 5



