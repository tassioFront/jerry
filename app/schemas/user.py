"""User-related schemas"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response schema for user information"""
    id: UUID
    email: str
    first_name: str
    last_name: str
    is_email_verified: bool
    email_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

