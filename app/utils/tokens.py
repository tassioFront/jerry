from datetime import datetime, timedelta, timezone
from typing import Literal, Optional, Dict, Any
from jose import JWTError, jwt
from app.config import settings
from app.exceptions import InvalidTokenError, ExpiredTokenError

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary containing token claims (typically user_id and email)
        expires_delta: Optional custom expiration time. If not provided, uses
                      JWT_ACCESS_TOKEN_EXPIRE_HOURS from settings
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS
        )
    
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc)
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Dictionary containing token claims (typically user_id only)
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.now(timezone.utc)
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str, token_type: Literal['access', 'refresh'] = "access") -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Dictionary containing decoded token claims
        
    Raises:
        InvalidTokenError: If token is invalid or malformed
        ExpiredTokenError: If token has expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        if payload.get("type") != token_type:
            raise InvalidTokenError(f"Token type mismatch. Expected {token_type}")
        
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if exp_datetime < datetime.now(timezone.utc):
                raise ExpiredTokenError()
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError()
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token (alias for decode_token with access type).
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Dictionary containing decoded token claims
        
    Raises:
        InvalidTokenError: If token is invalid or malformed
        ExpiredTokenError: If token has expired
    """
    return decode_token(token, token_type="access")


def generate_email_verification_token(user_id: str, email: str) -> str:
    """
    Generate an email verification token.
    
    Args:
        user_id: User UUID as string
        email: User email
        
    Returns:
        JWT token for email verification
    """
    data = {
        "user_id": user_id,
        "email": email,
        "purpose": "email_verification"
    }
    return create_access_token(data, expires_delta=timedelta(days=7))
