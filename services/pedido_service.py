from typing import Dict, List
from sqlalchemy.orm import Session
from repositories.pedido_repo import create as pedido_create, get_by_comprador_id, get_by_id
from repositories.usuario_comprador_repo import get_by_id as get_comprador_by_id
from repositories.carrito import get_by_comprador_id as get_carrito_by_comprador, get_productos_carrito, vaciar_carrito
from repositories.producto_repo import restar_stock, get_by_id as get_producto_by_id
import traceback

def crear_pedido(db: Session, id_comprador: int, metodo_pago: str) -> Dict:
    try:
        print(f"=== CREAR PEDIDO ===")
        print(f"ID Comprador: {id_comprador}")
        print(f"Método de pago: {metodo_pago}")
        
        # Verificar comprador
        comprador = get_comprador_by_id(db, id_comprador)
        if not comprador:
            raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
        print(f"Comprador encontrado: {comprador.nombre}")
        
        # Verificar carrito
        carrito = get_carrito_by_comprador(db, id_comprador)
        if not carrito:
            raise ValueError("El comprador no tiene carrito")
        print(f"Carrito ID: {carrito.id_carrito}")
        
        # Verificar productos en carrito
        productos_en_carrito = get_productos_carrito(db, carrito.id_carrito)
        if not productos_en_carrito:
            raise ValueError("El carrito está vacío, no se puede hacer un pedido")
        print(f"Productos en carrito: {len(productos_en_carrito)}")
        
        # Calcular total
        precio_total_general = 0.0
        for cp in productos_en_carrito:
            subtotal = cp.cantidad * cp.precio_unitario
            precio_total_general += subtotal
            print(f"  Producto {cp.producto_id}: {cp.cantidad} x {cp.precio_unitario} = {subtotal}")
        
        print(f"Total del pedido: {precio_total_general}")
        
        # Crear pedido (por ahora, un solo producto - temporal)
        primer_producto = productos_en_carrito[0]
        
        nuevo_pedido = pedido_create(
            db,
            precio_total=precio_total_general,
            metodo_pago=metodo_pago,
            id_comprador=id_comprador,
            id_producto=primer_producto.producto_id
        )
        print(f"Pedido creado con ID: {nuevo_pedido.id_pedido}")
        
        # Restar stock de productos
        for cp in productos_en_carrito:
            restar_stock(db, cp.producto_id, cp.cantidad)
            print(f"Stock actualizado para producto {cp.producto_id}")
        
        # Vaciar carrito
        vaciar_carrito(db, carrito.id_carrito)
        print("Carrito vaciado")
        
        return {
            "id_pedido": nuevo_pedido.id_pedido,
            "id_comprador": id_comprador,
            "precio_total": precio_total_general,
            "metodo_pago": metodo_pago,
            "mensaje": "Pedido creado exitosamente"
        }
    except Exception as e:
        print(f"ERROR en crear_pedido: {e}")
        print(traceback.format_exc())
        raise

def obtener_historial_pedidos(db: Session, id_comprador: int) -> Dict:
    try:
        print(f"=== OBTENER HISTORIAL ===")
        print(f"ID Comprador: {id_comprador}")
        
        pedidos = get_by_comprador_id(db, id_comprador)
        print(f"Pedidos encontrados: {len(pedidos)}")
        
        pedidos_response = [
            {
                "id_pedido": p.id_pedido,
                "fecha": str(p.fecha),
                "precio_total": p.precio_total,
                "metodo_pago": p.metodo_pago,
                "id_producto": p.id_producto,
                "nombre_producto": p.producto.nombre if p.producto else "Producto"
            }
            for p in pedidos
        ]
        
        return {
            "id_comprador": id_comprador,
            "cantidad_pedidos": len(pedidos_response),
            "pedidos": pedidos_response
        }
    except Exception as e:
        print(f"ERROR en obtener_historial_pedidos: {e}")
        print(traceback.format_exc())
        raise

def obtener_detalle_pedido(db: Session, id_pedido: int, id_comprador: int) -> Dict:
    try:
        print(f"=== OBTENER DETALLE PEDIDO ===")
        print(f"ID Pedido: {id_pedido}")
        print(f"ID Comprador: {id_comprador}")
        
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
            "id_producto": pedido.id_producto,
            "nombre_producto": pedido.producto.nombre if pedido.producto else "Producto",
            "precio_producto": pedido.producto.precio if pedido.producto else 0,
            "categoria_producto": pedido.producto.categoria if pedido.producto else ""
        }
    except Exception as e:
        print(f"ERROR en obtener_detalle_pedido: {e}")
        print(traceback.format_exc())
        raise