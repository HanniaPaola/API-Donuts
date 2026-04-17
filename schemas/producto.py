# schemas/producto.py
from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    categoria: Optional[str] = Field(None, max_length=100, description="Categoría del producto")
    stock_disponible: int = Field(default=0, ge=0, description="Stock disponible (no puede ser negativo)")
    id_colaborador: Optional[int] = Field(
        None,
        description="Si se indica, el producto aparece en el menú de ese colaborador",
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Donut de Chocolate",
                "precio": 2.50,
                "categoria": "Postres",
                "stock_disponible": 100
            }
        }

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150, description="Nombre del producto")
    precio: Optional[float] = Field(None, gt=0, description="Precio del producto")
    categoria: Optional[str] = Field(None, max_length=100, description="Categoría del producto")
    stock_disponible: Optional[int] = Field(None, ge=0, description="Stock disponible")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Donut Premium de Chocolate",
                "precio": 3.00,
                "stock_disponible": 150
            }
        }

class ProductoResponse(BaseModel):
    id_producto: int
    nombre: str
    precio: float
    categoria: Optional[str]
    stock_disponible: int
    id_admin: int
    id_colaborador: Optional[int] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_producto": 1,
                "nombre": "Donut de Chocolate",
                "precio": 2.50,
                "categoria": "Postres",
                "stock_disponible": 100,
                "id_admin": 1
            }
        }