# routers/admins.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from repositories import usuario_admin_repo
from schemas import (
    UsuarioAdminCreate,
    UsuarioAdminLogin,
    UsuarioAdminResponse,
)
from services import usuario_admin_service

router = APIRouter(prefix="/admins", tags=["Administradores"])


@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
def registrar_admin(
    datos: UsuarioAdminCreate,
    db: Session = Depends(get_db),
):
    try:
        return usuario_admin_service.registrar_admin(
            db,
            datos.nombre,
            datos.contrasena,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=dict)
def login_admin(
    datos: UsuarioAdminLogin,
    db: Session = Depends(get_db),
):
    if not datos.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar nombre o email",
        )
    try:
        return usuario_admin_service.login_admin(
            db,
            datos.username,
            datos.contrasena,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/contacto-chat", response_model=dict)
def contacto_chat_colaboracion(db: Session = Depends(get_db)):
    """Identificador público (mismo valor que `nombre` en login) para salas comprador–admin. Sin credenciales."""
    admins = usuario_admin_repo.get_all(db)
    if not admins:
        return {"peer_id": ""}
    admins.sort(key=lambda a: a.id_admin)
    return {"peer_id": admins[0].nombre}


@router.get("/{id_admin}", response_model=UsuarioAdminResponse)
def obtener_admin(
    id_admin: int,
    db: Session = Depends(get_db),
):
    try:
        return usuario_admin_service.obtener_admin(db, id_admin)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
