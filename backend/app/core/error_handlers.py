# English: Global error handlers — consistent error response shape across the API.
# Roman Urdu: Global error handlers — poori API mein consistent error response shape.

import logging
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _shape(code: str, message: str, detail=None) -> dict:
    """English: Uniform error envelope.
    Roman Urdu: Uniform error envelope."""
    return {
        'error': {
            'code': code,
            'message': message,
            'detail': detail,
        }
    }


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    English: Wrap HTTPException into our envelope while preserving the status code.
    Roman Urdu: HTTPException ko apne envelope mein wrap karo, status code preserve karte hue.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=_shape(
            code=f'http_{exc.status_code}',
            message=str(exc.detail) if exc.detail else 'Request failed',
            detail=None,
        ),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    English: Wrap FastAPI's 422 validation errors with a clear, consistent shape.
    Roman Urdu: FastAPI ke 422 validation errors ko clear, consistent shape mein wrap karo.
    """
    # `exc.errors()` may contain non-serializable context, so we trim it.
    errs = []
    for e in exc.errors():
        errs.append({
            'loc': list(e.get('loc', [])),
            'msg': e.get('msg', ''),
            'type': e.get('type', ''),
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_shape(
            code='validation_error',
            message='One or more fields are invalid.',
            detail=errs,
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    English: Catch-all for unexpected exceptions — log full trace, return generic message.
    Roman Urdu: Unexpected exceptions ke liye catch-all — full trace log karo, generic message return karo.
    """
    logger.exception(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content=_shape(
            code='internal_error',
            message='An unexpected error occurred. Please try again.',
            detail=None,
        ),
    )
