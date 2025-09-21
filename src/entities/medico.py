import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


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
