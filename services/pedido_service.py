from typing import Dict, List

from sqlalchemy.orm import Session

from repositories.pedido_repo import create as pedido_create, get_by_comprador_id, get_by_id
from repositories.usuario_comprador_repo import get_by_id as get_comprador_by_id
from repositories.carrito import (
    get_by_comprador_id as get_carrito_by_comprador,
    get_productos_carrito,
    vaciar_carrito,
)
from repositories.producto_repo import restar_stock, get_by_id as get_producto_by_id
import traceback


def _lineas_dict(pedido) -> List[Dict]:
    return [
        {
            "id_producto": it.id_producto,
            "nombre_producto": it.producto_nombre,
            "cantidad": it.cantidad,
            "precio_unitario": it.precio_unitario,
            "subtotal": it.subtotal,
        }
        for it in pedido.items
    ]


def crear_pedido(db: Session, id_comprador: int, metodo_pago: str) -> Dict:
    try:
        comprador = get_comprador_by_id(db, id_comprador)
        if not comprador:
            raise ValueError(f"Comprador con ID {id_comprador} no encontrado")

        carrito = get_carrito_by_comprador(db, id_comprador)
        if not carrito:
            raise ValueError("El comprador no tiene carrito")

        productos_en_carrito = get_productos_carrito(db, carrito.id_carrito)
        if not productos_en_carrito:
            raise ValueError("El carrito está vacío, no se puede hacer un pedido")

        precio_total_general = 0.0
        lineas = []
        for cp in productos_en_carrito:
            subtotal = cp.cantidad * cp.precio_unitario
            precio_total_general += subtotal
            prod = get_producto_by_id(db, cp.producto_id)
            nombre = prod.nombre if prod else "Producto"
            lineas.append(
                {
                    "id_producto": cp.producto_id,
                    "producto_nombre": nombre,
                    "cantidad": cp.cantidad,
                    "precio_unitario": cp.precio_unitario,
                    "subtotal": subtotal,
                }
            )

        nuevo_pedido = pedido_create(
            db,
            precio_total=precio_total_general,
            metodo_pago=metodo_pago,
            id_comprador=id_comprador,
            lineas=lineas,
        )

        for cp in productos_en_carrito:
            restar_stock(db, cp.producto_id, cp.cantidad)

        vaciar_carrito(db, carrito.id_carrito)

        return {
            "id_pedido": nuevo_pedido.id_pedido,
            "id_comprador": id_comprador,
            "precio_total": precio_total_general,
            "metodo_pago": metodo_pago,
            "lineas": _lineas_dict(nuevo_pedido),
            "mensaje": "Pedido creado exitosamente",
        }
    except Exception as e:
        print(f"ERROR en crear_pedido: {e}")
        print(traceback.format_exc())
        raise


def obtener_historial_pedidos(db: Session, id_comprador: int) -> Dict:
    try:
        pedidos = get_by_comprador_id(db, id_comprador)
        pedidos_response = [
            {
                "id_pedido": p.id_pedido,
                "fecha": str(p.fecha),
                "precio_total": p.precio_total,
                "metodo_pago": p.metodo_pago,
                "lineas": _lineas_dict(p),
            }
            for p in pedidos
        ]
        return {
            "id_comprador": id_comprador,
            "cantidad_pedidos": len(pedidos_response),
            "pedidos": pedidos_response,
        }
    except Exception as e:
        print(f"ERROR en obtener_historial_pedidos: {e}")
        print(traceback.format_exc())
        raise


def obtener_detalle_pedido(db: Session, id_pedido: int, id_comprador: int) -> Dict:
    try:
        pedido = get_by_id(db, id_pedido)
        if not pedido:
            raise ValueError(f"Pedido con ID {id_pedido} no encontrado")

        if pedido.id_comprador != id_comprador:
            raise ValueError("No tienes permiso para ver este pedido")

        return {
            "id_pedido": pedido.id_pedido,
            "fecha": str(pedido.fecha),
            "precio_total": pedido.precio_total,
            "metodo_pago": pedido.metodo_pago,
            "id_comprador": pedido.id_comprador,
            "lineas": _lineas_dict(pedido),
        }
    except Exception as e:
        print(f"ERROR en obtener_detalle_pedido: {e}")
        print(traceback.format_exc())
        raise
