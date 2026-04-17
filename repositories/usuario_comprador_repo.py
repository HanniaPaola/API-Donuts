# repositories/usuario_comprador_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session
from models.usuario_comprador import UsuarioComprador

def get_by_id(db: Session, id_comprador: int) -> Optional[UsuarioComprador]:
    return db.query(UsuarioComprador).filter(UsuarioComprador.id_comprador == id_comprador).first()

def get_by_nombre(db: Session, nombre: str) -> Optional[UsuarioComprador]:
    return db.query(UsuarioComprador).filter(UsuarioComprador.nombre == nombre).first()

def create(db: Session, nombre: str, contrasena_hash: str) -> UsuarioComprador:
    nuevo_comprador = UsuarioComprador(
        nombre=nombre,
        contrasena=contrasena_hash
    )
    db.add(nuevo_comprador)
    db.commit()
    db.refresh(nuevo_comprador)
    return nuevo_comprador

def get_all(db: Session) -> List[UsuarioComprador]:
    return db.query(UsuarioComprador).all()

def delete(db: Session, id_comprador: int) -> bool:
    comprador = get_by_id(db, id_comprador)
    if comprador:
        db.delete(comprador)
        db.commit()
        return True
    return False