from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.User import User, UserStatus
from app.schemas.login import UserLoginRequest, TokenResponse
from app.exceptions import InvalidCredentialsError, NotAllowed
from app.utils.tokens import create_access_token, create_refresh_token
from app.utils.logger import logging
from app.utils.mask_email import mask_email
from app.utils.password import verify_password
from app.config import settings


logger = logging.getLogger(__name__)


class LoginService:
    @staticmethod
    async def login_user(
        request: UserLoginRequest,
        db: Session,
    ) -> TokenResponse:
        """
        Authenticate a user and generate access and refresh tokens.

        Args:
            request: Login request with email and password
            db: Database session

        Returns:
            TokenResponse with access_token, refresh_token, and user_id

        Raises:
            InvalidCredentialsError: If email or password is incorrect
        """
        hidden_email = mask_email(request.email)

        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            logger.debug(
                f"[LOGIN_LOG] User not found: {hidden_email}"
            )
            raise InvalidCredentialsError()

        if not verify_password(request.password, user.password_hash):
            logger.debug(
                f"[LOGIN_LOG] Invalid password for user: {user.id} - {hidden_email}"
            )
            raise InvalidCredentialsError()
        if user.status != UserStatus.active:
            raise NotAllowed(f"User not allowed due status {user.status.value}")

        access_token = create_access_token(
            data={
                "user_id": str(user.id),
                "email": user.email,
            }
        )
        refresh_token = create_refresh_token(
            data={
                "user_id": str(user.id),
            }
        )

        try:
            db.commit()
            logger.info(
                f"[LOGIN_LOG] User logged in successfully: {user.id} - {hidden_email}"
            )
        except IntegrityError as e:
            logger.error(
                f"[LOGIN_LOG] Failed to store login event: {user.id} - {hidden_email}"
            )
            db.rollback()

        # Calculate expires_in in seconds (24 hours)
        expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS * 3600

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in,
            user_id=user.id,
        )
