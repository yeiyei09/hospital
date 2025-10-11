"""
Pydantic schemas for Diagnostico entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DiagnosticoBase(BaseModel):
    """Base schema for Diagnostico with common fields."""

    idCita: UUID
    idPaciente: UUID
    idMedico: UUID
    idEnfermera: UUID
    diagnostico: str
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None


class DiagnosticoCreate(DiagnosticoBase):
    """Schema for creating a new Diagnostico."""

    pass


class DiagnosticoResponse(DiagnosticoBase):
    """Schema for Diagnostico response."""

    idDiagnostico: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
