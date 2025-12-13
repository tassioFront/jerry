"""Custom exceptions for the authentication service"""
from typing import Optional
from fastapi import HTTPException, status


class AuthException(HTTPException):
    """Base exception for authentication errors"""
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail={
            "code": error_code,
            "message": message,
            "details": details or {}
        })


class ValidationError(AuthException):
    """Input validation error"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class DuplicateEmailError(AuthException):
    """Email already registered"""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="DUPLICATE_EMAIL",
            message=f"Email {email} is already registered",
            details={"field": "email", "issue": "Email already exists"}
        )


class PasswordMismatchError(AuthException):
    """Password confirmation does not match"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="PASSWORD_MISMATCH",
            message="Password confirmation does not match",
            details={"field": "password_confirmation", "issue": "Passwords do not match"}
        )


class WeakPasswordError(AuthException):
    """Password does not meet requirements"""
    def __init__(self, message: str = "Password does not meet security requirements"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="WEAK_PASSWORD",
            message=message,
            details={"field": "password", "issue": "Password too weak"}
        )


class InvalidEmailError(AuthException):
    """Invalid email format"""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_EMAIL",
            message=f"Invalid email format: {email}",
            details={"field": "email", "issue": "Invalid email format"}
        )


class UserNotFoundError(AuthException):
    """User does not exist"""
    def __init__(self, email: Optional[str] = None):
        message = "User not found"
        if email:
            message = f"User with email {email} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="USER_NOT_FOUND",
            message=message,
            details={"field": "email", "issue": "User does not exist"}
        )


class InvalidCredentialsError(AuthException):
    """Invalid email or password"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            details={"field": "credentials", "issue": "Email or password incorrect"}
        )


class InvalidTokenError(AuthException):
    """Token is invalid or malformed"""
    def __init__(self, message: str = "Invalid or malformed token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN",
            message=message,
            details={"field": "token", "issue": "Token is invalid"}
        )


class ExpiredTokenError(AuthException):
    """Token has expired"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="EXPIRED_TOKEN",
            message="Token has expired",
            details={"field": "token", "issue": "Token expired"}
        )


class EmailNotVerifiedError(AuthException):
    """Email verification required"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="EMAIL_NOT_VERIFIED",
            message="Email verification required",
            details={"field": "email", "issue": "Email not verified"}
        )


class InternalError(AuthException):
    """Internal server error"""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_ERROR",
            message=message,
            details={}
        )

