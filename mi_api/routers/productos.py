# routers/productos.py
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_token
from services import producto_service
from schemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse
)
import traceback

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

security = HTTPBearer()

def obtener_id_admin_autenticado(credentials: HTTPAuthorizationCredentials = Security(security)) -> int:
    token = credentials.credentials
    print(f"Verificando token admin...")
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    try:
        id_admin = int(payload.get("sub"))
        print(f"Admin autenticado ID: {id_admin}")
        return id_admin
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

@router.get("/", response_model=List[dict])
def listar_productos(db: Session = Depends(get_db)):
    try:
        resultado = producto_service.obtener_todos_productos(db)
        return resultado
    except Exception as e:
        print(f"Error en listar_productos: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar productos"
        )

@router.get("/{id_producto}", response_model=ProductoResponse)
def obtener_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    try:
        resultado = producto_service.obtener_producto(db, id_producto)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error en obtener_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener producto"
        )

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: ProductoCreate,
    db: Session = Depends(get_db),
    id_admin: int = Depends(obtener_id_admin_autenticado)
):
    try:
        print(f"=== CREAR PRODUCTO ===")
        print(f"Nombre: {datos.nombre}")
        print(f"Precio: {datos.precio}")
        print(f"Categoría: {datos.categoria}")
        print(f"Stock: {datos.stock_disponible}")
        print(f"ID Admin: {id_admin}")
        
        resultado = producto_service.crear_producto(
            db,
            datos.nombre,
            datos.precio,
            datos.categoria,
            datos.stock_disponible,
            id_admin
        )
        print(f"Resultado: {resultado}")
        return resultado
    except ValueError as e:
        print(f"Error de validación: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error inesperado: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )

@router.put("/{id_producto}", response_model=dict)
def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
    id_admin: int = Depends(obtener_id_admin_autenticado)
):
    try:
        resultado = producto_service.actualizar_producto(
            db,
            id_producto,
            datos.model_dump(exclude_unset=True),
            id_admin
        )
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error en actualizar_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar producto"
        )

@router.delete("/{id_producto}", response_model=dict)
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    id_admin: int = Depends(obtener_id_admin_autenticado)
):
    try:
        resultado = producto_service.eliminar_producto(db, id_producto, id_admin)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error en eliminar_producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar producto"
        )