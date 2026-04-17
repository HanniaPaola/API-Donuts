# services/usuario_comprador_service.py
from typing import Dict, List
from sqlalchemy.orm import Session
from repositories.usuario_comprador_repo import get_by_nombre, get_by_id, create, get_all
from repositories.carrito import create as create_carrito
from auth import hash_password, verify_password, create_access_token

def registrar_comprador(db: Session, nombre: str, contrasena: str) -> Dict:
    print(f"=== INICIANDO REGISTRO ===")
    print(f"Nombre: {nombre}")
    print(f"Contraseña length: {len(contrasena)}")
    
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")
    
    # Verificar si ya existe
    comprador_existente = get_by_nombre(db, nombre)
    if comprador_existente:
        raise ValueError(f"El comprador '{nombre}' ya existe")
    
    if len(contrasena) < 6:
        raise ValueError("La contraseña debe tener mínimo 6 caracteres")
    
    # Hashear contraseña
    print("Hasheando contraseña...")
    contrasena_hash = hash_password(contrasena)
    print(f"Hash generado: {contrasena_hash[:20]}...")
    
    # Crear comprador
    print("Creando comprador en BD...")
    nuevo_comprador = create(db, nombre, contrasena_hash)
    print(f"Comprador creado con ID: {nuevo_comprador.id_comprador}")
    
    # Crear carrito automáticamente
    print("Creando carrito...")
    create_carrito(db, nuevo_comprador.id_comprador)
    print("Carrito creado exitosamente")
    
    return {
        "id_comprador": nuevo_comprador.id_comprador,
        "nombre": nuevo_comprador.nombre,
        "mensaje": "Comprador registrado exitosamente"
    }

def login_comprador(db: Session, identificador: str, contrasena: str) -> Dict:
    print(f"=== INICIANDO LOGIN ===")
    print(f"Identificador: {identificador}")
    
    comprador = get_by_nombre(db, identificador)
    
    if not comprador:
        raise ValueError("Comprador no encontrado")
    
    print(f"Comprador encontrado: {comprador.nombre}")
    
    if not verify_password(contrasena, comprador.contrasena):
        raise ValueError("Contraseña incorrecta")

    token = create_access_token({"sub": str(comprador.id_comprador)})
    
    return {
        "id": comprador.id_comprador,
        "email": comprador.nombre,
        "display_name": comprador.nombre,
        "nombre": comprador.nombre,
        "token": token,
        "tipo_token": "bearer"
    }

def obtener_comprador(db: Session, id_comprador: int) -> Dict:
    comprador = get_by_id(db, id_comprador)
    
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
    
    return {
        "id_comprador": comprador.id_comprador,
        "nombre": comprador.nombre
    }

def obtener_detalle_comprador(db: Session, id_comprador: int) -> Dict:
    comprador = get_by_id(db, id_comprador)
    
    if not comprador:
        raise ValueError(f"Comprador con ID {id_comprador} no encontrado")
    
    return {
        "id": comprador.id_comprador,
        "email": comprador.nombre,
        "nombre": comprador.nombre,
        "telefono": "",
        "direccion": "",
        "ciudad": "",
        "estado": "",
        "codigo_postal": ""
    }

def obtener_todos_compradores(db: Session) -> List[Dict]:
    compradores = get_all(db)
    return [
        {
            "id_comprador": c.id_comprador,
            "nombre": c.nombre
        }
        for c in compradores
    ]