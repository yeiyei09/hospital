from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from database import Base

# Definición de los modelos de la base de datos identicos a las tablas en SQL Server
class Paciente(Base):
    __tablename__ = 'pacientes'
    idPaciente = Column(String, primary_key=True, index=True)
    nombrePaciente = Column(String, index=True)
    correoPaciente = Column(String, index=True)
 
class Medico(Base):
    __tablename__ = 'medicos'
    idMedico = Column(String, primary_key=True, index=True)
    especializacion = Column(String, index=True)
    nombreMedico = Column(String, index=True)
    correoMedico = Column(String, index=True)
 
class Enfermera(Base):
    __tablename__ = 'enfermeras'
    idEnfermera = Column(String, primary_key=True, index=True)
    nombreEnfermera = Column(String, index=True)
    area = Column(String, index=True)
    correoEnfermera = Column(String, index=True)

class AgendarCita(Base):
    __tablename__ = 'agendar_cita'
    idCita = Column(Integer, primary_key=True, index=True)
    idPaciente = Column(String, ForeignKey('pacientes.idPaciente'))
    idMedico = Column(String, ForeignKey('medicos.idMedico'))
    fechaAgendamiento = Column(Date, index=True)
    fechaEmision = Column(DateTime, default=datetime.now)  # Aquí se replica GETDATE()
    motivoConsulta = Column(String, index=True)

class Diagnostico(Base):
    __tablename__ = 'diagnostico'
    idDiagnostico = Column(Integer, primary_key=True, index=True)
    idCita = Column(Integer, ForeignKey('agendar_cita.idCita'))
    idMedico = Column(String, ForeignKey('medicos.idMedico'))
    idPaciente = Column(String, ForeignKey('pacientes.idPaciente'))
    idEnfermera = Column(String, ForeignKey('enfermeras.idEnfermera'))
    fechaDiagnostico = Column(DateTime, default=datetime.now)  # Aquí se replica GETDATE()
    descripcionDiagnostico = Column(String, index=True)

class Factura(Base):
    __tablename__ = 'factura'
    idFactura = Column(Integer, primary_key=True, index=True)
    idPaciente = Column(String, ForeignKey('pacientes.idPaciente'))
    idCita = Column(Integer, ForeignKey('agendar_cita.idCita'))
    estadoFactura = Column(String, index=True)
    fechaEmision = Column(DateTime, default=datetime.now)  # Aquí se replica GETDATE()
    fechaVencimiento = Column(Date, index=True)
    montoTotal = Column(Integer, index=True)
    