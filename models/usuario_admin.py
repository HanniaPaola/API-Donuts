# models/usuario_admin.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class UsuarioAdmin(Base):
    __tablename__ = "usuario_admin"
    
    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    
    productos = relationship("Producto", back_populates="admin")