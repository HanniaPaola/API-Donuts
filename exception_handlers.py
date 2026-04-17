from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("api.errors")


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))


def error_payload(
    code: str,
    message: Any,
    request_id: str,
    *,
    details: Any | None = None,
) -> dict:
    err: dict[str, Any] = {
        "code": code,
        "message": message,
        "request_id": request_id,
    }
    if details is not None:
        err["details"] = details
    return {"error": err}


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    rid = _request_id(request)
    logger.warning(
        "HTTP %s | %s %s | request_id=%s | detail=%s",
        exc.status_code,
        request.method,
        request.url.path,
        rid,
        exc.detail,
    )
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code,
        headers=dict(headers) if headers else {},
        content=error_payload(f"HTTP_{exc.status_code}", exc.detail, rid),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    rid = _request_id(request)
    errors = exc.errors()
    logger.info(
        "Validación | %s %s | request_id=%s | errores=%s",
        request.method,
        request.url.path,
        rid,
        errors,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_payload(
            "VALIDATION_ERROR",
            "Error de validación en la solicitud",
            rid,
            details=errors,
        ),
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    rid = _request_id(request)
    logger.warning(
        "Integridad BD | %s %s | request_id=%s | %s",
        request.method,
        request.url.path,
        rid,
        exc.orig if hasattr(exc, "orig") else str(exc),
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_payload(
            "CONFLICT",
            "Conflicto con datos existentes (clave duplicada o restricción)",
            rid,
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    rid = _request_id(request)
    logger.exception(
        "No controlado | %s %s | request_id=%s",
        request.method,
        request.url.path,
        rid,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload(
            "INTERNAL_ERROR",
            "Ocurrió un error inesperado. Intente más tarde o contacte soporte.",
            rid,
        ),
    )


def register_exception_handlers(app: Any) -> None:
    """Registrar en orden: específicos antes del catch-all Exception."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
