"""Registration-related schemas"""
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator


class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    password_confirmation: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength.
        Requirements:
        - Minimum 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number
        - At least 1 special character
        """
        if len(v) < 8:
            raise ValueError("WEAK_PASSWORD","Password must be at least 8 characters long")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)
        
        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError(
                "INVALID_EMAIL",
                "Password must contain at least one uppercase letter,"
                "one lowercase letter, one number, and one special character"
            )
        
        return v
    


class UserRegisterResponse(BaseModel):
    """Response schema for user registration"""
    user_id: UUID
    email: str
    message: str

