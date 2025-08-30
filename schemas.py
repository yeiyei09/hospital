from datetime import datetime, date
from pydantic import BaseModel

# Esta clase define los campos base que tendrá un paciente.
# Se usa como clase padre para otros esquemas relacionados con pacientes.
class PacienteBase(BaseModel):
    idPaciente: str
    nombrePaciente: str
    correoPaciente: str

# Esta clase se usa específicamente para la creación de pacientes.
# Hereda todos los campos de PacienteBase sin agregar nuevos, pero puede extenderse en el futuro.
class PacienteCreate(PacienteBase):
    pass  # No se agregan nuevos campos, pero se mantiene por claridad y estructura.

# Esta clase representa el esquema completo del paciente que se devuelve en las respuest
# También hereda de PacienteBase.
class Paciente(PacienteBase):
    # Esta configuración permite que Pydantic convierta automáticamente objetos ORM (commo los de SQLAlchemy)
    # en instancias de este esquema, lo cual es útil cuando usamos response_model en FastAPI.
    class Config:
        from_attributes = True  # Equivalente a 'orm_mode = True' en versiones anteriores

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
    idCita: int
    fechaEmision: datetime  # Usar str para fechas en Pydantic

    class Config:
        orm_mode = True

class DiagnosticoBase(BaseModel):
    idCita: int
    idMedico: str
    idPaciente: str
    idEnfermera: str
    descripcionDiagnostico: str

class DiagnosticoCreate(DiagnosticoBase):
    pass

class Diagnostico(DiagnosticoBase):
    idDiagnostico: int
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
    idFactura: int
    fechaEmision: datetime  # Usar str para fechas en Pydantic

    class Config:
        orm_mode = True

#