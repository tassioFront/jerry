"""FastAPI application initialization"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings


app = FastAPI(
    title="Auth Service",
    description="FastAPI Authentication Microservice",
    version=settings.SERVICE_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "database": "connected",  # Will be updated when database is implemented
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }



