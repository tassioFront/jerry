"""Application-wide exception handlers."""
import ast
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.logger import logging


logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.info('exc')
    logger.info(exc.errors())
    """
    Handle Pydantic validation errors (RequestValidationError)
    """
    errors = exc.errors()
    # error_messages: list[str] = []
    custom_error: list[dict[str, Any]] = []

    logger.info("exception_handler[RequestValidationError] - init")

    for error in errors:
        logger.debug(error)

        error_msg: str = error.get("msg", "UNKNOWN_ERROR")

        if "Value error," in error_msg:
            # It is expected all ValueError instances raise a TYPE_ERROR and msg
            # such as ValueError(WEAK_PASSWORD, "weak password")
            logger.debug(
                "exception_handler[RequestValidationError] - ValueError instance raised"
            )
            msg = ast.literal_eval(error_msg.split("Value error,", 1)[1].strip())
            logger.debug(msg[0])
            error_obj = {
                "msg": msg[1:],
                "code": msg[0],
            }
            logger.debug("ERROR")
            custom_error.append(error_obj)

        elif error.get("type") == "missing":
            field: tuple = error["loc"]
            error_obj = {
                "msg": f"{field[1]} is required",
                "code": "MISSING_FIELD",
                "field": field[1],
            }
            logger.debug(
                "exception_handler[RequestValidationError] - It is missing type %s",
                field[1],
            )
            custom_error.append(error_obj)

        elif error.get("type") == "value_error":
            # eg. email format, auto value error raised by FastApi
            field: tuple = error["loc"]
            msg = error["msg"]
            error_obj = {
                "field": field[1],
                "msg": msg,
                "code": "VALIDATION_ERROR",
            }
            logger.debug(
                "exception_handler[RequestValidationError] - It is value_error type %s",
                field[1],
            )
            custom_error.append(error_obj)

        else:
            logger.debug(
                "exception_handler[RequestValidationError] - Unexpected type: %s",
                error.get("type"),
            )

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


