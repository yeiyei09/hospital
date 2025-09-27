import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from database.connection import Base


class Usuario(Base):
    """
    Modelo de usuario para autenticación
    """

    __tablename__ = "usuarios"
    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre_completo = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    rol = Column(String, default="usuario", nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    # Campos de auditoría
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True, nullable=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True, nullable=True
    )
    fecha_creacion = Column(DateTime, default=datetime.utcnow, index=True)
    fecha_actualizacion = Column(DateTime, index=True, nullable=True)
