"""Authentication endpoints: register, login, token validation, profile update"""
from datetime import datetime, timezone

from fastapi import APIRouter, status, Depends

from app.dependencies import DatabaseSession, get_current_user
from app.schemas.common import ResponseModel
from app.schemas.registration import UserRegisterRequest, UserRegisterResponse
from app.schemas.user import UserProfileUpdateRequest, UserProfileResponse
from app.services.auth_service import AuthService
from app.models.User import User

router = APIRouter(prefix="/v1/auth", tags=["authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[UserRegisterResponse],
)
async def register(
    request: UserRegisterRequest,
    db: DatabaseSession,
) -> ResponseModel[UserRegisterResponse]:
    """
    Register a new user.

    Args:
        request: Registration request with email, password, and confirmation
        db: Database session

    Returns:
        Response with user_id and success message

    Raises:
        DuplicateEmailError: If email is already registered
        PasswordMismatchError: If passwords don't match
        ValidationError: If validation fails
    """
    response_data = await AuthService.register_user(request, db)

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )


@router.put(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[UserProfileResponse],
)
async def update_profile(
    request: UserProfileUpdateRequest,
    db: DatabaseSession,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[UserProfileResponse]:
    """
    Update the authenticated user's basic profile information.

    This operation is atomic and transactional: either all fields are updated
    and the corresponding outbox event is written, or none of them are.
    """
    response_data = await AuthService.update_profile(
        user=current_user,
        request=request,
        db=db,
    )

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )

