# routers/productos.py
import traceback
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin_id
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse
from services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[dict])
def listar_productos(db: Session = Depends(get_db)):
    try:
        return producto_service.obtener_todos_productos(db)
    except Exception as e:
        print(f"Error en listar_productos: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar productos",
        )


@router.get("/{id_producto}", response_model=ProductoResponse)
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    try:
        return producto_service.obtener_producto(db, id_producto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error en obtener_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener producto",
        )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: ProductoCreate,
    db: Session = Depends(get_db),
    id_admin: int = Depends(require_admin_id),
):
    try:
        return producto_service.crear_producto(
            db,
            datos.nombre,
            datos.precio,
            datos.categoria,
            datos.stock_disponible,
            id_admin,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}",
        )


@router.put("/{id_producto}", response_model=dict)
def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
    id_admin: int = Depends(require_admin_id),
):
    try:
        return producto_service.actualizar_producto(
            db,
            id_producto,
            datos.model_dump(exclude_unset=True),
            id_admin,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error en actualizar_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar producto",
        )


@router.delete("/{id_producto}", response_model=dict)
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    id_admin: int = Depends(require_admin_id),
):
    try:
        return producto_service.eliminar_producto(db, id_producto, id_admin)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error en eliminar_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar producto",
        )
