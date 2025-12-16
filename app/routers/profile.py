from datetime import datetime, timezone

from fastapi import APIRouter, status, Depends

from app.dependencies import DatabaseSession, get_current_user
from app.schemas.common import ResponseModel
from app.schemas.user import UserProfileUpdateRequest, UserProfileResponse
from app.services.profile_service import ProfileService
from app.models.User import User

router = APIRouter(tags=["authentication"])

@router.put(
    "/v1/profile",
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
    response_data = await ProfileService.update_profile(
        user=current_user,
        request=request,
        db=db,
    )

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )

