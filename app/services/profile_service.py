from uuid import UUID
from app.schemas.error_code import ErrorCode
from app.schemas.pagination import PaginatedResponse
from app.utils.paginator import paginate_query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exceptions import AuthException, DuplicateEmailError, NotAllowed
from app.models.User import User
from app.models.OutboxEvent import OutboxEvent
from app.schemas.profile import UserProfileGetUsersRequest, UserProfileUpdateRequest, UserProfileResponse
from app.utils.logger import logging
from app.events import EventTypes
from fastapi import Query, status


logger = logging.getLogger(__name__)


class ProfileService:

    @staticmethod
    async def update_profile(
        user: User,
        request: UserProfileUpdateRequest,
        db: Session,
        user_id: UUID # id from url
    ) -> UserProfileResponse:
        """
        Update basic user profile information in a single atomic transaction.

        Args:
            user: The authenticated user to update.
            request: Profile update request with first_name, last_name, and email.
            db: Database session.
        """
        if (user_id != user.id):
            raise NotAllowed()
        existing = (
            db.query(User)
            .filter(User.email == request.email, User.id != user.id)
            .first()
        )
        if existing:
            raise DuplicateEmailError(request.email)

        user.first_name = request.first_name
        user.last_name = request.last_name
        #[to-do] update email only if it is provided
        # user.email = request.email

        outbox_event = OutboxEvent(
            event_type=getattr(
                EventTypes,
                "USER_PROFILE_UPDATED",
                "user.profile_updated",
            ),
            aggregate_id=str(user.id),
            payload={
                "user_id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            status="pending",
        )

        try:
            db.add(user)
            db.add(outbox_event)
            db.commit()
            db.refresh(user)
            logger.debug(f"user {user.id} update")
        except IntegrityError:
            logger.debug(f"user {user.id} NOT update")
            db.rollback()
            raise

        return UserProfileResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            type=user.type,
            status=user.status
        )

    @staticmethod
    async def internal_get_users(
        request: UserProfileGetUsersRequest,
        db: Session,
    ) -> PaginatedResponse[UserProfileResponse]:
        q: Query = db.query(User).order_by(User.created_at.desc())
        return paginate_query(query=q,page=request.page, page_size=request.page_size, schema_cls=UserProfileResponse)