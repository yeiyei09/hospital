import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.entities.audit_mixin import AuditMixin

from database.connection import Base


class Cita(AuditMixin, Base):
    """
    Modelo de cita médica
    """

    __tablename__ = "citas"

    idCita = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    idPaciente = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.idPaciente"), index=True
    )
    idMedico = Column(UUID(as_uuid=True), ForeignKey("medicos.idMedico"), index=True)
    fechaAgendamiento = Column(Date, index=True)
    motivoConsulta = Column(String)
    fechaEmision = Column(DateTime, index=True)

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
    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
