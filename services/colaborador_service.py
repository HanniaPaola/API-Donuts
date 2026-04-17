from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from models.colaborador import Colaborador
from repositories.colaborador_repo import ColaboradorRepository
from schemas.colaborador import (
    ColaboradorCreate,
    ColaboradorUpdate,
    CollaboratorPublic,
)

VALID_SPECIALTIES = frozenset({"donas", "galletas", "bebidas"})


def _to_public(c: Colaborador) -> CollaboratorPublic:
    return CollaboratorPublic(
        id=str(c.id),
        email=c.email,
        displayName=c.display_name,
        handle=c.handle,
        bio=c.bio,
        specialty=c.specialty,
        productCount=c.product_count,
        salesCount=c.sales_count,
        isOnline=c.is_online,
        status=c.status,
    )


class ColaboradorService:
    """Service layer for Colaborador business logic and validations"""

    @staticmethod
    def get_all_colaboradores(db: Session, skip: int = 0, limit: int = 100) -> Dict:
        colaboradores = ColaboradorRepository.get_all(db, skip, limit)
        return {
            "colaboradores": [_to_public(c) for c in colaboradores],
            "total": ColaboradorRepository.count(db),
        }

    @staticmethod
    def get_colaborador_by_id(db: Session, colaborador_id: int) -> CollaboratorPublic:
        colaborador = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not colaborador:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
        return _to_public(colaborador)

    @staticmethod
    def get_colaboradores_by_specialty(db: Session, specialty: str) -> List[CollaboratorPublic]:
        if specialty not in VALID_SPECIALTIES:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(sorted(VALID_SPECIALTIES))}"
            )
        rows = ColaboradorRepository.get_by_specialty(db, specialty)
        return [_to_public(c) for c in rows]

    @staticmethod
    def get_online_colaboradores(db: Session) -> List[CollaboratorPublic]:
        rows = (
            db.query(Colaborador)
            .filter(Colaborador.is_online.is_(True))
            .filter(Colaborador.status == "active")
            .all()
        )
        return [_to_public(c) for c in rows]

    @staticmethod
    def create_colaborador(db: Session, colaborador_data: ColaboradorCreate) -> CollaboratorPublic:
        if colaborador_data.specialty not in VALID_SPECIALTIES:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(sorted(VALID_SPECIALTIES))}"
            )

        existing = ColaboradorRepository.get_by_handle(db, colaborador_data.handle)
        if existing:
            raise ValueError(f"Handle '{colaborador_data.handle}' already exists")

        existing_email = (
            db.query(Colaborador)
            .filter(Colaborador.email == colaborador_data.email.strip().lower())
            .first()
        )
        if existing_email:
            raise ValueError(f"Email '{colaborador_data.email}' already exists")

        if not colaborador_data.display_name.strip():
            raise ValueError("Display name cannot be empty")

        if not colaborador_data.handle.strip():
            raise ValueError("Handle cannot be empty")

        data = colaborador_data.model_dump()
        data["email"] = data["email"].strip().lower()
        normalized = ColaboradorCreate(**data)
        created = ColaboradorRepository.create(db, normalized)
        return _to_public(created)

    @staticmethod
    def update_colaborador(
        db: Session, colaborador_id: int, update_data: ColaboradorUpdate
    ) -> CollaboratorPublic:
        existing = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not existing:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")

        if update_data.specialty and update_data.specialty not in VALID_SPECIALTIES:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(sorted(VALID_SPECIALTIES))}"
            )

        if update_data.handle and update_data.handle != existing.handle:
            handle_exists = ColaboradorRepository.get_by_handle(db, update_data.handle)
            if handle_exists:
                raise ValueError(f"Handle '{update_data.handle}' already exists")

        if update_data.email:
            email_norm = update_data.email.strip().lower()
            other = (
                db.query(Colaborador)
                .filter(Colaborador.email == email_norm)
                .filter(Colaborador.id != colaborador_id)
                .first()
            )
            if other:
                raise ValueError(f"Email '{update_data.email}' already exists")
            update_data = update_data.model_copy(update={"email": email_norm})

        updated = ColaboradorRepository.update(db, colaborador_id, update_data)
        if not updated:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
        return _to_public(updated)

    @staticmethod
    def delete_colaborador(db: Session, colaborador_id: int) -> None:
        if not ColaboradorRepository.delete(db, colaborador_id):
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
