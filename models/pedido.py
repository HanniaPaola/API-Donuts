# models/pedido.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Pedido(Base):
    __tablename__ = "pedido"
    
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=func.now())
    precio_total = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    id_comprador = Column(Integer, ForeignKey("usuario_comprador.id_comprador"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    
    comprador = relationship("UsuarioComprador", back_populates="pedidos")
    producto = relationship("Producto", back_populates="pedidos")
    
