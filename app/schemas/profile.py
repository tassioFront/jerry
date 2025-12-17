from uuid import UUID
from typing import Optional
from app.models.User import UserStatus, UserType
from app.schemas.error_code import ErrorCode
from pydantic import BaseModel, EmailStr, field_validator, constr, Field, ConfigDict


class UserProfileUpdateRequest(BaseModel):
    """Request schema for updating basic user profile information."""

    first_name: constr(strip_whitespace=True, min_length=1)
    last_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_single_word_name(cls, v: str) -> str:
        """
        Ensure first_name and last_name are single words without spaces.
        """
        if " " in v:
            raise ValueError(
                ErrorCode.MAX_ALLOWED_WORDS,
                "Name fields must be a single word without spaces",
            )
        return v


class UserProfileResponse(BaseModel):
    """Response schema for updated user profile information."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    type: UserType



class UserProfileGetUsersRequest(BaseModel):
    page: int = Field(1, ge=1, description="Page number starting at 1")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    email: Optional[str] = Field(None, description="Optional filter by email (substring or exact)")
    type: Optional[str] = Field(None, description='Optional filter by user type: "sudo", "admin", "audit", "client"')
    user_id: Optional[UUID] = Field(None, description="Optional filter by specific user id")


