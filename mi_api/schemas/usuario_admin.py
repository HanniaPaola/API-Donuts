# schemas/usuario_admin.py
from pydantic import BaseModel, Field
from typing import Optional

class UsuarioAdminCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre único del admin")
    contrasena: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "admin_test",
                "contrasena": "admin123"
            }
        }

class UsuarioAdminLogin(BaseModel):
    email: Optional[str] = Field(None, description="Email del admin")
    nombre: Optional[str] = Field(None, description="Nombre del admin")
    contrasena: str = Field(..., description="Contraseña")
    
    @property
    def username(self) -> Optional[str]:
        return self.nombre or self.email
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "admin_test",
                "contrasena": "admin123"
            }
        }

class UsuarioAdminResponse(BaseModel):
    id_admin: int
    nombre: str
    
    class Config:
        from_attributes = True