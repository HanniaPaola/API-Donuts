# routers/carrito.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_buyer_id
from schemas import AgregarAlCarritoRequest, CarritoResponse
from services import carrito_service

router = APIRouter(prefix="/carrito", tags=["Carrito"])


@router.get("/mi-carrito", response_model=CarritoResponse)
def obtener_mi_carrito(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return carrito_service.obtener_carrito(db, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/agregar", response_model=dict, status_code=status.HTTP_200_OK)
def agregar_al_carrito(
    datos: AgregarAlCarritoRequest,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return carrito_service.agregar_al_carrito(
            db,
            id_comprador,
            datos.id_producto,
            datos.cantidad,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/quitar/{id_producto}", response_model=dict)
def quitar_del_carrito(
    id_producto: int,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return carrito_service.quitar_del_carrito(db, id_comprador, id_producto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/vaciar", response_model=dict)
def vaciar_mi_carrito(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return carrito_service.vaciar_mi_carrito(db, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
