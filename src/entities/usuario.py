import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Usuario(Base):
    """
    Modelo de usuario
    """

    __tablename__ = "usuarios"
    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    primer_nombre = Column(String, index=True, nullable=False)
    segundo_nombre = Column(String, index=True, nullable=True)
    primer_apellido = Column(String, index=True, nullable=False)
    segundo_apellido = Column(String, index=True, nullable=True)
    correo_usuario = Column(String, unique=True, index=True, nullable=False)
    contrasena_usuario = Column(String, nullable=False)

    # Campos de auditoría
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), index=True
    )
    fecha_creacion = Column(DateTime, index=True)
    fecha_actualizacion = Column(DateTime, index=True)
