from sqlalchemy.orm import Session
from models import Paciente, Medico, Enfermera, AgendarCita, Diagnostico, Factura
from schemas import PacienteCreate, MedicoCreate, EnfermeraCreate, AgendarCitaCreate, DiagnosticoCreate, FacturaCreate

def create_paciente(db: Session, paciente: PacienteCreate):
    new_paciente = Paciente(
        idPaciente=str(paciente.idPaciente),
        nombrePaciente=paciente.nombrePaciente,
        correoPaciente=paciente.correoPaciente
    )
    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    return new_paciente

def get_paciente(db: Session, paciente_id: str):
    return db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()

def get_pacientes(db: Session):
    return db.query(Paciente).all()

def update_paciente(db: Session, paciente_id: str, paciente: PacienteCreate):
    db_paciente = db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db_paciente.nombrePaciente = paciente.nombrePaciente
        db_paciente.correoPaciente = paciente.correoPaciente
        db.commit()
        db.refresh(db_paciente)
    return db_paciente

def delete_paciente(db: Session, paciente_id: str):
    db_paciente = db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente

#A partir de aqui hacemos metodos para los medicos 

def create_medico(db: Session, medico: MedicoCreate):
    new_medico = Medico(
        idMedico = str(medico.idMedico),
        especializacion=medico.especializacion,
        nombreMedico=medico.nombreMedico,
        correoMedico=medico.correoMedico
    )
    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    return new_medico

def get_medico(db: Session, medico_id: str):
    return db.query(Medico).filter(Medico.idMedico == medico_id).first()

def get_medicos(db: Session):
    return db.query(Medico).all()

def update_medico(db: Session, medico_id: str, medico: MedicoCreate):
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if db_medico:
        db_medico.especializacion = medico.especializacion
        db_medico.nombreMedico = medico.nombreMedico
        db_medico.correoMedico = medico.correoMedico
        db.commit()
        db.refresh(db_medico)
    return db_medico

def delete_medico(db: Session, medico_id: str):
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico

#A partir de aqui hacemos metodos para las enfermeras

def create_enfermera(db: Session, enfermera: EnfermeraCreate):
    new_enfermera = Enfermera(
        idEnfermera = str(enfermera.idEnfermera),
        nombreEnfermera=enfermera.nombreEnfermera,
        area = enfermera.area,
        correoEnfermera=enfermera.correoEnfermera
    )
    db.add(new_enfermera)
    db.commit()
    db.refresh(new_enfermera)
    return new_enfermera

def get_enfermera(db: Session, enfermera_id: str):
    return db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()

def get_enfermeras(db: Session):
    return db.query(Enfermera).all()

def update_enfermera(db: Session, enfermera_id: str, enfermera: EnfermeraCreate):
    db_enfermera = db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()
    if db_enfermera:
        db_enfermera.nombreEnfermera = enfermera.nombreEnfermera
        db_enfermera.area = enfermera.area
        db_enfermera.correoEnfermera = enfermera.correoEnfermera
        db.commit()
        db.refresh(db_enfermera)
    return db_enfermera

def delete_enfermera(db: Session, enfermera_id: str):
    db_enfermera = db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()
    if db_enfermera:
        db.delete(db_enfermera)
        db.commit()
    return db_enfermera

#A partir de aqui hacemos metodos para las citas

def create_agendar_cita(db: Session, cita: AgendarCitaCreate):
    new_cita = AgendarCita(
        idPaciente = str(cita.idPaciente),
        idMedico = str(cita.idMedico),
        fechaAgendamiento = cita.fechaAgendamiento,
        motivoConsulta = cita.motivoConsulta
    )
    db.add(new_cita)
    db.commit()
    db.refresh(new_cita)
    return new_cita

def get_agendar_cita(db: Session, cita_id: int):
    return db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()

def get_agendar_citas(db: Session):
    return db.query(AgendarCita).all()

def update_agendar_cita(db: Session, cita_id: int, cita: AgendarCitaCreate):
    db_cita = db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()
    if db_cita:
        db_cita.idPaciente = str(cita.idPaciente)
        db_cita.idMedico = str(cita.idMedico)
        db_cita.fechaAgendamiento = cita.fechaAgendamiento
        db_cita.motivoConsulta = cita.motivoConsulta
        db.commit()
        db.refresh(db_cita)
    return db_cita

def delete_agendar_cita(db: Session, cita_id: int):
    db_cita = db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
    return db_cita

#A partir de aqui hacemos metodos para los diagnosticos

def create_diagnostico(db: Session, diagnostico: DiagnosticoCreate):
    new_diagnostico = Diagnostico(
        idCita = diagnostico.idCita,
        idMedico = str(diagnostico.idMedico),
        idPaciente = str(diagnostico.idPaciente),
        idEnfermera = str(diagnostico.idEnfermera),
        descripcionDiagnostico = diagnostico.descripcionDiagnostico
    )
    db.add(new_diagnostico)
    db.commit()
    db.refresh(new_diagnostico)
    return new_diagnostico

def get_diagnostico(db: Session, diagnostico_id: int):
    return db.query(Diagnostico).filter(Diagnostico.idDiagnostico == diagnostico_id).first()

def get_diagnosticos(db: Session):
    return db.query(Diagnostico).all()

def delete_diagnostico(db: Session, diagnostico_id: int):
    db_diagnostico = db.query(Diagnostico).filter(Diagnostico.idDiagnostico == diagnostico_id).first()
    if db_diagnostico:
        db.delete(db_diagnostico)
        db.commit()
    return db_diagnostico

#A partir de aqui hacemos metodos para las facturas
def create_factura(db: Session, factura: FacturaCreate):
    new_factura = Factura(
        idPaciente = str(factura.idPaciente),
        idCita = factura.idCita,
        estadoFactura = factura.estadoFactura,
        fechaVencimiento = factura.fechaVencimiento,
        montoTotal = factura.montoTotal
    )
    db.add(new_factura)
    db.commit()
    db.refresh(new_factura)
    return new_factura

def get_factura(db: Session, factura_id: int):
    return db.query(Factura).filter(Factura.idFactura == factura_id).first()

def get_facturas(db: Session):
    return db.query(Factura).all()

def delete_factura(db: Session, factura_id: int):
    db_factura = db.query(Factura).filter(Factura.idFactura == factura_id).first()
    if db_factura:
        db.delete(db_factura)
        db.commit()
    return db_factura