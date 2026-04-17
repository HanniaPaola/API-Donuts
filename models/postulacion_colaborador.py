from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class PostulacionColaborador(Base):

    __tablename__ = "postulaciones_colaborador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_comprador = Column(
        Integer,
        ForeignKey("usuario_comprador.id_comprador"),
        nullable=True,
        index=True,
    )
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    telefono = Column(String(40), nullable=False)
    specialty = Column(String(50), nullable=False)
    mensaje = Column(Text, nullable=True)
    estado = Column(String(32), nullable=False, default="pendiente")
    creado_en = Column(DateTime, server_default=func.now(), nullable=False)
