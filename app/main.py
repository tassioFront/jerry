"""FastAPI application initialization"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from app.config import settings
from app.routers import auth
from app.exceptions import AuthException, DuplicateEmailError


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

# Include routers
app.include_router(auth.router)


# Exception handler for custom AuthException
@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    """Handle custom authentication exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
    )


# Exception handler for validation errors (Pydantic)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors - convert 422 to 400"""
    # Extract error messages from validation errors
    errors = exc.errors()
    error_messages = []
    error_code = "VALIDATION_ERROR"
    
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        msg = error.get("msg", "Validation error")
        error_messages.append(msg)
        
        # Determine specific error code based on message content
        msg_lower = msg.lower()
        if "password confirmation" in msg_lower or "does not match" in msg_lower:
            error_code = "PASSWORD_MISMATCH"
        elif "password" in msg_lower and ("weak" in msg_lower or "must contain" in msg_lower or "at least" in msg_lower):
            error_code = "WEAK_PASSWORD"
        elif "email" in msg_lower or "value is not a valid" in msg_lower:
            error_code = "INVALID_EMAIL"
    
    message = "; ".join(error_messages) if error_messages else "Validation error"
    
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": {}
            },
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
    )


# Exception handler for SQLAlchemy IntegrityError (duplicate keys, etc.)
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (e.g., duplicate email)"""
    error_str = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Check if it's a duplicate email error
    if "ix_user_email" in error_str or "duplicate key" in error_str.lower():
        # Try to extract email from the request body
        email = "unknown"
        try:
            body = await request.json()
            email = body.get("email", "unknown")
        except:
            pass
        
        # Return DuplicateEmailError response format
        duplicate_error = DuplicateEmailError(email)
        return JSONResponse(
            status_code=duplicate_error.status_code,
            content={
                "success": False,
                "error": duplicate_error.detail,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }
        )
    
    # For other integrity errors, return generic error
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": "INTEGRITY_ERROR",
                "message": "Database integrity constraint violation",
                "details": {}
            },
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
    )


@app.get("/health")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "database": "connected",  # Will be updated when database is implemented
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
    }



