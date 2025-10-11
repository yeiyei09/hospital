"""
Pydantic schemas for Paciente entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PacienteBase(BaseModel):
    """Base schema for Paciente with common fields."""

    idPaciente: str
    nombrePaciente: str
    correoPaciente: EmailStr
    telefonoPaciente: Optional[str] = None
    direccionPaciente: Optional[str] = None
    fechaNacimiento: Optional[datetime] = None


class PacienteCreate(PacienteBase):
    """Schema for creating a new Paciente."""

    pass


class PacienteResponse(PacienteBase):
    """Schema for Paciente response."""

    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
