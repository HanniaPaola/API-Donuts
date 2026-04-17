from typing import List, Optional

from sqlalchemy.orm import Session

from models.postulacion_colaborador import PostulacionColaborador


def create(
    db: Session,
    *,
    nombre_completo: str,
    email: str,
    telefono: str,
    specialty: str,
    mensaje: Optional[str],
    id_comprador: Optional[int] = None,
) -> PostulacionColaborador:
    row = PostulacionColaborador(
        id_comprador=id_comprador,
        nombre_completo=nombre_completo,
        email=email.strip().lower(),
        telefono=telefono.strip(),
        specialty=specialty.strip().lower(),
        mensaje=(mensaje.strip() if mensaje else None) or None,
        estado="pendiente",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_all_ordered(db: Session) -> List[PostulacionColaborador]:
    return (
        db.query(PostulacionColaborador)
        .order_by(PostulacionColaborador.creado_en.desc())
        .all()
    )


def get_latest_by_comprador_id(db: Session, id_comprador: int) -> Optional[PostulacionColaborador]:
    return (
        db.query(PostulacionColaborador)
        .filter(PostulacionColaborador.id_comprador == id_comprador)
        .order_by(PostulacionColaborador.creado_en.desc())
        .first()
    )


def get_latest_by_email(db: Session, email_normalized: str) -> Optional[PostulacionColaborador]:
    em = email_normalized.strip().lower()
    return (
        db.query(PostulacionColaborador)
        .filter(PostulacionColaborador.email == em)
        .order_by(PostulacionColaborador.creado_en.desc())
        .first()
    )


def get_by_id(db: Session, postulacion_id: int) -> Optional[PostulacionColaborador]:
    return (
        db.query(PostulacionColaborador)
        .filter(PostulacionColaborador.id == postulacion_id)
        .first()
    )


def update_estado(
    db: Session,
    postulacion_id: int,
    nuevo_estado: str,
) -> Optional[PostulacionColaborador]:
    row = get_by_id(db, postulacion_id)
    if row is None:
        return None
    row.estado = nuevo_estado
    db.commit()
    db.refresh(row)
    return row
