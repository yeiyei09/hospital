import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.connection import Base


class Diagnostico(Base):
    """
    Modelo de diagnóstico médico
    """

    __tablename__ = "diagnosticos"
    idDiagnostico = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    idCita = Column(UUID(as_uuid=True), ForeignKey("citas.idCita"), index=True)
    idMedico = Column(UUID(as_uuid=True), ForeignKey("medicos.idMedico"), index=True)
    idPaciente = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.idPaciente"), index=True
    )
    idEnfermera = Column(
        UUID(as_uuid=True), ForeignKey("enfermeras.idEnfermera"), index=True
    )
    descripcionDiagnostico = Column(String)
    fechaDiagnostico = Column(DateTime, index=True)

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
    cita = relationship("Cita", back_populates="diagnosticos")
    medico = relationship("Medico", back_populates="diagnosticos")
    paciente = relationship("Paciente", back_populates="diagnosticos")
    enfermera = relationship("Enfermera", back_populates="diagnosticos")
