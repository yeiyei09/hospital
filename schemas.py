from datetime import datetime, date
from pydantic import BaseModel

class PacienteBase(BaseModel):
    idPaciente: str
    nombrePaciente: str
    correoPaciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):

    class Config:
        from_attributes = True

class MedicoBase(BaseModel):
    idMedico: str
    especializacion: str
    nombreMedico: str
    correoMedico: str

class MedicoCreate(MedicoBase):
    pass

class Medico(MedicoBase):

    class Config:
        orm_mode = True

class EnfermeraBase(BaseModel):
    idEnfermera: str
    nombreEnfermera: str
    area: str
    correoEnfermera: str

class EnfermeraCreate(EnfermeraBase):
    pass

class Enfermera(EnfermeraBase):

    class Config:
        orm_mode = True

class AgendarCitaBase(BaseModel):
    idPaciente: str
    idMedico: int
    fechaAgendamiento: date  # Usar str para fechas en Pydantic
    motivoConsulta: str

class AgendarCitaCreate(AgendarCitaBase):
    pass

class AgendarCita(AgendarCitaBase):
    id: int
    fechaEmision: datetime  # Usar str para fechas en Pydantic

    class Config:
        orm_mode = True

class DiagnosticoBase(BaseModel):
    idCita: int
    idMedico: str
    idPaciente: str
    idEnfermera: str
    fechaEmision: date  # Usar str para fechas en Pydantic
    descripcionDiagnostico: str

class DiagnosticoCreate(DiagnosticoBase):
    pass

class Diagnostico(DiagnosticoBase):
    id: int
    fechaDiagnostico: datetime  # Usar str para fechas en Pydantic

    class Config:
        orm_mode = True

class FacturaBase(BaseModel):
    idPaciente: str
    idCita: int
    estadoFactura: str
    fechaVencimiento: date  # Usar str para fechas en Pydantic
    montoTotal: int

class FacturaCreate(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int
    fechaEmision: datetime  # Usar str para fechas en Pydantic

    class Config:
        orm_mode = True