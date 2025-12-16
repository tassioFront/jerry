from datetime import datetime, timezone

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.exception_handlers import register_exception_handlers
from app.exceptions import AuthException, DuplicateEmailError
from app.routers import register, health, login, profile

app = FastAPI(
    title="Auth Service",
    description="FastAPI Authentication Microservice",
    version=settings.SERVICE_VERSION
)

prefix = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
prefix.include_router(register.router)
prefix.include_router(login.router)
prefix.include_router(profile.router)
prefix.include_router(health.router)

app.include_router(prefix)

# Register global exception handlers
register_exception_handlers(app)

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


# Exception handler for SQLAlchemy IntegrityError (duplicate keys, etc.)
# @app.exception_handler(IntegrityError)
# async def integrity_error_handler(request: Request, exc: IntegrityError):
#     """Handle database integrity errors (e.g., duplicate email)"""
#     error_str = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
#     # Check if it's a duplicate email error
#     if "ix_user_email" in error_str or "duplicate key" in error_str.lower():
#         # Try to extract email from the request body
#         email = "unknown"
#         try:
#             body = await request.json()
#             email = body.get("email", "unknown")
#         except:
#             pass
        
#         # Return DuplicateEmailError response format
#         duplicate_error = DuplicateEmailError(email)
#         return JSONResponse(
#             status_code=duplicate_error.status_code,
#             content={
#                 "success": False,
#                 "error": duplicate_error.detail,
#                 "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
#             }
#         )
    
#     # For other integrity errors, return generic error
#     return JSONResponse(
#         status_code=400,
#         content={
#             "success": False,
#             "error": {
#                 "code": "INTEGRITY_ERROR",
#                 "message": "Database integrity constraint violation",
#                 "details": {}
#             },
#             "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
#         }
#     )






