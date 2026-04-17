from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class ColaboradorBase(BaseModel):
    """Base schema for Colaborador - used for create/update operations"""

    email: str
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

    email: Optional[str] = None
    display_name: Optional[str] = None
    handle: Optional[str] = None
    bio: Optional[str] = None
    specialty: Optional[str] = None
    product_count: Optional[int] = None
    sales_count: Optional[int] = None
    is_online: Optional[bool] = None
    status: Optional[str] = None


class ColaboradorResponse(ColaboradorBase):
    """Schema for API responses - includes id (entero, legado interno)"""

    id: int

    class Config:
        from_attributes = True


class CollaboratorPublic(BaseModel):
    """Formato alineado con el frontend DoniDeli (camelCase, id string)."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: str
    displayName: str
    handle: str
    bio: Optional[str] = None
    specialty: str
    productCount: int
    salesCount: int
    isOnline: bool
    status: str


class ColaboradorListResponse(BaseModel):
    """Schema for list endpoints"""

    colaboradores: List[ColaboradorResponse]
    total: int

    class Config:
        from_attributes = True
