import logging
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from repositories import postulacion_colaborador_repo
from repositories import usuario_comprador_repo
from services.colaborador_service import VALID_SPECIALTIES

logger = logging.getLogger(__name__)


def crear_postulacion(
    db: Session,
    nombre_completo: str,
    email: str,
    telefono: str,
    specialty: str,
    mensaje: str | None,
    id_comprador_sesion: int | None = None,
) -> Dict:
    sp = specialty.strip().lower()
    if sp not in VALID_SPECIALTIES:
        raise ValueError("Especialidad no válida. Use: donas, galletas o bebidas.")

    id_comprador: int | None = None
    email_final = str(email).strip().lower()

    if id_comprador_sesion is not None:
        comprador = usuario_comprador_repo.get_by_id(db, id_comprador_sesion)
        if not comprador:
            raise ValueError("Sesión de comprador no válida.")
        email_cuenta = comprador.nombre.strip().lower()
        if email_final != email_cuenta:
            raise ValueError(
                "El correo debe ser el mismo con el que inicias sesión como comprador para vincular tu solicitud."
            )
        email_final = email_cuenta
        id_comprador = id_comprador_sesion

    row = postulacion_colaborador_repo.create(
        db,
        nombre_completo=nombre_completo.strip(),
        email=email_final,
        telefono=telefono,
        specialty=sp,
        mensaje=mensaje,
        id_comprador=id_comprador,
    )
    logger.info(
        "Postulación colaborador id=%s email=%s id_comprador=%s",
        row.id,
        row.email,
        id_comprador,
    )
    return {
        "id": row.id,
        "mensaje": "Tu postulación fue recibida. Nos pondremos en contacto pronto.",
    }


def listar_postulaciones_admin(db: Session) -> Dict:
    rows = postulacion_colaborador_repo.list_all_ordered(db)
    items: List[Dict] = []
    for r in rows:
        items.append(
            {
                "id": r.id,
                "id_comprador": r.id_comprador,
                "nombre_completo": r.nombre_completo,
                "email": r.email,
                "telefono": r.telefono,
                "specialty": r.specialty,
                "mensaje": r.mensaje,
                "estado": r.estado or "pendiente",
                "creado_en": r.creado_en.isoformat() if r.creado_en else "",
            }
        )
    return {"postulaciones": items, "total": len(items)}


def obtener_postulacion_colaborador_mia(db: Session, id_comprador: int) -> Optional[Dict]:
    """Última postulación cuyo correo coincide con el identificador del comprador (campo `nombre`)."""
    comprador = usuario_comprador_repo.get_by_id(db, id_comprador)
    if not comprador:
        return None
    email_clave = comprador.nombre.strip().lower()
    row = postulacion_colaborador_repo.get_latest_by_email(db, email_clave)
    if not row:
        return None
    return {
        "id": row.id,
        "nombre_completo": row.nombre_completo,
        "email": row.email,
        "telefono": row.telefono,
        "specialty": row.specialty,
        "mensaje": row.mensaje,
        "estado": row.estado or "pendiente",
        "creado_en": row.creado_en.isoformat() if row.creado_en else "",
    }


def actualizar_estado_postulacion_admin(
    db: Session,
    postulacion_id: int,
    nuevo_estado: str,
) -> Dict:
    row = postulacion_colaborador_repo.get_by_id(db, postulacion_id)
    if row is None:
        raise ValueError("Postulación no encontrada.")
    actual = (row.estado or "pendiente").strip().lower()
    if actual != "pendiente":
        raise ValueError("Solo se puede aceptar o rechazar postulaciones en estado pendiente.")
    updated = postulacion_colaborador_repo.update_estado(db, postulacion_id, nuevo_estado)
    if updated is None:
        raise ValueError("Postulación no encontrada.")
    logger.info("Postulación id=%s estado -> %s", postulacion_id, nuevo_estado)
    return _fila_postulacion_a_dict(updated)
