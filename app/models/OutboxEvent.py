"""Outbox event model for reliable event publishing (transactional outbox pattern)."""
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Any, Dict

from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.Base import Base


class OutboxEvent(Base):
    """Outbox event stored in the same database as domain data.

    Events are written in the same transaction as domain changes (e.g., user registration)
    and then later dispatched to the message broker by a separate process.
    """

    __tablename__ = "outbox_event"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    aggregate_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    retry_count: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<OutboxEvent(id={self.id}, event_type={self.event_type}, status={self.status})>"


