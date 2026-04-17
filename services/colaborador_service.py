import re
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from models.colaborador import Colaborador
from repositories import postulacion_colaborador_repo
from repositories.colaborador_repo import ColaboradorRepository
from schemas.colaborador import (
    ColaboradorCreate,
    ColaboradorUpdate,
    CollaboratorPublic,
)

VALID_SPECIALTIES = frozenset({"donas", "galletas", "bebidas"})


def _normalizar_handle(raw: str) -> str:
    h = raw.strip()
    if not h.startswith("@"):
        h = f"@{h.lstrip('@')}"
    return h


def _generar_handle_unico(db: Session, email: str) -> str:
    local = email.split("@")[0].lower()
    local = re.sub(r"[^a-z0-9_]", "_", local).strip("_")[:26] or "colab"
    i = 0
    while True:
        candidate = f"@{local}" if i == 0 else f"@{local}_{i}"
        if not ColaboradorRepository.get_by_handle(db, candidate):
            return candidate
        i += 1


def _to_public(c: Colaborador, product_count: int | None = None) -> CollaboratorPublic:
    """`product_count` real desde tabla `producto`; si es None se usa la columna (legado)."""
    pc = c.product_count if product_count is None else product_count
    return CollaboratorPublic(
        id=str(c.id),
        email=c.email,
        displayName=c.display_name,
        handle=c.handle,
        bio=c.bio,
        specialty=c.specialty,
        productCount=pc,
        salesCount=c.sales_count,
        isOnline=c.is_online,
        status=c.status,
    )


class ColaboradorService:
    """Service layer for Colaborador business logic and validations"""

    @staticmethod
    def get_all_colaboradores(db: Session, skip: int = 0, limit: int = 100) -> Dict:
        colaboradores = ColaboradorRepository.get_all(db, skip, limit)
        ids = [c.id for c in colaboradores]
        counts = ColaboradorRepository.product_counts_for_ids(db, ids)
        return {
            "colaboradores": [_to_public(c, counts.get(c.id, 0)) for c in colaboradores],
            "total": ColaboradorRepository.count(db),
        }

    @staticmethod
    def get_colaborador_by_id(db: Session, colaborador_id: int) -> CollaboratorPublic:
        colaborador = ColaboradorRepository.get_by_id(db, colaborador_id)
        if not colaborador:
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
        counts = ColaboradorRepository.product_counts_for_ids(db, [colaborador_id])
        return _to_public(colaborador, counts.get(colaborador_id, 0))

    @staticmethod
    def get_colaboradores_by_specialty(db: Session, specialty: str) -> List[CollaboratorPublic]:
        if specialty not in VALID_SPECIALTIES:
            raise ValueError(
                f"Invalid specialty. Must be one of: {', '.join(sorted(VALID_SPECIALTIES))}"
            )
        rows = ColaboradorRepository.get_by_specialty(db, specialty)
        ids = [c.id for c in rows]
        counts = ColaboradorRepository.product_counts_for_ids(db, ids)
        return [_to_public(c, counts.get(c.id, 0)) for c in rows]

    @staticmethod
    def get_online_colaboradores(db: Session) -> List[CollaboratorPublic]:
        rows = (
            db.query(Colaborador)
            .filter(Colaborador.is_online.is_(True))
            .filter(Colaborador.status == "active")
            .all()
        )
        ids = [c.id for c in rows]
        counts = ColaboradorRepository.product_counts_for_ids(db, ids)
        return [_to_public(c, counts.get(c.id, 0)) for c in rows]

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
        pwd = data.pop("contrasena", None)
        if not pwd:
            raise ValueError("La contraseña es obligatoria")
        normalized = ColaboradorCreate(**data, contrasena=pwd)
        created = ColaboradorRepository.create(db, normalized, hash_password(pwd))
        return _to_public(created)

    @staticmethod
    def activar_cuenta_desde_postulacion(
        db: Session,
        email: str,
        contrasena: str,
        handle_opcional: Optional[str] = None,
    ) -> CollaboratorPublic:
        """Crea el registro en `colaboradores` solo si existe postulación aceptada para ese correo."""
        email_norm = email.strip().lower()
        post = postulacion_colaborador_repo.get_latest_by_email(db, email_norm)
        if post is None:
            raise ValueError(
                "No hay postulación registrada con ese correo. Primero envía tu solicitud como colaborador."
            )
        estado = (post.estado or "").strip().lower()
        if estado != "aceptada":
            raise ValueError(
                "Solo puedes activar tu cuenta cuando tu postulación esté aceptada. "
                "Si aún está en revisión, espera la confirmación del equipo."
            )

        existente = ColaboradorRepository.get_by_email(db, email_norm)
        if existente is not None:
            if existente.contrasena:
                raise ValueError(
                    "Este correo ya tiene cuenta de colaborador. Inicia sesión en lugar de registrarte."
                )
            raise ValueError(
                "Existe un perfil incompleto para este correo. Contacta al administrador."
            )

        if handle_opcional and handle_opcional.strip():
            handle = _normalizar_handle(handle_opcional)
            if ColaboradorRepository.get_by_handle(db, handle):
                raise ValueError(f"El handle '{handle}' ya está en uso. Prueba otro o déjalo vacío para generar uno.")
        else:
            handle = _generar_handle_unico(db, email_norm)

        sp = (post.specialty or "").strip().lower()
        if sp not in VALID_SPECIALTIES:
            raise ValueError("La especialidad de tu postulación no es válida. Contacta al administrador.")

        payload = ColaboradorCreate(
            email=email_norm,
            contrasena=contrasena,
            display_name=post.nombre_completo.strip(),
            handle=handle,
            bio=(post.mensaje.strip() if post.mensaje else None) or None,
            specialty=sp,
            product_count=0,
            sales_count=0,
            is_online=False,
            status="active",
        )
        return ColaboradorService.create_colaborador(db, payload)

    @staticmethod
    def login_colaborador(db: Session, email: str, contrasena: str) -> Dict:
        row = ColaboradorRepository.get_by_email(db, email)
        if not row:
            raise ValueError("Colaborador no encontrado")
        if not row.contrasena:
            raise ValueError(
                "Esta cuenta no tiene contraseña de acceso. Regístrate de nuevo con contraseña o pide a un administrador que actualice tu perfil."
            )
        if (row.status or "").strip().lower() != "active":
            raise ValueError("Colaborador inactivo")
        if not verify_password(contrasena, row.contrasena):
            raise ValueError("Contraseña incorrecta")
        token = create_access_token({"sub": str(row.id), "role": "collaborator"})
        return {
            "id": row.id,
            "email": row.email,
            "display_name": row.display_name,
            "nombre": row.display_name,
            "role": "collaborator",
            "token": token,
            "tipo_token": "bearer",
        }

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
        counts = ColaboradorRepository.product_counts_for_ids(db, [colaborador_id])
        return _to_public(updated, counts.get(colaborador_id, 0))

    @staticmethod
    def delete_colaborador(db: Session, colaborador_id: int) -> None:
        if not ColaboradorRepository.delete(db, colaborador_id):
            raise ValueError(f"Colaborador with id {colaborador_id} not found")
