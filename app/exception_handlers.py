"""Application-wide exception handlers."""
import ast
import json
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.logger import logging


logger = logging.getLogger(__name__)


def _parse_custom_value_error(message: str) -> dict[str, Any] | None:
    """
    Parse custom ValueError messages of the form:
        "Value error, ('ERROR_CODE', 'Message 1', ...)"
        eg. ValueError(WEAK_PASSWORD, "weak password")

    Returns a dict with our standardized structure or None
    if the message cannot be parsed.
    """
    if "Value error," not in message:
        return None

    try:
        raw_tuple = message.split("Value error,", 1)[1].strip()
        parsed = ast.literal_eval(raw_tuple)
        code, msgs = parsed
        return {
            "msg": msgs,
            "code": code,
        }
    except (ValueError, SyntaxError, TypeError):
        logger.exception(
            "Failed to parse custom ValueError message: %s",
            message,
        )
        return None


def _build_custom_error(error: dict[str, Any]) -> dict[str, Any] | None:
    """
    Translate a single Pydantic error dict into our custom error format.

    Returns None when the error type is not supported and should be ignored.
    """
    error_type = error.get("type")
    error_msg: str = error.get("msg", "UNKNOWN_ERROR")

    custom_value_error = _parse_custom_value_error(error_msg)
    if custom_value_error is not None:
        return custom_value_error

    if error_type == "missing":
        field: tuple = error["loc"]
        return {
            "msg": f"{field[1]} is required",
            "code": "MISSING_FIELD",
            "field": field[1],
        }

    if error_type == "value_error" or error_type == 'enum':
        # e.g. email format, auto value error raised by FastAPI/Pydantic
        field: tuple = error["loc"]
        return {
            "field": field[1],
            "msg": error_msg,
            "code": "VALIDATION_ERROR",
        }

    return None


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors (RequestValidationError)
    """
    custom_error: list[dict[str, Any]] = []

    for error in exc.errors():
        error_obj = _build_custom_error(error)
        if error_obj is not None:
            custom_error.append(error_obj)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": custom_error,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        },
    )

def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the given FastAPI app."""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


