import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.entities.audit_mixin import AuditMixin

from database.connection import Base


class Paciente(AuditMixin, Base):
    """
    Modelo de paciente con campos de auditoría heredados.
    """

    __tablename__ = "pacientes"

    idPaciente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombrePaciente = Column(String, index=True)
    correoPaciente = Column(String, index=True)
    telefonoPaciente = Column(String, nullable=True)
    cedulaPaciente = Column(String, nullable=True, index=True)
    direccionPaciente = Column(String, nullable=True)
    fechaNacimiento = Column(Date, nullable=True)
    # Campos de auditoría
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    fecha_creacion = Column(DateTime, index=True)
    fecha_actualizacion = Column(DateTime, index=True)

    # Relaciones
    citas = relationship("Cita", back_populates="paciente")
    diagnosticos = relationship("Diagnostico", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")
