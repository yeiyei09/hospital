from sqlalchemy.orm import Session
from models import Paciente
from schemas import PacienteCreate

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

