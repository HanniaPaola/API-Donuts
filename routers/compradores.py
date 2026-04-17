# routers/compradores.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_buyer_id
from schemas import (
    UsuarioCompradorCreate,
    UsuarioCompradorLogin,
    UsuarioCompradorResponse,
)
from services import usuario_comprador_service
from services.postulacion_colaborador_service import obtener_postulacion_colaborador_mia

router = APIRouter(prefix="/compradores", tags=["Compradores"])


@router.post("/registro", response_model=dict, status_code=status.HTTP_201_CREATED)
def registrar_comprador(
    datos: UsuarioCompradorCreate,
    db: Session = Depends(get_db),
):
    try:
        return usuario_comprador_service.registrar_comprador(
            db,
            datos.nombre,
            datos.contrasena,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/mi-postulacion-colaborador", response_model=dict)
def mi_postulacion_colaborador(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    """Última postulación como colaborador asociada al identificador de sesión (ver docs de vinculación por correo)."""
    data = obtener_postulacion_colaborador_mia(db, id_comprador)
    return {"postulacion": data}


@router.post("/login", response_model=dict)
def login_comprador(
    datos: UsuarioCompradorLogin,
    db: Session = Depends(get_db),
):
    if not datos.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar nombre o email",
        )
    try:
        return usuario_comprador_service.login_comprador(
            db,
            datos.username,
            datos.contrasena,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/{id_comprador}", response_model=UsuarioCompradorResponse)
def obtener_comprador(
    id_comprador: int,
    db: Session = Depends(get_db),
):
    try:
        return usuario_comprador_service.obtener_comprador(db, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
