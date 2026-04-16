# services/carrito_service.py
from typing import Dict
from sqlalchemy.orm import Session
from repositories.carrito import (
    get_by_comprador_id, 
    create, 
    get_productos_carrito, 
    agregar_producto, 
    actualizar_subtotal, 
    quitar_producto, 
    vaciar_carrito,
    get_producto_en_carrito
)
from repositories.usuario_comprador_repo import get_by_id as get_comprador_by_id
from repositories.producto_repo import get_by_id as get_producto_by_id
import traceback

def obtener_carrito(db: Session, id_comprador: int) -> Dict:
    print(f"=== OBTENER CARRITO ===")
    print(f"ID Comprador: {id_comprador}")
    
    comprador = get_comprador_by_id(db, id_comprador)
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
    
    carrito = get_by_comprador_id(db, id_comprador)
    if not carrito:
        print(f"Creando nuevo carrito para comprador {id_comprador}")
        carrito = create(db, id_comprador)
    
    # Usar id_carrito
    productos_en_carrito = get_productos_carrito(db, carrito.id_carrito)
    
    productos_response = [
        {
            "id_producto": cp.producto_id,
            "nombre": cp.producto.nombre if cp.producto else "Producto",
            "precio": cp.producto.precio if cp.producto else cp.precio_unitario,
            "cantidad": cp.cantidad,
            "precio_unitario": cp.precio_unitario
        }
        for cp in productos_en_carrito
    ]
    
    return {
        "id_carrito": carrito.id_carrito,
        "id_comprador": carrito.id_comprador,
        "subtotal": carrito.subtotal,
        "cantidad_items": carrito.cantidad_items,
        "productos": productos_response
    }

def agregar_al_carrito(db: Session, id_comprador: int, id_producto: int, cantidad: int) -> Dict:
    try:
        print(f"=== AGREGAR AL CARRITO ===")
        print(f"ID Comprador: {id_comprador}")
        print(f"ID Producto: {id_producto}")
        print(f"Cantidad: {cantidad}")
        
        comprador = get_comprador_by_id(db, id_comprador)
        if not comprador:
            raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
        print(f"Comprador encontrado: {comprador.nombre}")
        
        producto = get_producto_by_id(db, id_producto)
        if not producto:
            raise ValueError(f"Producto con ID {id_producto} no encontrado")
        print(f"Producto encontrado: {producto.nombre}, Stock: {producto.stock_disponible}")
        
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        if producto.stock_disponible < cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {producto.stock_disponible}, Solicitado: {cantidad}"
            )
        
        carrito = get_by_comprador_id(db, id_comprador)
        if not carrito:
            print(f"Creando nuevo carrito para comprador {id_comprador}")
            carrito = create(db, id_comprador)
        
        # Usar id_carrito
        carrito_id = carrito.id_carrito
        print(f"Carrito ID: {carrito_id}")
        
        carrito_producto = agregar_producto(
            db,
            carrito_id,
            id_producto,
            cantidad,
            producto.precio
        )
        
        productos = get_productos_carrito(db, carrito_id)
        nuevo_subtotal = sum(cp.cantidad * cp.precio_unitario for cp in productos)
        nueva_cantidad_items = sum(cp.cantidad for cp in productos)
        
        carrito_actualizado = actualizar_subtotal(
            db,
            carrito_id,
            nuevo_subtotal,
            nueva_cantidad_items
        )
        
        print(f"Producto agregado exitosamente")
        return {
            "id_carrito": carrito_actualizado.id_carrito,
            "id_comprador": carrito_actualizado.id_comprador,
            "id_producto": id_producto,
            "cantidad_agregada": cantidad,
            "subtotal": carrito_actualizado.subtotal,
            "cantidad_items": carrito_actualizado.cantidad_items,
            "mensaje": "Producto agregado al carrito"
        }
    except Exception as e:
        print(f"ERROR en agregar_al_carrito: {e}")
        print(traceback.format_exc())
        raise

def quitar_del_carrito(db: Session, id_comprador: int, id_producto: int) -> Dict:
    print(f"=== QUITAR DEL CARRITO ===")
    print(f"ID Comprador: {id_comprador}")
    print(f"ID Producto: {id_producto}")
    
    comprador = get_comprador_by_id(db, id_comprador)
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
    
    carrito = get_by_comprador_id(db, id_comprador)
    if not carrito:
        raise ValueError("El comprador no tiene carrito")
    
    carrito_id = carrito.id_carrito
    
    producto_en_carrito = get_producto_en_carrito(db, carrito_id, id_producto)
    
    if not producto_en_carrito:
        raise ValueError(f"El producto {id_producto} no está en el carrito")
    
    quitar_producto(db, carrito_id, id_producto)
    
    productos = get_productos_carrito(db, carrito_id)
    nuevo_subtotal = sum(cp.cantidad * cp.precio_unitario for cp in productos) if productos else 0.0
    nueva_cantidad_items = sum(cp.cantidad for cp in productos) if productos else 0
    
    carrito_actualizado = actualizar_subtotal(
        db,
        carrito_id,
        nuevo_subtotal,
        nueva_cantidad_items
    )
    
    return {
        "id_carrito": carrito_actualizado.id_carrito,
        "id_comprador": carrito_actualizado.id_comprador,
        "id_producto": id_producto,
        "subtotal": carrito_actualizado.subtotal,
        "cantidad_items": carrito_actualizado.cantidad_items,
        "mensaje": "Producto removido del carrito"
    }