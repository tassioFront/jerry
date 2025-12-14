"""Email verification schemas"""
from uuid import UUID
from pydantic import BaseModel


class VerifyEmailRequest(BaseModel):
    """Request schema for email verification"""
    token: str


class VerifyEmailResponse(BaseModel):
    """Response schema for email verification"""
    message: str
    user_id: UUID

