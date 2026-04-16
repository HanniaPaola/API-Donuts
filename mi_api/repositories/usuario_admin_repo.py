# repositories/usuario_admin_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session
from models.usuario_admin import UsuarioAdmin

def get_by_id(db: Session, id_admin: int) -> Optional[UsuarioAdmin]:
    return db.query(UsuarioAdmin).filter(UsuarioAdmin.id_admin == id_admin).first()

def get_by_nombre(db: Session, nombre: str) -> Optional[UsuarioAdmin]:
    return db.query(UsuarioAdmin).filter(UsuarioAdmin.nombre == nombre).first()

def create(db: Session, nombre: str, contrasena_hash: str) -> UsuarioAdmin:
    nuevo_admin = UsuarioAdmin(
        nombre=nombre,
        contrasena=contrasena_hash
    )
    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)
    return nuevo_admin

def get_all(db: Session) -> List[UsuarioAdmin]:
    return db.query(UsuarioAdmin).all()

def delete(db: Session, id_admin: int) -> bool:
    admin = get_by_id(db, id_admin)
    if admin:
        db.delete(admin)
        db.commit()
        return True
    return False