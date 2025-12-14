"""Authentication endpoints: register, login, token validation"""
from datetime import datetime, timezone
from fastapi import APIRouter, status
from app.dependencies import DatabaseSession
from app.schemas.common import ResponseModel
from app.schemas.registration import UserRegisterRequest, UserRegisterResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[UserRegisterResponse]
)
async def register(
    request: UserRegisterRequest,
    db: DatabaseSession
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
    # Delegate business logic to service layer
    response_data = await AuthService.register_user(request, db)
    
    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z"
    )

