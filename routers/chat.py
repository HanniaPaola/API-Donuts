from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from deps import require_chat_actor_nombre
from schemas.chat_mensaje import (
    ChatMensajeCreate,
    ChatMensajeItem,
    ChatMensajeListResponse,
)
from services import chat_mensaje_service

router = APIRouter(prefix="/chat", tags=["Chat colaboración"])


@router.get("/mensajes", response_model=ChatMensajeListResponse)
def listar_mensajes(
    room: str = Query(..., min_length=8, max_length=255),
    db: Session = Depends(get_db),
    actor_nombre: str = Depends(require_chat_actor_nombre),
):
    try:
        items = chat_mensaje_service.list_mensajes(db, room, actor_nombre)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    return ChatMensajeListResponse(
        mensajes=[ChatMensajeItem(**m) for m in items],
    )


@router.post("/mensajes", response_model=ChatMensajeItem, status_code=status.HTTP_201_CREATED)
def crear_mensaje(
    body: ChatMensajeCreate,
    db: Session = Depends(get_db),
    actor_nombre: str = Depends(require_chat_actor_nombre),
):
    try:
        created = chat_mensaje_service.append_mensaje(
            db,
            body.room,
            body.texto,
            body.timestamp,
            actor_nombre,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    return ChatMensajeItem(**created)
