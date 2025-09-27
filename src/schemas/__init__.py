"""
Pydantic schemas for FastAPI response models.

This module contains Pydantic models that are used for
API request/response validation and serialization.
"""

from .cita import CitaCreate, CitaResponse
from .diagnostico import DiagnosticoCreate, DiagnosticoResponse
from .enfermera import EnfermeraCreate, EnfermeraResponse
from .factura import FacturaCreate, FacturaResponse
from .medico import MedicoCreate, MedicoResponse
from .paciente import PacienteCreate, PacienteResponse

__all__ = [
    "CitaCreate",
    "CitaResponse",
    "DiagnosticoCreate",
    "DiagnosticoResponse",
    "EnfermeraCreate",
    "EnfermeraResponse",
    "FacturaCreate",
    "FacturaResponse",
    "MedicoCreate",
    "MedicoResponse",
    "PacienteCreate",
    "PacienteResponse",
]
