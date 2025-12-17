from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.dependencies import DatabaseSession, NotClientOnly, get_current_user, require_user_active_status
from app.schemas.common import ResponseModel
from app.schemas.profile import UserProfileUpdateRequest, UserProfileResponse, UserProfileGetUsersRequest
from app.services.profile_service import ProfileService
from app.models.User import User
from app.schemas.pagination import PaginatedResponse

from typing import TypeVar

T = TypeVar("T")

router = APIRouter(tags=["authentication"])

@router.put(
    "/v1/profile/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[UserProfileResponse],
)
async def update_profile(
    user_id: UUID,
    request: UserProfileUpdateRequest,
    db: DatabaseSession,
    current_user: User = Depends(get_current_user),
    status: User = Depends(require_user_active_status()),
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
        user_id=user_id
    )

    return ResponseModel[UserProfileResponse](
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )



@router.get(
    "/v1/profile/internal",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[PaginatedResponse[UserProfileResponse]],
)
async def list_users(
    request: UserProfileGetUsersRequest,
    db: DatabaseSession,
    current_user: User = Depends(NotClientOnly),
    status: User = Depends(require_user_active_status()),
) -> ResponseModel[PaginatedResponse[UserProfileResponse]]:
    response_data = await ProfileService.internal_get_users(
        request=request,
        db=db,
    )

    return ResponseModel(
        success=True,
        data=response_data,
        timestamp=datetime.now(timezone.utc).isoformat() + "Z",
    )
