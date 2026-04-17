from typing import List

from sqlalchemy.orm import Session

from models.chat_mensaje import ChatMensaje


def list_by_room(db: Session, room: str, limit: int = 500) -> List[ChatMensaje]:
    return (
        db.query(ChatMensaje)
        .filter(ChatMensaje.room == room)
        .order_by(ChatMensaje.id.asc())
        .limit(limit)
        .all()
    )


def create(
    db: Session,
    room: str,
    sender_id: str,
    texto: str,
    ts_ms: int,
) -> ChatMensaje:
    row = ChatMensaje(room=room, sender_id=sender_id, texto=texto, ts_ms=ts_ms)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
