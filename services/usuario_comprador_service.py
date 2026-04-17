# services/usuario_comprador_service.py
import logging
from typing import Dict, List

from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from repositories.carrito import create as create_carrito
from repositories.usuario_comprador_repo import create, get_all, get_by_id, get_by_nombre

logger = logging.getLogger(__name__)


def registrar_comprador(db: Session, nombre: str, contrasena: str) -> Dict:
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")

    if get_by_nombre(db, nombre):
        raise ValueError(f"El comprador '{nombre}' ya existe")

    if len(contrasena) < 6:
        raise ValueError("La contraseña debe tener mínimo 6 caracteres")

    contrasena_hash = hash_password(contrasena)
    nuevo_comprador = create(db, nombre, contrasena_hash)
    create_carrito(db, nuevo_comprador.id_comprador)

    logger.info("Comprador registrado id_comprador=%s", nuevo_comprador.id_comprador)

    return {
        "id_comprador": nuevo_comprador.id_comprador,
        "nombre": nuevo_comprador.nombre,
        "mensaje": "Comprador registrado exitosamente",
    }


def login_comprador(db: Session, identificador: str, contrasena: str) -> Dict:
    comprador = get_by_nombre(db, identificador)

    if not comprador:
        raise ValueError("Comprador no encontrado")

    if not verify_password(contrasena, comprador.contrasena):
        raise ValueError("Contraseña incorrecta")

    token = create_access_token(
        {"sub": str(comprador.id_comprador), "role": "buyer"}
    )

    logger.info("Login comprador id=%s", comprador.id_comprador)

    return {
        "id": comprador.id_comprador,
        "email": comprador.nombre,
        "display_name": comprador.nombre,
        "nombre": comprador.nombre,
        "role": "buyer",
        "token": token,
        "tipo_token": "bearer",
    }


def obtener_comprador(db: Session, id_comprador: int) -> Dict:
    comprador = get_by_id(db, id_comprador)

    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")

    return {
        "id_comprador": comprador.id_comprador,
        "nombre": comprador.nombre,
    }


def obtener_detalle_comprador(db: Session, id_comprador: int) -> Dict:
    comprador = get_by_id(db, id_comprador)

    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")

    return {
        "id_comprador": comprador.id_comprador,
        "email": comprador.nombre,
        "nombre": comprador.nombre,
        "telefono": "",
        "direccion": "",
        "ciudad": "",
        "estado": "",
        "codigo_postal": "",
    }


def obtener_todos_compradores(db: Session) -> List[Dict]:
    compradores = get_all(db)
    return [
        {
            "id_comprador": c.id_comprador,
            "nombre": c.nombre,
        }
        for c in compradores
    ]
