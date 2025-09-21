import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.connection import Base


class Medico(Base):
    """
    Modelo de médico
    """

    __tablename__ = "medicos"
    idMedico = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    especializacion = Column(String, index=True)
    nombreMedico = Column(String, index=True)
    correoMedico = Column(String, index=True)

    # Relaciones
    citas = relationship("Cita", back_populates="medico")
    diagnosticos = relationship("Diagnostico", back_populates="medico")

    # Campos de auditoría
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    fecha_creacion = Column(DateTime, index=True)
    fecha_actualizacion = Column(DateTime, index=True)
