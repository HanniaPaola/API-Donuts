# routers/carrito.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_token
from services import carrito_service
from schemas import (
    CarritoResponse,
    AgregarAlCarritoRequest
)
import traceback

router = APIRouter(
    prefix="/carrito",
    tags=["Carrito"]
)

security = HTTPBearer()

def obtener_id_comprador_autenticado(credentials: HTTPAuthorizationCredentials = Security(security)) -> int:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    try:
        id_comprador = int(payload.get("sub"))
        print(f"ID Comprador autenticado: {id_comprador}")
        return id_comprador
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

@router.get("/mi-carrito", response_model=CarritoResponse)
def obtener_mi_carrito(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    try:
        resultado = carrito_service.obtener_carrito(db, id_comprador)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error obtener carrito: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener carrito"
        )

@router.post("/agregar", response_model=dict, status_code=status.HTTP_200_OK)
def agregar_al_carrito(
    datos: AgregarAlCarritoRequest,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    try:
        print(f"=== AGREGAR AL CARRITO ===")
        print(f"ID Comprador: {id_comprador}")
        print(f"ID Producto: {datos.id_producto}")
        print(f"Cantidad: {datos.cantidad}")
        
        resultado = carrito_service.agregar_al_carrito(
            db,
            id_comprador,
            datos.id_producto,
            datos.cantidad
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
            detail=f"Error al agregar producto: {str(e)}"
        )

@router.delete("/quitar/{id_producto}", response_model=dict)
def quitar_del_carrito(
    id_producto: int,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    try:
        resultado = carrito_service.quitar_del_carrito(db, id_comprador, id_producto)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error quitar producto: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al quitar producto del carrito"
        )