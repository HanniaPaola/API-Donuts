# schemas/usuario_comprador.py
from pydantic import BaseModel, Field
from typing import Optional

class UsuarioCompradorCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único del comprador")
    contrasena: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "juan_perez",
                "contrasena": "password123"
            }
        }

class UsuarioCompradorLogin(BaseModel):
    email: Optional[str] = Field(None, description="Email del comprador")
    nombre: Optional[str] = Field(None, description="Nombre del comprador")
    contrasena: str = Field(..., description="Contraseña")
    
    @property
    def username(self) -> Optional[str]:
        """Devuelve el nombre o email como identificador"""
        return self.nombre or self.email
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "comprador",
                "contrasena": "123456"
            }
        }

class UsuarioCompradorResponse(BaseModel):
    id_comprador: int
    nombre: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_comprador": 1,
                "nombre": "juan_perez"
            }
        }