import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.entities.audit_mixin import AuditMixin

from database.connection import Base


class Enfermera(AuditMixin, Base):
    """
    Modelo de enfermera con campos de auditoría heredados.
    """

    __tablename__ = "enfermeras"

    idEnfermera = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombreEnfermera = Column(String, index=True)
    correoEnfermera = Column(String, nullable=True)
    telefonoEnfermera = Column(String, nullable=True)
    cedulaEnfermera = Column(String, nullable=True, index=True)
    areaEnfermera = Column(String, index=True)

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
    diagnosticos = relationship("Diagnostico", back_populates="enfermera")
