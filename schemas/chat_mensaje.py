from pydantic import BaseModel, Field


class ChatMensajeCreate(BaseModel):
    room: str = Field(..., min_length=8, max_length=255)
    texto: str = Field(..., min_length=1, max_length=8000)
    timestamp: int = Field(..., description="Unix epoch en milisegundos")


class ChatMensajeItem(BaseModel):
    sender_id: str
    texto: str
    timestamp: int


class ChatMensajeListResponse(BaseModel):
    mensajes: list[ChatMensajeItem]
