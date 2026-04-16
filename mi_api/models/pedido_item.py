from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class PedidoItem(Base):
    __tablename__ = "pedido_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    producto_nombre = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto")