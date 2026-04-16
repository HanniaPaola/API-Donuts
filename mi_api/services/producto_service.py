# services/producto_service.py
from typing import Dict, List
from sqlalchemy.orm import Session
from repositories.producto_repo import get_by_id, get_all, get_by_categoria, create, update, delete, restar_stock, sumar_stock
from repositories.usuario_admin_repo import get_by_id as get_admin_by_id
import traceback

def obtener_producto(db: Session, id_producto: int) -> Dict:
    producto = get_by_id(db, id_producto)
    
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")
    
    return {
        "id_producto": producto.id_producto,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "categoria": producto.categoria,
        "stock_disponible": producto.stock_disponible,
        "id_admin": producto.id_admin
    }

def obtener_todos_productos(db: Session) -> List[Dict]:
    productos = get_all(db)
    return [
        {
            "id": p.id_producto,
            "nombre": p.nombre,
            "categoria": p.categoria,
            "precio": p.precio,
            "estado": "activo" if p.stock_disponible > 0 else "agotado",
            "stock": p.stock_disponible,
            "colaborador_nombre": "Admin",
            "ventas_count": 0
        }
        for p in productos
    ]

def obtener_productos_por_categoria(db: Session, categoria: str) -> List[Dict]:
    productos = get_by_categoria(db, categoria)
    return [
        {
            "id_producto": p.id_producto,
            "nombre": p.nombre,
            "precio": p.precio,
            "categoria": p.categoria,
            "stock_disponible": p.stock_disponible,
            "id_admin": p.id_admin
        }
        for p in productos
    ]

def crear_producto(db: Session, nombre: str, precio: float, categoria: str,
                   stock_disponible: int, id_admin: int) -> Dict:
    try:
        print("=== INICIANDO crear_producto ===")
        
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if stock_disponible < 0:
            raise ValueError("El stock no puede ser negativo")
        
        print(f"Buscando admin con ID: {id_admin}")
        admin = get_admin_by_id(db, id_admin)
        if not admin:
            raise ValueError(f"Admin con ID {id_admin} no encontrado")
        
        print("Creando producto...")
        nuevo_producto = create(
            db,
            nombre=nombre,
            precio=precio,
            categoria=categoria,
            stock_disponible=stock_disponible,
            id_admin=id_admin
        )
        
        print(f"Producto creado con ID: {nuevo_producto.id_producto}")
        
        return {
            "id_producto": nuevo_producto.id_producto,
            "nombre": nuevo_producto.nombre,
            "precio": nuevo_producto.precio,
            "categoria": nuevo_producto.categoria,
            "stock_disponible": nuevo_producto.stock_disponible,
            "id_admin": nuevo_producto.id_admin,
            "mensaje": "Producto creado exitosamente"
        }
    except Exception as e:
        print(f"ERROR en crear_producto: {e}")
        print(traceback.format_exc())
        raise

def actualizar_producto(db: Session, id_producto: int, datos: Dict, id_admin: int) -> Dict:
    producto = get_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")
    
    if producto.id_admin != id_admin:
        raise ValueError("No tienes permiso para actualizar este producto")
    
    if "precio" in datos and datos["precio"] is not None:
        if datos["precio"] <= 0:
            raise ValueError("El precio debe ser mayor a 0")
    
    if "stock_disponible" in datos and datos["stock_disponible"] is not None:
        if datos["stock_disponible"] < 0:
            raise ValueError("El stock no puede ser negativo")
    
    datos_filtrados = {k: v for k, v in datos.items() if v is not None}
    
    producto_actualizado = update(db, id_producto, datos_filtrados)
    
    return {
        "id_producto": producto_actualizado.id_producto,
        "nombre": producto_actualizado.nombre,
        "precio": producto_actualizado.precio,
        "categoria": producto_actualizado.categoria,
        "stock_disponible": producto_actualizado.stock_disponible,
        "id_admin": producto_actualizado.id_admin,
        "mensaje": "Producto actualizado exitosamente"
    }

def eliminar_producto(db: Session, id_producto: int, id_admin: int) -> Dict:
    producto = get_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")
    
    if producto.id_admin != id_admin:
        raise ValueError("No tienes permiso para eliminar este producto")
    
    delete(db, id_producto)
    
    return {
        "id_producto": id_producto,
        "mensaje": "Producto eliminado exitosamente"
    }