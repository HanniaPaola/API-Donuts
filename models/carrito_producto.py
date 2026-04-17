from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class CarritoProducto(Base):
    __tablename__ = "carrito_producto"

    id_carrito_producto = Column(Integer, primary_key=True, autoincrement=True)
    carrito_id = Column("id_carrito", Integer, ForeignKey("carrito.id_carrito"), nullable=False)
    producto_id = Column("id_producto", Integer, ForeignKey("producto.id_producto"), nullable=False)
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(Float, nullable=False)

    carrito = relationship("Carrito", back_populates="productos")
    producto = relationship("Producto", back_populates="carrito_productos")
