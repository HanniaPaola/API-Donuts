# services/carrito_service.py
import logging
from typing import Dict

from sqlalchemy.orm import Session

from repositories.carrito import (
    actualizar_subtotal,
    agregar_producto,
    create,
    get_by_comprador_id,
    get_producto_en_carrito,
    get_productos_carrito,
    quitar_producto,
)
from repositories.producto_repo import get_by_id as get_producto_by_id
from repositories.usuario_comprador_repo import get_by_id as get_comprador_by_id

logger = logging.getLogger(__name__)


def obtener_carrito(db: Session, id_comprador: int) -> Dict:
    logger.debug("obtener_carrito id_comprador=%s", id_comprador)

    comprador = get_comprador_by_id(db, id_comprador)
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")

    carrito = get_by_comprador_id(db, id_comprador)
    if not carrito:
        logger.debug("Creando carrito id_comprador=%s", id_comprador)
        carrito = create(db, id_comprador)

    productos_en_carrito = get_productos_carrito(db, carrito.id_carrito)

    productos_response = [
        {
            "id_producto": cp.producto_id,
            "nombre": cp.producto.nombre if cp.producto else "Producto",
            "precio": cp.producto.precio if cp.producto else cp.precio_unitario,
            "cantidad": cp.cantidad,
            "precio_unitario": cp.precio_unitario,
        }
        for cp in productos_en_carrito
    ]

    return {
        "id_carrito": carrito.id_carrito,
        "id_comprador": carrito.id_comprador,
        "subtotal": carrito.subtotal,
        "cantidad_items": carrito.cantidad_items,
        "productos": productos_response,
    }


def agregar_al_carrito(
    db: Session, id_comprador: int, id_producto: int, cantidad: int
) -> Dict:
    logger.debug(
        "agregar_al_carrito id_comprador=%s id_producto=%s cantidad=%s",
        id_comprador,
        id_producto,
        cantidad,
    )

    comprador = get_comprador_by_id(db, id_comprador)
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")

    producto = get_producto_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    if producto.stock_disponible < cantidad:
        raise ValueError(
            f"Stock insuficiente. Disponible: {producto.stock_disponible}, Solicitado: {cantidad}"
        )

    carrito = get_by_comprador_id(db, id_comprador)
    if not carrito:
        carrito = create(db, id_comprador)

    carrito_id = carrito.id_carrito

    agregar_producto(
        db,
        carrito_id,
        id_producto,
        cantidad,
        producto.precio,
    )

    productos = get_productos_carrito(db, carrito_id)
    nuevo_subtotal = sum(cp.cantidad * cp.precio_unitario for cp in productos)
    nueva_cantidad_items = sum(cp.cantidad for cp in productos)

    carrito_actualizado = actualizar_subtotal(
        db,
        carrito_id,
        nuevo_subtotal,
        nueva_cantidad_items,
    )

    logger.info(
        "Producto agregado al carrito id_carrito=%s id_producto=%s",
        carrito_id,
        id_producto,
    )

    return {
        "id_carrito": carrito_actualizado.id_carrito,
        "id_comprador": carrito_actualizado.id_comprador,
        "id_producto": id_producto,
        "cantidad_agregada": cantidad,
        "subtotal": carrito_actualizado.subtotal,
        "cantidad_items": carrito_actualizado.cantidad_items,
        "mensaje": "Producto agregado al carrito",
    }


def quitar_del_carrito(db: Session, id_comprador: int, id_producto: int) -> Dict:
    logger.debug(
        "quitar_del_carrito id_comprador=%s id_producto=%s",
        id_comprador,
        id_producto,
    )

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
    nuevo_subtotal = (
        sum(cp.cantidad * cp.precio_unitario for cp in productos) if productos else 0.0
    )
    nueva_cantidad_items = sum(cp.cantidad for cp in productos) if productos else 0

    carrito_actualizado = actualizar_subtotal(
        db,
        carrito_id,
        nuevo_subtotal,
        nueva_cantidad_items,
    )

    logger.info(
        "Producto quitado del carrito id_carrito=%s id_producto=%s",
        carrito_id,
        id_producto,
    )

    return {
        "id_carrito": carrito_actualizado.id_carrito,
        "id_comprador": carrito_actualizado.id_comprador,
        "id_producto": id_producto,
        "subtotal": carrito_actualizado.subtotal,
        "cantidad_items": carrito_actualizado.cantidad_items,
        "mensaje": "Producto removido del carrito",
    }
