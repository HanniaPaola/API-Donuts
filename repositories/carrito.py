# repositories/carrito.py
from typing import List, Optional
from sqlalchemy.orm import Session
from models.carrito import Carrito
from models.carrito_producto import CarritoProducto

def get_by_comprador_id(db: Session, id_comprador: int) -> Optional[Carrito]:
    return db.query(Carrito).filter(Carrito.id_comprador == id_comprador).first()

def get_by_id(db: Session, id_carrito: int) -> Optional[Carrito]:
    return db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()

def create(db: Session, id_comprador: int) -> Carrito:
    nuevo_carrito = Carrito(
        id_comprador=id_comprador,
        subtotal=0.0,
        cantidad_items=0
    )
    db.add(nuevo_carrito)
    db.commit()
    db.refresh(nuevo_carrito)
    return nuevo_carrito

def agregar_producto(db: Session, id_carrito: int, id_producto: int, 
                     cantidad: int, precio_unitario: float) -> CarritoProducto:
    carrito_producto = db.query(CarritoProducto).filter(
        CarritoProducto.carrito_id == id_carrito,
        CarritoProducto.producto_id == id_producto
    ).first()
    
    if carrito_producto:
        carrito_producto.cantidad += cantidad
    else:
        carrito_producto = CarritoProducto(
            carrito_id=id_carrito,
            producto_id=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        db.add(carrito_producto)
    
    db.commit()
    db.refresh(carrito_producto)
    return carrito_producto

def quitar_producto(db: Session, id_carrito: int, id_producto: int) -> bool:
    carrito_producto = db.query(CarritoProducto).filter(
        CarritoProducto.carrito_id == id_carrito,
        CarritoProducto.producto_id == id_producto
    ).first()
    
    if carrito_producto:
        db.delete(carrito_producto)
        db.commit()
        return True
    return False

def actualizar_subtotal(db: Session, id_carrito: int, nuevo_subtotal: float,
                        nueva_cantidad_items: int) -> Optional[Carrito]:
    carrito = get_by_id(db, id_carrito)
    if carrito:
        carrito.subtotal = nuevo_subtotal
        carrito.cantidad_items = nueva_cantidad_items
        db.commit()
        db.refresh(carrito)
    return carrito

def vaciar_carrito(db: Session, id_carrito: int) -> bool:
    productos = db.query(CarritoProducto).filter(CarritoProducto.carrito_id == id_carrito).all()
    for producto in productos:
        db.delete(producto)
    
    carrito = get_by_id(db, id_carrito)
    if carrito:
        carrito.subtotal = 0.0
        carrito.cantidad_items = 0
    
    db.commit()
    return True

def get_productos_carrito(db: Session, id_carrito: int) -> List[CarritoProducto]:
    return db.query(CarritoProducto).filter(CarritoProducto.carrito_id == id_carrito).all()

def get_producto_en_carrito(db: Session, carrito_id: int, producto_id: int) -> Optional[CarritoProducto]:
    return db.query(CarritoProducto).filter(
        CarritoProducto.carrito_id == carrito_id,
        CarritoProducto.producto_id == producto_id
    ).first()