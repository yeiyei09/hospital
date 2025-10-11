"""
Pydantic schemas for Cita entity.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CitaBase(BaseModel):
    """Base schema for Cita with common fields."""

    idPaciente: UUID
    idMedico: UUID
    fechaAgendamiento: date
    motivoConsulta: str
    fechaEmision: datetime


class CitaCreate(CitaBase):
    """Schema for creating a new Cita."""

    pass


class CitaResponse(CitaBase):
    """Schema for Cita response."""

    idCita: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
