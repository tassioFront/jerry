"""FastAPI dependencies for dependency injection"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

# Type alias for database session dependency
DatabaseSession = Annotated[Session, Depends(get_db)]

