# repositories/producto_repo.py
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from models.producto import Producto

def get_by_id(db: Session, id_producto: int) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()

def get_all(db: Session) -> List[Producto]:
    return db.query(Producto).all()

def get_by_admin_id(db: Session, id_admin: int) -> List[Producto]:
    return db.query(Producto).filter(Producto.id_admin == id_admin).all()

def get_by_colaborador_id(db: Session, id_colaborador: int) -> List[Producto]:
    return (
        db.query(Producto)
        .filter(Producto.id_colaborador == id_colaborador)
        .all()
    )

def get_by_categoria(db: Session, categoria: str) -> List[Producto]:
    return db.query(Producto).filter(Producto.categoria == categoria).all()

def create(
    db: Session,
    nombre: str,
    precio: float,
    categoria: str,
    stock_disponible: int,
    id_admin: int,
    id_colaborador: Optional[int] = None,
) -> Producto:
    nuevo_producto = Producto(
        nombre=nombre,
        precio=precio,
        categoria=categoria,
        stock_disponible=stock_disponible,
        id_admin=id_admin,
        id_colaborador=id_colaborador,
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

def update(db: Session, id_producto: int, datos: Dict) -> Optional[Producto]:
    producto = get_by_id(db, id_producto)
    if producto:
        for key, value in datos.items():
            setattr(producto, key, value)
        db.commit()
        db.refresh(producto)
    return producto

def delete(db: Session, id_producto: int) -> bool:
    producto = get_by_id(db, id_producto)
    if producto:
        db.delete(producto)
        db.commit()
        return True
    return False

def restar_stock(db: Session, id_producto: int, cantidad: int) -> bool:
    producto = get_by_id(db, id_producto)
    if producto and producto.stock_disponible >= cantidad:
        producto.stock_disponible -= cantidad
        db.commit()
        db.refresh(producto)
        return True
    return False

def sumar_stock(db: Session, id_producto: int, cantidad: int) -> bool:
    producto = get_by_id(db, id_producto)
    if producto:
        producto.stock_disponible += cantidad
        db.commit()
        db.refresh(producto)
        return True
    return False