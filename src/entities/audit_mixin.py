from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class AuditMixin:
    """Campos de auditoría comunes para todas las entidades."""

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True, nullable=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True, nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=True)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
