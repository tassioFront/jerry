from datetime import datetime, timezone

from app.models import User
from app.models.User import UserType
from fastapi import APIRouter, status, Depends

from app.dependencies import DatabaseSession, NotClientOnly
from app.schemas.common import ResponseModel
from app.schemas.registration import InternalUserRegisterRequest, UserRegisterRequest, UserRegisterResponse
from app.services.register_service import RegisterService

router = APIRouter(tags=["authentication"])


@router.post(
    "/v1/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[UserRegisterResponse],
)
async def register(
    request: UserRegisterRequest,
    db: DatabaseSession,
) -> ResponseModel[UserRegisterResponse]:
    """
    Register a new user: client type only.

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
    response_data = await RegisterService.register_user(request, db, UserType.CLIENT)

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )

@router.post(
    "/v1/register/internal",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[UserRegisterResponse],
)
async def internal_register(
    request: InternalUserRegisterRequest,
    db: DatabaseSession,
    current_user: User = Depends(NotClientOnly),
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
    response_data = await RegisterService.register_user(request, db, request.type)

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )
