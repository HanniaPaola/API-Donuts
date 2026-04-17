# routers/carrito.py
import traceback

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
    except Exception as e:
        print(f"Error obtener carrito: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener carrito",
        )


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
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar producto: {str(e)}",
        )


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
    except Exception as e:
        print(f"Error quitar producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al quitar producto del carrito",
        )
