from pydantic import BaseModel
from typing import List, Optional, Dict


class ColaboradorBase(BaseModel):
    """Base schema for Colaborador - used for create/update operations"""
    display_name: str
    handle: str
    bio: Optional[str] = None
    specialty: str  # donas, galletas, bebidas
    product_count: int = 0
    sales_count: int = 0
    is_online: bool = False
    status: str = "active"  # active, inactive


class ColaboradorCreate(ColaboradorBase):
    """Schema for creating a new collaborator"""
    pass


class ColaboradorUpdate(BaseModel):
    """Schema for updating collaborator - all fields optional"""
    display_name: Optional[str] = None
    handle: Optional[str] = None
    bio: Optional[str] = None
    specialty: Optional[str] = None
    product_count: Optional[int] = None
    sales_count: Optional[int] = None
    is_online: Optional[bool] = None
    status: Optional[str] = None


class ColaboradorResponse(ColaboradorBase):
    """Schema for API responses - includes id"""
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy model conversion


class ColaboradorListResponse(BaseModel):
    """Schema for list endpoints"""
    colaboradores: List[ColaboradorResponse]
    total: int

    class Config:
        from_attributes = True
