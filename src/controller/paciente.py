from sqlalchemy.orm import Session

from src.entities.paciente import Paciente as paciente

"""A partir de aqui hacemos metodos para los pacientes

Metodos para crear, leer, actualizar y eliminar pacientes"""


def create_paciente(db: Session, paciente: paciente):
    new_paciente = paciente(
        idPaciente=str(paciente.idPaciente),
        nombrePaciente=paciente.nombrePaciente,
        correoPaciente=paciente.correoPaciente,
    )
    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    return new_paciente


def get_paciente(db: Session, paciente_id: str):
    return db.query(paciente).filter(paciente.idPaciente == paciente_id).first()


def get_pacientes(db: Session):
    return db.query(paciente).all()


def update_paciente(db: Session, paciente_id: str, paciente: paciente):
    db_paciente = db.query(paciente).filter(paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db_paciente.nombrePaciente = paciente.nombrePaciente
        db_paciente.correoPaciente = paciente.correoPaciente
        db.commit()
        db.refresh(db_paciente)
    return db_paciente


def delete_paciente(db: Session, paciente_id: str):
    db_paciente = db.query(paciente).filter(paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente
