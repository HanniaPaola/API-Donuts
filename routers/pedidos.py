from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_admin_id, require_buyer_id
from schemas import PedidoCreate, PedidoEstadoUpdate
from services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    datos: PedidoCreate,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return pedido_service.crear_pedido(db, id_comprador, datos.metodo_pago)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/historial", response_model=dict)
def obtener_mis_pedidos(
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return pedido_service.obtener_historial_pedidos(db, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/admin/historial", response_model=dict)
def obtener_historial_pedidos_admin(
    db: Session = Depends(get_db),
    _id_admin: int = Depends(require_admin_id),
):
    return pedido_service.obtener_historial_admin(db)


@router.patch("/admin/{id_pedido}/estado", response_model=dict)
def admin_actualizar_estado_pedido(
    id_pedido: int,
    datos: PedidoEstadoUpdate,
    db: Session = Depends(get_db),
    _id_admin: int = Depends(require_admin_id),
):
    try:
        return pedido_service.actualizar_estado_pedido_admin(db, id_pedido, datos.estado)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/mi-pedido/{id_pedido}/cancelar", response_model=dict)
def comprador_cancelar_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return pedido_service.cancelar_pedido_comprador(db, id_pedido, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/detalle/{id_pedido}", response_model=dict)
def obtener_detalle_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    id_comprador: int = Depends(require_buyer_id),
):
    try:
        return pedido_service.obtener_detalle_pedido(db, id_pedido, id_comprador)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
