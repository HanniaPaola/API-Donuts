from typing import List, Optional, Sequence
from sqlalchemy.orm import Session, joinedload

from models.pedido import Pedido
from models.pedido_item import PedidoItem


def get_by_id(db: Session, id_pedido: int) -> Optional[Pedido]:
    return (
        db.query(Pedido)
        .options(joinedload(Pedido.items))
        .filter(Pedido.id_pedido == id_pedido)
        .first()
    )


def get_by_comprador_id(db: Session, id_comprador: int) -> List[Pedido]:
    return (
        db.query(Pedido)
        .options(joinedload(Pedido.items))
        .filter(Pedido.id_comprador == id_comprador)
        .order_by(Pedido.id_pedido.desc())
        .all()
    )


def create(
    db: Session,
    precio_total: float,
    metodo_pago: str,
    id_comprador: int,
    lineas: Sequence[dict],
) -> Pedido:
    """Crea un pedido y sus ítems en una transacción."""
    pedido = Pedido(
        precio_total=precio_total,
        metodo_pago=metodo_pago,
        id_comprador=id_comprador,
        estado="pendiente",
    )
    db.add(pedido)
    db.flush()

    for ln in lineas:
        db.add(
            PedidoItem(
                id_pedido=pedido.id_pedido,
                id_producto=ln["id_producto"],
                producto_nombre=ln["producto_nombre"],
                cantidad=ln["cantidad"],
                precio_unitario=ln["precio_unitario"],
                subtotal=ln["subtotal"],
            )
        )

    db.commit()
    db.refresh(pedido)
    return pedido


def get_all(db: Session) -> List[Pedido]:
    return (
        db.query(Pedido)
        .options(joinedload(Pedido.items), joinedload(Pedido.comprador))
        .order_by(Pedido.id_pedido.desc())
        .all()
    )


def update_estado(db: Session, id_pedido: int, estado: str) -> Optional[Pedido]:
    pedido = get_by_id(db, id_pedido)
    if pedido:
        pedido.estado = estado
        db.commit()
        db.refresh(pedido)
    return pedido


def delete(db: Session, id_pedido: int) -> bool:
    pedido = get_by_id(db, id_pedido)
    if pedido:
        db.delete(pedido)
        db.commit()
        return True
    return False
