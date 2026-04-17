# schemas/pedido.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PedidoCreate(BaseModel):
    metodo_pago: str = Field(..., description="Método de pago (transferencia, tarjeta, efectivo, etc)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "metodo_pago": "tarjeta"
            }
        }

class PedidoResponse(BaseModel):
    id_pedido: int
    fecha: datetime
    precio_total: float
    metodo_pago: str
    id_comprador: int
    id_producto: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_pedido": 1,
                "fecha": "2026-04-14T10:30:00",
                "precio_total": 10.00,
                "metodo_pago": "tarjeta",
                "id_comprador": 1,
                "id_producto": 1
            }
        }