"""SQLAlchemy ORM models for the authentication service"""
import enum
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4
from sqlalchemy import String, Boolean, DateTime, func, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from app.models.Base import Base



class UserType(str, enum.Enum):
    """
        - sudo: full CRUD on users, including changing other users’ type.
        - admin: full CRUD on users except sudo users (cannot modify or delete sudo).
        - audit: read-only on user resources (GET list, GET detail).
        - client: no access to user admin endpoints at all.
    """
    SUDO = "sudo"
    ADMIN = "admin"
    AUDIT = "audit"
    CLIENT = "client"

AllowedUserType = Literal[UserType.ADMIN, UserType.AUDIT, UserType.CLIENT]


class User(Base):
    """User model for authentication"""
    __tablename__ = "user"
    
    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    type: Mapped[UserType] = mapped_column(
        Enum(UserType, name="user_type_enum"),
        default=UserType.CLIENT,
        nullable=False,
        index=True,
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, is_email_verified={self.is_email_verified})>"

