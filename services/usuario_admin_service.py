# services/usuario_admin_service.py
import logging
from typing import Dict

from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from repositories.usuario_admin_repo import create, get_by_id, get_by_nombre

logger = logging.getLogger(__name__)


def registrar_admin(db: Session, nombre: str, contrasena: str) -> Dict:
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")

    if get_by_nombre(db, nombre):
        raise ValueError(f"El admin '{nombre}' ya existe")

    if len(contrasena) < 6:
        raise ValueError("La contraseña debe tener mínimo 6 caracteres")

    contrasena_hash = hash_password(contrasena)
    nuevo_admin = create(db, nombre, contrasena_hash)

    logger.info("Admin registrado id_admin=%s", nuevo_admin.id_admin)

    return {
        "id_admin": nuevo_admin.id_admin,
        "nombre": nuevo_admin.nombre,
        "mensaje": "Admin registrado exitosamente",
    }


def login_admin(db: Session, identificador: str, contrasena: str) -> Dict:
    admin = get_by_nombre(db, identificador)

    if not admin:
        raise ValueError("Admin no encontrado")

    if not verify_password(contrasena, admin.contrasena):
        raise ValueError("Contraseña incorrecta")

    token = create_access_token({"sub": str(admin.id_admin), "role": "admin"})

    logger.info("Login admin id=%s", admin.id_admin)

    return {
        "id": admin.id_admin,
        "email": admin.nombre,
        "display_name": admin.nombre,
        "nombre": admin.nombre,
        "role": "admin",
        "token": token,
        "tipo_token": "bearer",
    }


def obtener_admin(db: Session, id_admin: int) -> Dict:
    admin = get_by_id(db, id_admin)

    if not admin:
        raise ValueError(f"Admin con ID {id_admin} no encontrado")

    return {
        "id_admin": admin.id_admin,
        "nombre": admin.nombre,
    }
