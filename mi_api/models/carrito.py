from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Carrito(Base):
    __tablename__ = "carrito"
    
    id_carrito = Column(Integer, primary_key=True, autoincrement=True)
    subtotal = Column(Float, default=0.0)
    cantidad_items = Column(Integer, default=0)
    id_comprador = Column(Integer, ForeignKey("usuario_comprador.id_comprador"), nullable=False, unique=True)
    
    comprador = relationship("UsuarioComprador", back_populates="carrito")
    productos = relationship("CarritoProducto", back_populates="carrito", cascade="all, delete-orphan")