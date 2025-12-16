from uuid import UUID
from app.schemas.error_code import ErrorCode
from pydantic import BaseModel, EmailStr, field_validator, constr


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

    user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr

