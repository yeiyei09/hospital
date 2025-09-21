import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Paciente(Base):
    """
    Modelo de paciente
    """

    __tablename__ = "pacientes"
    idPaciente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombrePaciente = Column(String, index=True)
    correoPaciente = Column(String, index=True)

    # Relaciones
    citas = relationship("Cita", back_populates="paciente")
    diagnosticos = relationship("Diagnostico", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")
