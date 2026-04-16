from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from repositories.colaborador_repo import ColaboradorRepository
from schemas.colaborador import ColaboradorCreate, ColaboradorUpdate

# Resto del código...


class ColaboradorService:
    """Service layer for Colaborador business logic and validations"""

    @staticmethod
    def get_all_colaboradores(db: Session, skip: int = 0, limit: int = 100) -> Dict:
        colaboradores = ColaboradorRepository.get_all(db, skip, limit)
        # Transformar al formato que espera el frontend
        colaboradores_transformados = [
            {
                "id": c.id,
                "display_name": c.display_name,
                "handle": c.handle,
                "bio": c.bio,
                "specialty": c.specialty,
                "product_count": c.product_count,
                "sales_count": c.sales_count,
                "is_online": c.is_online,
                "status": c.status
            }
            for c in colaboradores
        ]
        return {
            "colaboradores": colaboradores_transformados,
            "total": ColaboradorRepository.count(db),
        }

    @staticmethod
    def get_colaborador_by_id(db: Session, colaborador_id: int) -> Optional[object]:
        """Get single colaborador by ID"""
        colaborador = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not colaborador:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
        return colaborador

    @staticmethod
    def get_colaboradores_by_specialty(db: Session, specialty: str) -> List:
        """Get all colaboradores by specialty"""
        valid_specialties = ["donas", "galletas", "bebidas"]
        if specialty not in valid_specialties:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(valid_specialties)}"
            )
        return ColaboradorRepository.get_by_specialty(db, specialty)

    @staticmethod
    def create_colaborador(db: Session, colaborador_data: ColaboradorCreate) -> object:
        """Create new colaborador with validation"""
        # Validate specialty
        valid_specialties = ["donas", "galletas", "bebidas"]
        if colaborador_data.specialty not in valid_specialties:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(valid_specialties)}"
            )

        # Check if handle already exists
        existing = ColaboradorRepository.get_by_handle(db, colaborador_data.handle)
        if existing:
            raise ValueError(f"Handle '{colaborador_data.handle}' already exists")

        # Validate display_name not empty
        if not colaborador_data.display_name.strip():
            raise ValueError("Display name cannot be empty")

        # Validate handle not empty
        if not colaborador_data.handle.strip():
            raise ValueError("Handle cannot be empty")

        return ColaboradorRepository.create(db, colaborador_data)

    @staticmethod
    def update_colaborador(
        db: Session, colaborador_id: int, update_data: ColaboradorUpdate
    ) -> object:
        """Update colaborador with validation"""
        # Check exists
        existing = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not existing:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")

        # Validate specialty if provided
        if update_data.specialty:
            valid_specialties = ["donas", "galletas", "bebidas"]
            if update_data.specialty not in valid_specialties:
                raise ValueError(
                    f"Invalid specialty. Must be one of: {', '.join(valid_specialties)}"
                )

        # Check handle uniqueness if being updated
        if update_data.handle and update_data.handle != existing.handle:
            handle_exists = ColaboradorRepository.get_by_handle(db, update_data.handle)
            if handle_exists:
                raise ValueError(f"Handle '{update_data.handle}' already exists")

        return ColaboradorRepository.update(db, colaborador_id, update_data)

    @staticmethod
    def delete_colaborador(db: Session, colaborador_id: int):
        """Delete colaborador"""
        if not ColaboradorRepository.delete(db, colaborador_id):
            raise ValueError(f"Colaborador with id {colaborador_id} not found")

    @staticmethod
    def get_online_colaboradores(db: Session) -> List:
        """Get all online colaboradores"""
        return (
            db.query(ColaboradorRepository.get_all(db))
            if hasattr(ColaboradorRepository, "get_all")
            else []
        )
