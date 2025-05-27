import traceback

from fastapi import Request
from fastapi.exceptions import (HTTPException, RequestValidationError,
                                ResponseValidationError)
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

"""Custom Exception Handler for FastAPI HTTPException"""


def custom_http_exception_handler(request: Request, exc: HTTPException):
    print("🔥 HTTP exception:", exc.detail)
    print(exc.status_code)

    if exc.status_code == 500:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": "An internal server error occured. Please try again later.",
                },
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.status_code, "message": exc.detail},
        },
    )


"""Custom Exception Handler for Starlette"""


def custom_http_starlette_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    print("🔥 HTTP[starlette] exception:", exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.status_code, "message": exc.detail},
        },
    )


"""Custom Exception Handler for FastAPI ResponseValidationError"""


def custom_http_response_validation_exception_handler(
    request, Request, exc: ResponseValidationError
):
    print("🔥 Response Validation error:", exc.errors)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An internal server error occured. Please try again later.",
            },
        },
    )


"""Custom Exception Handler for FastAPI RequestValidationError"""


def custom_http_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    print("🔥 Request Validation error:", exc.errors)

    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Request validation failed. Check input fields.",
                "data": {"errors": errors},
            },
        },
    )


"""Custom Exception Handler for Exception"""


def custom_http_internal_server_error_handler(request: Request, exc: Exception):
    print("🔥 Internal Server error:", traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An internal server error occured. Please try again later.",
            },
        },
    )


"""Custom Exception Handler for SQLAlchemy IntegrityError"""


def custom_db_integrity_error_handler(request: Request, exc: IntegrityError):
    print("🔥 Database Integrity error:", exc.detail)

    error_message = str(exc.orig).split("\n")[0]

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "code": 400,
                "message": "Resource integrity error.",
                "details": error_message,
            },
        },
    )
