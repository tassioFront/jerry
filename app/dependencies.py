"""FastAPI dependencies for dependency injection"""
from typing import Annotated

from typing import Iterable, Callable
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.User import User, UserType
from app.utils.tokens import verify_token
from app.exceptions import InvalidTokenError, UserNotFoundError

DatabaseSession = Annotated[Session, Depends(get_db)]


security_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the current authenticated user from a Bearer token.

    Expects a JWT access token with a "user_id" claim and loads the
    corresponding User from the database.
    """
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise InvalidTokenError()


    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError()

    return user


def require_user_type(allowed_types: Iterable[UserType]) -> Callable:
    allowed_set = set[UserType](allowed_types)

    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.type not in allowed_set:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions",
            )
        return current_user

    return checker

NotClientOnly = require_user_type([UserType.SUDO, UserType.ADMIN, UserType.AUDIT])
AdminLevel = require_user_type([UserType.SUDO, UserType.ADMIN])

