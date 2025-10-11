"""
Pydantic schemas for Enfermera entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class EnfermeraBase(BaseModel):
    """Base schema for Enfermera with common fields."""

    idEnfermera: str
    nombreEnfermera: str
    correoEnfermera: EmailStr
    telefonoEnfermera: Optional[str] = None
    especialidad: Optional[str] = None
    numeroColegiatura: Optional[str] = None


class EnfermeraCreate(EnfermeraBase):
    """Schema for creating a new Enfermera."""

    pass


class EnfermeraResponse(EnfermeraBase):
    """Schema for Enfermera response."""

    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
