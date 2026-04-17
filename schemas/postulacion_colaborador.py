from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


SpecialtyPostulacion = Literal["donas", "galletas", "bebidas"]


class PostulacionColaboradorCreate(BaseModel):
    nombre_completo: str = Field(..., min_length=2, max_length=150)
    email: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Correo o identificador de cuenta comprador (debe coincidir con la sesión si envías token).",
    )
    telefono: str = Field(..., min_length=8, max_length=40)
    specialty: SpecialtyPostulacion
    mensaje: Optional[str] = Field(None, max_length=2000)

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str) -> str:
        return v.strip().lower()


class PostulacionColaboradorItem(BaseModel):
    id: int
    nombre_completo: str
    email: str
    telefono: str
    specialty: str
    mensaje: Optional[str] = None
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True


class PostulacionColaboradorListResponse(BaseModel):
    postulaciones: List[PostulacionColaboradorItem]
    total: int


PostulacionEstadoAdmin = Literal["aceptada", "rechazada"]


class PostulacionColaboradorEstadoUpdate(BaseModel):
    estado: PostulacionEstadoAdmin
