from datetime import datetime, timezone

from fastapi import APIRouter, status

from app.dependencies import DatabaseSession
from app.schemas.common import ResponseModel
from app.schemas.login import UserLoginRequest, TokenResponse
from app.services.login_service import LoginService
from app.models.User import User

router = APIRouter(tags=["authentication"])


@router.post(
    "/v1/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[TokenResponse],
)
async def login(
    request: UserLoginRequest,
    db: DatabaseSession,
) -> ResponseModel[TokenResponse]:
    """
    Authenticate a user and return access and refresh tokens.

    Args:
        request: Login request with email and password
        db: Database session

    Returns:
        Response with access_token, refresh_token, and user_id

    Raises:
        InvalidCredentialsError: If email or password is incorrect
    """
    response_data = await LoginService.login_user(request, db)

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )
