from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI(
    title="Auth Service",
    description="FastAPI Authentication Microservice",
    version=os.getenv("SERVICE_VERSION", "1.0.0")
)


@app.get("/")
def read_root():
    return {"message": "Auth Service API"}


@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": os.getenv("SERVICE_NAME", "SERVICE_NAME"),
        "version": os.getenv("SERVICE_VERSION", "1.0.0"),
        "database": "connected",  # Will be updated when database is implemented
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

