from typing import List, Optional
from sqlalchemy.orm import Session
from models.pedido import Pedido

def get_by_id(db: Session, id_pedido: int) -> Optional[Pedido]:
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

def get_by_comprador_id(db: Session, id_comprador: int) -> List[Pedido]:
    return db.query(Pedido).filter(Pedido.id_comprador == id_comprador).all()

def create(db: Session, precio_total: float, metodo_pago: str,
           id_comprador: int, id_producto: int) -> Pedido:
    nuevo_pedido = Pedido(
        precio_total=precio_total,
        metodo_pago=metodo_pago,
        id_comprador=id_comprador,
        id_producto=id_producto
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido

def get_all(db: Session) -> List[Pedido]:
    return db.query(Pedido).all()

def delete(db: Session, id_pedido: int) -> bool:
    pedido = get_by_id(db, id_pedido)
    if pedido:
        db.delete(pedido)
        db.commit()
        return True
    return False