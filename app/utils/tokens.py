"""Token generation utilities"""
from datetime import timedelta
from app.security import create_access_token


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

