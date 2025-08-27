from datetime import datetime, date
from pydantic import BaseModel

class PacienteBase(BaseModel):
    idPaciente: str
    nombrePaciente: str
    correoPaciente: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: str

    class Config:
        from_attributes = True

class MedicoBase(BaseModel):
    especializacion: str
    nombreMedico: str
    correoMedico: str

class MedicoCreate(MedicoBase):
    pass

class Medico(MedicoBase):
    id: int

    class Config:
        from_attributes = True

class EnfermeraBase(BaseModel):
    nombreEnfermera: str
    area: str
    correoEnfermera: str

class EnfermeraCreate(EnfermeraBase):
    pass

class Enfermera(EnfermeraBase):
    id: int

    class Config:
        from_attributes = True

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
        from_attributes = True

class DiagnosticoBase(BaseModel):
    idCita: int
    idMedico: int
    idPaciente: str
    idEnfermera: int
    fechaEmision: date  # Usar str para fechas en Pydantic
    descripcionDiagnostico: str

class DiagnosticoCreate(DiagnosticoBase):
    pass

class Diagnostico(DiagnosticoBase):
    id: int
    fechaDiagnostico: datetime  # Usar str para fechas en Pydantic

    class Config:
        from_attributes = True

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
        from_attributes = True