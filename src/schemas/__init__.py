"""
Pydantic schemas for FastAPI response models.

This module contains Pydantic models that are used for
API request/response validation and serialization.
"""

from .cita import CitaCreate, CitaResponse
from .enfermera import EnfermeraCreate, EnfermeraResponse
from .medico import MedicoCreate, MedicoResponse
from .paciente import PacienteCreate, PacienteResponse

__all__ = [
    "CitaCreate",
    "CitaResponse",
    "EnfermeraCreate",
    "EnfermeraResponse",
    "MedicoCreate",
    "MedicoResponse",
    "PacienteCreate",
    "PacienteResponse",
]
