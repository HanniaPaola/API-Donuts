from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import optional_buyer_id, require_admin_id
from schemas.colaborador import ColaboradorCreate, ColaboradorUpdate, CollaboratorPublic
from schemas.postulacion_colaborador import PostulacionColaboradorCreate, PostulacionColaboradorEstadoUpdate
from services.colaborador_service import ColaboradorService
from services.postulacion_colaborador_service import (
    actualizar_estado_postulacion_admin,
    crear_postulacion,
    listar_postulaciones_admin,
)
from services.producto_service import obtener_productos_menu_colaborador

router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])


@router.post("/postulaciones", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_postulacion_colaborador(
    datos: PostulacionColaboradorCreate,
    db: Session = Depends(get_db),
    id_comprador_sesion: int | None = Depends(optional_buyer_id),
):
    try:
        return crear_postulacion(
            db,
            datos.nombre_completo,
            str(datos.email),
            datos.telefono,
            datos.specialty,
            datos.mensaje,
            id_comprador_sesion=id_comprador_sesion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/postulaciones/admin", response_model=dict)
def listar_postulaciones_colaborador_admin(
    db: Session = Depends(get_db),
    _id_admin: int = Depends(require_admin_id),
):
    return listar_postulaciones_admin(db)


@router.patch("/postulaciones/{postulacion_id}/estado", response_model=dict)
def patch_estado_postulacion_colaborador(
    postulacion_id: int,
    body: PostulacionColaboradorEstadoUpdate,
    db: Session = Depends(get_db),
    _id_admin: int = Depends(require_admin_id),
):
    try:
        return actualizar_estado_postulacion_admin(db, postulacion_id, body.estado)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/specialty/{specialty}", response_model=List[CollaboratorPublic])
def get_colaboradores_by_specialty(specialty: str, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.get_colaboradores_by_specialty(db, specialty)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/online", response_model=List[CollaboratorPublic])
def get_online_colaboradores(db: Session = Depends(get_db)):
    return ColaboradorService.get_online_colaboradores(db)


@router.get("/", response_model=List[CollaboratorPublic])
def get_all_colaboradores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data = ColaboradorService.get_all_colaboradores(db, skip, limit)
        return data["colaboradores"]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=CollaboratorPublic, status_code=status.HTTP_201_CREATED)
def create_colaborador(colaborador_data: ColaboradorCreate, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.create_colaborador(db, colaborador_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{colaborador_id}/productos", response_model=List[dict])
def listar_menu_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    """Productos asignados al menú de un colaborador (`id_colaborador` en tabla producto)."""
    try:
        return obtener_productos_menu_colaborador(db, colaborador_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{colaborador_id}", response_model=CollaboratorPublic)
def get_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    try:
        return ColaboradorService.get_colaborador_by_id(db, colaborador_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{colaborador_id}", response_model=CollaboratorPublic)
def update_colaborador(
    colaborador_id: int,
    update_data: ColaboradorUpdate,
    db: Session = Depends(get_db),
):
    try:
        return ColaboradorService.update_colaborador(db, colaborador_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    try:
        ColaboradorService.delete_colaborador(db, colaborador_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
