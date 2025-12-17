from app.config import settings
from app.email_config import conf
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.User import AllowedUserType, User, UserStatus
from app.models.OutboxEvent import OutboxEvent
from app.schemas.registration import UserRegisterRequest, UserRegisterResponse
from app.exceptions import DuplicateEmailError, PasswordMismatchError
from app.utils.tokens import generate_email_verification_token
from app.utils.logger import logging
from app.utils.mask_email import mask_email
from app.utils.password import hash_password
from app.events import EventTypes
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks



logger = logging.getLogger(__name__)
fm = FastMail(conf)  # Global FastMail instance


class RegisterService:
    @staticmethod
    async def register_user(
        request: UserRegisterRequest,
        db: Session,
        type: AllowedUserType,
        background_tasks: BackgroundTasks
    ) -> UserRegisterResponse:
        """
        Args:
            request: Registration request with email, password, and confirmation
            db: Database session
        """
        hidden_email = mask_email(request.email)

        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            logger.debug(
                f"[REGISTER_LOG] User already exists: {existing_user.id} - {hidden_email}"
            )
            raise DuplicateEmailError(request.email)

        if request.password != request.password_confirmation:
            raise PasswordMismatchError()

        password_hash = hash_password(request.password)
        user = User(
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            password_hash=password_hash,
            is_email_verified=False,
            email_verified_at=None,
            type=type,
            status=request.status
        )

        email_verification_token = generate_email_verification_token(
            str(user.id),
            user.email,
        )
        verification_url = f"{settings.SERVICE_URL}/api/v1/email/verify?token={email_verification_token}"


        logger.debug(f"[REGISTER_LOG] generate email link {verification_url}")

        message = MessageSchema(
            subject="[Jerry] Verify your email address",
            recipients=[user.email],
            body=f"Please verify your email: {verification_url}",
            subtype=MessageType.html,
            html=f"""
            <h2>Email Verification</h2>
            <p>Click the link below to verify your email:</p>
            <a href="{verification_url}">Verify Email</a>
            <p>This link expires in 15 minutes.</p>
            """
        )


        db.add(user)

        outbox_event = OutboxEvent(
            event_type=EventTypes.USER_REGISTERED,
            aggregate_id=str(user.id),
            payload={
                "user_id": str(user.id),
                "email": user.email,
                "is_email_verified": user.is_email_verified,
                "email_verification_token": email_verification_token,
            },
            status="pending",
        )
        db.add(outbox_event)

        try:
            db.commit()
            db.refresh(user)
            background_tasks.add_task(fm.send_message, message)
            logger.info(
                f"[REGISTER_LOG] User created and outbox event stored: {user.id} - {hidden_email}"
            )

        except IntegrityError as e:
            logger.error(
                f"[REGISTER_LOG] User was NOT created: {getattr(user, 'id', None)} - {hidden_email}"
            )
            db.rollback()
            error_str = str(e.orig) if hasattr(e, "orig") else str(e)
            # Check if it's a duplicate email error
            if "ix_user_email" in error_str or "duplicate key" in error_str.lower():
                raise DuplicateEmailError(request.email)
            raise

        return UserRegisterResponse(
            user_id=user.id,
            email=user.email,
            message="Registration successful. Please verify your email.",
        )