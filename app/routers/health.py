from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings


router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "database": "connected",  # Will be updated when database is implemented
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
    }
