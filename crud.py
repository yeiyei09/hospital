from sqlalchemy.orm import Session
from models import Paciente, Medico, Enfermera, AgendarCita, Diagnostico, Factura
from schemas import PacienteCreate, MedicoCreate, EnfermeraCreate, AgendarCitaCreate, DiagnosticoCreate, FacturaCreate

def create_paciente(db: Session, paciente: PacienteCreate):
    new_paciente = Paciente(
        idPaciente=paciente.idPaciente,
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
        especializacion=medico.especializacion,
        nombreMedico=medico.nombreMedico,
        correoMedico=medico.correoMedico
    )
    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    return new_medico

def get_medico(db: Session, medico_id: int):
    return db.query(Medico).filter(Medico.idMedico == medico_id).first()

def get_medicos(db: Session):
    return db.query(Medico).all()

def update_medico(db: Session, medico_id: int, medico: MedicoCreate):
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if db_medico:
        db_medico.especializacion = medico.especializacion
        db_medico.nombreMedico = medico.nombreMedico
        db_medico.correoMedico = medico.correoMedico
        db.commit()
        db.refresh(db_medico)
    return db_medico

def delete_medico(db: Session, medico_id: int):
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico