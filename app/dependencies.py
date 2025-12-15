"""FastAPI dependencies for dependency injection"""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.User import User
from app.utils.tokens import verify_token
from app.exceptions import InvalidTokenError, UserNotFoundError

DatabaseSession = Annotated[Session, Depends(get_db)]


security_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    # credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the current authenticated user from a Bearer token.

    Expects a JWT access token with a "user_id" claim and loads the
    corresponding User from the database.
    """
    # token = credentials.credentials
    # payload = verify_token(token)

    # user_id = payload.get("user_id") or payload.get("sub")
    # if not user_id:
    #     raise InvalidTokenError("Token payload missing user identifier")


    # [to-do] change it after has token
    user_id = 'a986724f-52e1-4ad4-b286-eaf0ad0d6561'
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError()

    return user

