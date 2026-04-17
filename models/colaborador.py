from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    handle = Column(String(50), unique=True, nullable=False)
    bio = Column(String(500), nullable=True)
    specialty = Column(String(50), nullable=False)
    product_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)
    is_online = Column(Boolean, default=False)
    status = Column(String(20), default="active")

    productos = relationship("Producto", back_populates="colaborador")
