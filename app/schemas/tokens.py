"""Token validation and refresh schemas"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class ValidateTokenRequest(BaseModel):
    """Request schema for token validation"""
    token: str


class TokenValidationResponse(BaseModel):
    """Response schema for token validation"""
    is_valid: bool
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    """Request schema for token refresh"""
    refresh_token: str

