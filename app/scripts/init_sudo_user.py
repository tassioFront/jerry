from uuid import UUID

from app.database import SessionLocal
from app.models.User import User, UserType
from app.config import settings
from app.utils.logger import logging
from app.utils.password import hash_password


logger = logging.getLogger(__name__)


def get_user_by_email(email: str):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).first()
        return user


def init_sudo_user():
        logger.info('[init_sudo_user]')

        exist = get_user_by_email(settings.SUDO_USER_EMAIL)

        if exist:
            logger.info('[init_sudo_user] skipped. User already exits')
            return

        user = User(
            email=settings.SUDO_USER_EMAIL,
            first_name=settings.SUDO_USER_NAME,
            last_name=settings.SUDO_USER_LAST_NAME,
            password_hash=hash_password(settings.SUDO_USER_PASS_WORD),
            is_email_verified=False,
            email_verified_at=None,
            type=UserType.SUDO
        )
        with SessionLocal() as db:
            db.add(user)
            db.commit()
            logger.info('[init_sudo_user] end. User created')
    


init_sudo_user()