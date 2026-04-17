"""Dependencias FastAPI: JWT con verificación de rol (buyer / admin)."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from auth import verify_token
from database import get_db
from repositories import usuario_admin_repo, usuario_comprador_repo

security = HTTPBearer()


def _jwt_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return payload


def require_buyer_id(payload: dict = Depends(_jwt_payload)) -> int:
    if payload.get("role") != "buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere sesión de comprador",
        )
    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        ) from exc


def require_admin_id(payload: dict = Depends(_jwt_payload)) -> int:
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere sesión de administrador",
        )
    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        ) from exc


def require_chat_actor_nombre(
    db: Session = Depends(get_db),
    payload: dict = Depends(_jwt_payload),
) -> str:
    """Identificador de usuario en salas chat (campo `nombre` / email en BD)."""
    role = payload.get("role")
    try:
        uid = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        ) from exc

    if role == "buyer":
        u = usuario_comprador_repo.get_by_id(db, uid)
        if not u:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
            )
        return u.nombre

    if role == "admin":
        u = usuario_admin_repo.get_by_id(db, uid)
        if not u:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
            )
        return u.nombre

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Solo comprador o administrador pueden usar el chat",
    )
