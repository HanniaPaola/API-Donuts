from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Dict, List, Optional

from models.colaborador import Colaborador
from models.producto import Producto
from schemas.colaborador import ColaboradorCreate, ColaboradorUpdate


class ColaboradorRepository:
    """Repository for Colaborador CRUD operations"""

    @staticmethod
    def get_by_id(db: Session, colaborador_id: int) -> Optional[Colaborador]:
        """Get colaborador by ID"""
        return db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()

    @staticmethod
    def get_by_handle(db: Session, handle: str) -> Optional[Colaborador]:
        """Get colaborador by handle (unique)"""
        return db.query(Colaborador).filter(Colaborador.handle == handle).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Colaborador]:
        return (
            db.query(Colaborador)
            .filter(Colaborador.email == email.strip().lower())
            .first()
        )

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Colaborador]:
        """Get all colaboradores with pagination"""
        return db.query(Colaborador).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_active(db: Session) -> List[Colaborador]:
        """Get all active colaboradores"""
        return db.query(Colaborador).filter(Colaborador.status == "active").all()

    @staticmethod
    def get_by_specialty(db: Session, specialty: str) -> List[Colaborador]:
        """Get colaboradores by specialty (donas, galletas, bebidas)"""
        return (
            db.query(Colaborador)
            .filter(Colaborador.specialty == specialty)
            .filter(Colaborador.status == "active")
            .all()
        )

    @staticmethod
    def create(db: Session, colaborador_data: ColaboradorCreate, contrasena_hash: str) -> Colaborador:
        """Create new colaborador (contrasena ya hasheada)."""
        fields = colaborador_data.model_dump(exclude={"contrasena"})
        db_colaborador = Colaborador(contrasena=contrasena_hash, **fields)
        db.add(db_colaborador)
        db.commit()
        db.refresh(db_colaborador)
        return db_colaborador

    @staticmethod
    def update(
        db: Session, colaborador_id: int, update_data: ColaboradorUpdate
    ) -> Optional[Colaborador]:
        """Update colaborador"""
        db_colaborador = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not db_colaborador:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_colaborador, key, value)

        db.commit()
        db.refresh(db_colaborador)
        return db_colaborador

    @staticmethod
    def delete(db: Session, colaborador_id: int) -> bool:
        """Delete colaborador"""
        db_colaborador = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not db_colaborador:
            return False

        db.delete(db_colaborador)
        db.commit()
        return True

    @staticmethod
    def count(db: Session) -> int:
        """Get total count of colaboradores"""
        return db.query(Colaborador).count()

    @staticmethod
    def count_by_specialty(db: Session, specialty: str) -> int:
        """Get count of colaboradores by specialty"""
        return db.query(Colaborador).filter(Colaborador.specialty == specialty).count()

    @staticmethod
    def product_counts_for_ids(db: Session, colaborador_ids: List[int]) -> Dict[int, int]:
        """Filas en `producto` con `id_colaborador` por colaborador (para tarjetas públicas)."""
        if not colaborador_ids:
            return {}
        rows = (
            db.query(Producto.id_colaborador, func.count(Producto.id_producto))
            .filter(Producto.id_colaborador.in_(colaborador_ids))
            .group_by(Producto.id_colaborador)
            .all()
        )
        return {int(cid): int(n) for cid, n in rows if cid is not None}
