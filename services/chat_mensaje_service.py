"""Persistencia de mensajes del chat colaboración (histórico vía REST; tiempo real vía WebSocket)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.chat_mensaje import ChatMensaje
from repositories import chat_mensaje_repo
from repositories import usuario_admin_repo
from repositories.colaborador_repo import ColaboradorRepository


def _participants_from_room(room: str) -> tuple[str, str]:
    if not room.startswith("chat:"):
        raise ValueError("Sala inválida")
    rest = room[5:]
    parts = rest.split(":")
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        raise ValueError("Sala inválida")
    return parts[0].strip(), parts[1].strip()


def _contacto_chat_peer_nombre_lower(db: Session) -> str | None:
    """Mismo criterio que GET /admins/contacto-chat (primer admin por id_admin)."""
    admins = usuario_admin_repo.get_all(db)
    if not admins:
        return None
    admins.sort(key=lambda a: a.id_admin)
    return (admins[0].nombre or "").strip().lower()


def _actor_es_admin_registrado(db: Session, actor_nombre: str) -> bool:
    n = (actor_nombre or "").strip()
    if not n:
        return False
    return usuario_admin_repo.get_by_nombre(db, n) is not None


def _actor_es_colaborador_activo_por_email(db: Session, email_lower: str) -> bool:
    c = ColaboradorRepository.get_by_email(db, email_lower)
    if not c:
        return False
    return (c.status or "active").strip().lower() == "active"


def actor_allowed_in_room(room: str, actor_nombre: str, db: Session) -> bool:
    try:
        a, b = _participants_from_room(room)
    except ValueError:
        return False
    actor = actor_nombre.strip().lower()
    a_l, b_l = a.lower(), b.lower()
    if actor in (a_l, b_l):
        return True
    peer = _contacto_chat_peer_nombre_lower(db)
    if peer and peer in (a_l, b_l) and _actor_es_admin_registrado(db, actor_nombre):
        return True
    if peer and peer in (a_l, b_l) and _actor_es_colaborador_activo_por_email(db, actor):
        return True
    return False


def list_mensajes(db: Session, room: str, actor_nombre: str) -> list[dict]:
    if not actor_allowed_in_room(room, actor_nombre, db):
        raise PermissionError("No tienes acceso a esta conversación")
    rows: list[ChatMensaje] = chat_mensaje_repo.list_by_room(db, room)
    return [
        {"sender_id": r.sender_id, "texto": r.texto, "timestamp": int(r.ts_ms)}
        for r in rows
    ]


def append_mensaje(
    db: Session,
    room: str,
    texto: str,
    ts_ms: int,
    actor_nombre: str,
) -> dict:
    if not actor_allowed_in_room(room, actor_nombre, db):
        raise PermissionError("No tienes acceso a esta conversación")
    row = chat_mensaje_repo.create(db, room, actor_nombre, texto.strip(), ts_ms)
    return {
        "sender_id": row.sender_id,
        "texto": row.texto,
        "timestamp": int(row.ts_ms),
    }
