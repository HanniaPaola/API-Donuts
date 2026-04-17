"""Persistencia de mensajes del chat colaboración (histórico vía REST; tiempo real vía WebSocket)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.chat_mensaje import ChatMensaje
from repositories import chat_mensaje_repo


def _participants_from_room(room: str) -> tuple[str, str]:
    if not room.startswith("chat:"):
        raise ValueError("Sala inválida")
    rest = room[5:]
    parts = rest.split(":")
    if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
        raise ValueError("Sala inválida")
    return parts[0].strip(), parts[1].strip()


def actor_allowed_in_room(room: str, actor_nombre: str) -> bool:
    try:
        a, b = _participants_from_room(room)
    except ValueError:
        return False
    actor = actor_nombre.strip().lower()
    return actor in (a.lower(), b.lower())


def list_mensajes(db: Session, room: str, actor_nombre: str) -> list[dict]:
    if not actor_allowed_in_room(room, actor_nombre):
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
    if not actor_allowed_in_room(room, actor_nombre):
        raise PermissionError("No tienes acceso a esta conversación")
    row = chat_mensaje_repo.create(db, room, actor_nombre, texto.strip(), ts_ms)
    return {
        "sender_id": row.sender_id,
        "texto": row.texto,
        "timestamp": int(row.ts_ms),
    }
