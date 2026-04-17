# services/usuario_admin_service.py
from typing import Dict
from sqlalchemy.orm import Session
from repositories.usuario_admin_repo import get_by_nombre, get_by_id, create
from auth import hash_password, verify_password, create_access_token
import traceback

def registrar_admin(db: Session, nombre: str, contrasena: str) -> Dict:
    try:
        print(f"=== INICIANDO REGISTRO ADMIN ===")
        print(f"Nombre: {nombre}")
        
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        admin_existente = get_by_nombre(db, nombre)
        if admin_existente:
            raise ValueError(f"El admin '{nombre}' ya existe")
        
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener mínimo 6 caracteres")
        
        print("Hasheando contraseña...")
        contrasena_hash = hash_password(contrasena)
        
        print("Creando admin en BD...")
        nuevo_admin = create(db, nombre, contrasena_hash)
        print(f"Admin creado con ID: {nuevo_admin.id_admin}")
        
        return {
            "id_admin": nuevo_admin.id_admin,
            "nombre": nuevo_admin.nombre,
            "mensaje": "Admin registrado exitosamente"
        }
    except Exception as e:
        print(f"ERROR en registrar_admin: {e}")
        print(traceback.format_exc())
        raise

def login_admin(db: Session, identificador: str, contrasena: str) -> Dict:
    print(f"=== INICIANDO LOGIN ADMIN ===")
    print(f"Identificador: {identificador}")
    
    admin = get_by_nombre(db, identificador)
    
    if not admin:
        raise ValueError("Admin no encontrado")
    
    print(f"Admin encontrado: {admin.nombre}")
    
    if not verify_password(contrasena, admin.contrasena):
        raise ValueError("Contraseña incorrecta")

    token = create_access_token({"sub": str(admin.id_admin), "role": "admin"})
    
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
        "nombre": admin.nombre
    }