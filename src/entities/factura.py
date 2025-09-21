import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Factura(Base):
    """
    Modelo de factura médica
    """

    __tablename__ = "facturas"
    idFactura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    idPaciente = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.idPaciente"), index=True
    )
    idCita = Column(UUID(as_uuid=True), ForeignKey("citas.idCita"), index=True)
    estadoFactura = Column(String, index=True)
    fechaVencimiento = Column(Date, index=True)
    montoTotal = Column(Integer)
    fechaEmision = Column(DateTime, index=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="facturas")
    cita = relationship("Cita", back_populates="facturas")
