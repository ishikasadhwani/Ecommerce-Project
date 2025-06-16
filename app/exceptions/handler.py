from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Custom exception handler to return errors in a consistent JSON format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code
        },
    )


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles validation errors (e.g., invalid email or required field missing).
    """
    for error in exc.errors():
        loc = error.get("loc", [])
        msg = error.get("msg", "Invalid input.")
        
        if "username" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": True,
                    "message": "Please enter username.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
            )
        elif "password" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": True,
                    "message": "Please enter password.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
            )

        if "email" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": True,
                    "message": "Invalid email format.",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
            )
    
    # Fallback for all other validation errors
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": True,
            "message": "Please enter all required fields.",
            "code": status.HTTP_400_BAD_REQUEST,
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for uncaught exceptions.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred.",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )
