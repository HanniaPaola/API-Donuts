# services/producto_service.py
import logging
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models.producto import Producto
from repositories.colaborador_repo import ColaboradorRepository
from repositories.producto_repo import (
    create,
    delete,
    get_all,
    get_by_admin_id,
    get_by_categoria,
    get_by_colaborador_id,
    get_by_id,
    update,
)
from repositories import usuario_admin_repo
from repositories.usuario_admin_repo import get_by_id as get_admin_by_id

logger = logging.getLogger(__name__)


def _primer_id_admin(db: Session) -> int:
    admins = usuario_admin_repo.get_all(db)
    if not admins:
        raise ValueError(
            "No hay administrador registrado; hace falta uno para asociar productos de colaboradores."
        )
    admins.sort(key=lambda a: a.id_admin)
    return admins[0].id_admin


def _producto_item_lista_publica(p: Producto) -> Dict:
    col_nombre = "—"
    if p.colaborador is not None:
        col_nombre = p.colaborador.display_name
    elif p.admin is not None and p.admin.nombre:
        col_nombre = p.admin.nombre
    return {
        "id": p.id_producto,
        "nombre": p.nombre,
        "categoria": p.categoria,
        "precio": p.precio,
        "estado": "activo" if p.stock_disponible > 0 else "agotado",
        "stock": p.stock_disponible,
        "colaborador_nombre": col_nombre,
        "ventas_count": 0,
        "id_colaborador": p.id_colaborador,
    }


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
        "id_admin": producto.id_admin,
        "id_colaborador": producto.id_colaborador,
    }


def obtener_todos_productos(db: Session) -> List[Dict]:
    productos = get_all(db)
    return [_producto_item_lista_publica(p) for p in productos]


def obtener_mis_productos_admin(db: Session, id_admin: int) -> List[Dict]:
    productos = get_by_admin_id(db, id_admin)
    return [_producto_item_lista_publica(p) for p in productos]


def obtener_mis_productos_colaborador(db: Session, id_colaborador: int) -> List[Dict]:
    col = ColaboradorRepository.get_by_id(db, id_colaborador)
    if not col:
        raise ValueError(f"Colaborador con id {id_colaborador} no encontrado")
    productos = get_by_colaborador_id(db, id_colaborador)
    return [_producto_item_lista_publica(p) for p in productos]


def obtener_productos_menu_colaborador(db: Session, colaborador_id: int) -> List[Dict]:
    col = ColaboradorRepository.get_by_id(db, colaborador_id)
    if not col:
        raise ValueError(f"Colaborador con id {colaborador_id} no encontrado")
    productos = get_by_colaborador_id(db, colaborador_id)
    return [_producto_item_lista_publica(p) for p in productos]


def obtener_productos_por_categoria(db: Session, categoria: str) -> List[Dict]:
    productos = get_by_categoria(db, categoria)
    return [
        {
            "id_producto": p.id_producto,
            "nombre": p.nombre,
            "precio": p.precio,
            "categoria": p.categoria,
            "stock_disponible": p.stock_disponible,
            "id_admin": p.id_admin,
        }
        for p in productos
    ]


def crear_producto(
    db: Session,
    nombre: str,
    precio: float,
    categoria: Optional[str],
    stock_disponible: int,
    id_admin: int,
    id_colaborador: Optional[int] = None,
) -> Dict:
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del producto no puede estar vacío")

    if precio <= 0:
        raise ValueError("El precio debe ser mayor a 0")

    if stock_disponible < 0:
        raise ValueError("El stock no puede ser negativo")

    admin = get_admin_by_id(db, id_admin)
    if not admin:
        raise ValueError(f"Admin con ID {id_admin} no encontrado")

    if id_colaborador is not None:
        if not ColaboradorRepository.get_by_id(db, id_colaborador):
            raise ValueError(f"Colaborador con id {id_colaborador} no encontrado")

    nuevo_producto = create(
        db,
        nombre=nombre,
        precio=precio,
        categoria=categoria,
        stock_disponible=stock_disponible,
        id_admin=id_admin,
        id_colaborador=id_colaborador,
    )

    logger.info(
        "Producto creado id_producto=%s id_admin=%s id_colaborador=%s",
        nuevo_producto.id_producto,
        id_admin,
        id_colaborador,
    )

    return {
        "id_producto": nuevo_producto.id_producto,
        "nombre": nuevo_producto.nombre,
        "precio": nuevo_producto.precio,
        "categoria": nuevo_producto.categoria,
        "stock_disponible": nuevo_producto.stock_disponible,
        "id_admin": nuevo_producto.id_admin,
        "id_colaborador": nuevo_producto.id_colaborador,
        "mensaje": "Producto creado exitosamente",
    }


def crear_producto_colaborador(
    db: Session,
    nombre: str,
    precio: float,
    categoria: Optional[str],
    stock_disponible: int,
    id_colaborador: int,
) -> Dict:
    col = ColaboradorRepository.get_by_id(db, id_colaborador)
    if not col:
        raise ValueError(f"Colaborador con id {id_colaborador} no encontrado")
    if (col.status or "active").strip().lower() != "active":
        raise ValueError("Colaborador inactivo")
    id_admin = _primer_id_admin(db)
    return crear_producto(
        db,
        nombre,
        precio,
        categoria,
        stock_disponible,
        id_admin,
        id_colaborador,
    )


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

    datos_filtrados: Dict = {}
    for k, v in datos.items():
        if k == "id_colaborador":
            datos_filtrados[k] = v
        elif v is not None:
            datos_filtrados[k] = v

    if "id_colaborador" in datos_filtrados:
        ic = datos_filtrados["id_colaborador"]
        if ic is not None and not ColaboradorRepository.get_by_id(db, ic):
            raise ValueError(f"Colaborador con id {ic} no encontrado")

    producto_actualizado = update(db, id_producto, datos_filtrados)

    logger.info("Producto actualizado id_producto=%s", id_producto)

    return {
        "id_producto": producto_actualizado.id_producto,
        "nombre": producto_actualizado.nombre,
        "precio": producto_actualizado.precio,
        "categoria": producto_actualizado.categoria,
        "stock_disponible": producto_actualizado.stock_disponible,
        "id_admin": producto_actualizado.id_admin,
        "id_colaborador": producto_actualizado.id_colaborador,
        "mensaje": "Producto actualizado exitosamente",
    }


def eliminar_producto(db: Session, id_producto: int, id_admin: int) -> Dict:
    producto = get_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")

    if producto.id_admin != id_admin:
        raise ValueError("No tienes permiso para eliminar este producto")

    delete(db, id_producto)

    logger.info("Producto eliminado id_producto=%s", id_producto)

    return {
        "id_producto": id_producto,
        "mensaje": "Producto eliminado exitosamente",
    }


def actualizar_producto_colaborador(
    db: Session, id_producto: int, datos: Dict, id_colaborador: int
) -> Dict:
    producto = get_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")
    if producto.id_colaborador != id_colaborador:
        raise ValueError("No tienes permiso para actualizar este producto")

    if "precio" in datos and datos["precio"] is not None:
        if datos["precio"] <= 0:
            raise ValueError("El precio debe ser mayor a 0")

    if "stock_disponible" in datos and datos["stock_disponible"] is not None:
        if datos["stock_disponible"] < 0:
            raise ValueError("El stock no puede ser negativo")

    datos_filtrados: Dict = {}
    for k, v in datos.items():
        if k == "id_colaborador":
            continue
        if v is not None:
            datos_filtrados[k] = v

    producto_actualizado = update(db, id_producto, datos_filtrados)

    logger.info("Producto actualizado por colaborador id_producto=%s", id_producto)

    return {
        "id_producto": producto_actualizado.id_producto,
        "nombre": producto_actualizado.nombre,
        "precio": producto_actualizado.precio,
        "categoria": producto_actualizado.categoria,
        "stock_disponible": producto_actualizado.stock_disponible,
        "id_admin": producto_actualizado.id_admin,
        "id_colaborador": producto_actualizado.id_colaborador,
        "mensaje": "Producto actualizado exitosamente",
    }


def eliminar_producto_colaborador(db: Session, id_producto: int, id_colaborador: int) -> Dict:
    producto = get_by_id(db, id_producto)
    if not producto:
        raise ValueError(f"Producto con ID {id_producto} no encontrado")
    if producto.id_colaborador != id_colaborador:
        raise ValueError("No tienes permiso para eliminar este producto")

    delete(db, id_producto)

    logger.info("Producto eliminado por colaborador id_producto=%s", id_producto)

    return {
        "id_producto": id_producto,
        "mensaje": "Producto eliminado exitosamente",
    }
