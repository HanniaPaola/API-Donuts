# schemas/carrito.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductoEnCarritoResponse(BaseModel):
    id_producto: int
    nombre: str
    precio: float
    cantidad: int
    precio_unitario: float
    
    class Config:
        from_attributes = True

class CarritoResponse(BaseModel):
    id_carrito: int
    id_comprador: int
    subtotal: float
    cantidad_items: int
    productos: List[ProductoEnCarritoResponse] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_carrito": 1,
                "id_comprador": 1,
                "subtotal": 10.00,
                "cantidad_items": 2,
                "productos": [
                    {
                        "id_producto": 1,
                        "nombre": "Donut de Chocolate",
                        "precio": 2.50,
                        "cantidad": 2,
                        "precio_unitario": 2.50
                    }
                ]
            }
        }

class AgregarAlCarritoRequest(BaseModel):
    id_producto: int = Field(..., gt=0, description="ID del producto a agregar")
    cantidad: int = Field(default=1, gt=0, description="Cantidad a agregar (mínimo 1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_producto": 1,
                "cantidad": 2
            }
        }