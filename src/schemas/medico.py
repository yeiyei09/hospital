"""
Pydantic schemas for Medico entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class MedicoBase(BaseModel):
    """Base schema for Medico with common fields."""

    idMedico: str
    nombreMedico: str
    correoMedico: EmailStr
    telefonoMedico: Optional[str] = None
    especialidad: Optional[str] = None
    numeroColegiatura: Optional[str] = None


class MedicoCreate(MedicoBase):
    """Schema for creating a new Medico."""

    pass


class MedicoResponse(MedicoBase):
    """Schema for Medico response."""

    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
