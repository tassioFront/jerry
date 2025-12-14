"""Common schemas used across the application"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# Generic type for response wrapper
T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None
    timestamp: str

