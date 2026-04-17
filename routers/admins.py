# routers/admins.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
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


@router.get("/{id_admin}", response_model=UsuarioAdminResponse)
def obtener_admin(
    id_admin: int,
    db: Session = Depends(get_db),
):
    try:
        return usuario_admin_service.obtener_admin(db, id_admin)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
