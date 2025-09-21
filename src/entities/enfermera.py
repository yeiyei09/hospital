import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Enfermera(Base):
    """
    Modelo de enfermera
    """

    __tablename__ = "enfermeras"
    idEnfermera = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombreEnfermera = Column(String, index=True)
    area = Column(String, index=True)
    correoEnfermera = Column(String, index=True)

    # Relaciones
    diagnosticos = relationship("Diagnostico", back_populates="enfermera")
