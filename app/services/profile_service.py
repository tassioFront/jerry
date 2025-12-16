from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exceptions import DuplicateEmailError
from app.models.User import User
from app.models.OutboxEvent import OutboxEvent
from app.schemas.profile import UserProfileUpdateRequest, UserProfileResponse
from app.utils.logger import logging
from app.events import EventTypes


logger = logging.getLogger(__name__)


class ProfileService:

    @staticmethod
    async def update_profile(
        user: User,
        request: UserProfileUpdateRequest,
        db: Session,
    ) -> UserProfileResponse:
        """
        Update basic user profile information in a single atomic transaction.

        Args:
            user: The authenticated user to update.
            request: Profile update request with first_name, last_name, and email.
            db: Database session.
        """
        existing = (
            db.query(User)
            .filter(User.email == request.email, User.id != user.id)
            .first()
        )
        if existing:
            raise DuplicateEmailError(request.email)

        user.first_name = request.first_name
        user.last_name = request.last_name
        user.email = request.email

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
        except IntegrityError:
            db.rollback()
            raise

        return UserProfileResponse(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
