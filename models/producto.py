# models/producto.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(100))
    stock_disponible = Column(Integer, default=0)
    id_admin = Column(Integer, ForeignKey("usuario_admin.id_admin"), nullable=False)

    admin = relationship("UsuarioAdmin", back_populates="productos")
    carrito_productos = relationship("CarritoProducto", back_populates="producto")
    pedido_items = relationship("PedidoItem", back_populates="producto")
