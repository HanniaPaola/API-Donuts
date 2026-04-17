# models/usuario_comprador.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class UsuarioComprador(Base):
    __tablename__ = "usuario_comprador"
    
    id_comprador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    
    carrito = relationship("Carrito", back_populates="comprador", uselist=False)
    pedidos = relationship("Pedido", back_populates="comprador")