from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from auth import verify_token
from services import pedido_service
from schemas import (
    PedidoCreate,
    PedidoResponse
)

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

# Configurar seguridad para Swagger
security = HTTPBearer()

def obtener_id_comprador_autenticado(credentials: HTTPAuthorizationCredentials = Security(security)) -> int:
    """Obtiene el ID del comprador desde el token JWT"""
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    try:
        id_comprador = int(payload.get("sub"))
        return id_comprador
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    datos: PedidoCreate,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    try:
        resultado = pedido_service.crear_pedido(
            db,
            id_comprador,
            datos.metodo_pago
        )
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear pedido"
        )

@router.get("/historial", response_model=dict)
def obtener_mis_pedidos(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    """Obtener mis propios pedidos (no necesita id en URL)"""
    try:
        resultado = pedido_service.obtener_historial_pedidos(db, id_comprador)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener historial de pedidos"
        )

@router.get("/detalle/{id_pedido}", response_model=dict)
def obtener_detalle_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(obtener_id_comprador_autenticado)
):
    try:
        resultado = pedido_service.obtener_detalle_pedido(db, id_pedido, id_comprador)
        return resultado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener detalle del pedido"
        )