"""Authentication business logic"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.schemas.registration import UserRegisterRequest, UserRegisterResponse
from app.security import hash_password
from app.exceptions import DuplicateEmailError, PasswordMismatchError
from app.utils.tokens import generate_email_verification_token
from app.events import EventPublisher, EventTypes


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    async def register_user(
        request: UserRegisterRequest,
        db: Session
    ) -> UserRegisterResponse:
        """
        Args:
            request: Registration request with email, password, and confirmation
            db: Database session
        """
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise DuplicateEmailError(request.email)
        
        if request.password != request.password_confirmation:
            raise PasswordMismatchError()
        
        password_hash = hash_password(request.password)
        user = User(
            email=request.email,
            password_hash=password_hash,
            is_email_verified=False,
            email_verified_at=None
        )
        
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
        except IntegrityError as e:
            db.rollback()
            error_str = str(e.orig) if hasattr(e, 'orig') else str(e)
            # Check if it's a duplicate email error
            if "ix_user_email" in error_str or "duplicate key" in error_str.lower():
                raise DuplicateEmailError(request.email)
            raise
        
        email_verification_token = generate_email_verification_token(
            str(user.id),
            user.email
        )
        
        await EventPublisher.publish(
            EventTypes.USER_REGISTERED,
            {
                "user_id": str(user.id),
                "email": user.email,
                "email_verification_token": email_verification_token
            }
        )
        
        return UserRegisterResponse(
            user_id=user.id,
            email=user.email,
            message="Registration successful. Please verify your email."
        )

