"""Import ORM models so Alembic and the application can discover them."""

from app.models.User import User  # noqa: F401
from app.models.OutboxEvent import OutboxEvent  # noqa: F401

