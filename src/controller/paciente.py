from datetime import datetime, date
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.paciente import Paciente
from src.schemas.paciente import PacienteCreate

"""A partir de aqui hacemos metodos para los pacientes

Metodos para crear, leer, actualizar y eliminar pacientes"""


def create_paciente(db: Session, paciente_data: PacienteCreate):
    """Crea un nuevo paciente con UUID autogenerado."""
    new_paciente = Paciente(
        nombrePaciente=paciente_data.nombrePaciente,
        correoPaciente=paciente_data.correoPaciente,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    return new_paciente


def get_paciente(db: Session, paciente_id: UUID):
    """Obtiene un paciente por su UUID."""
    return db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()


def get_pacientes(db: Session):
    """Obtiene todos los pacientes registrados."""
    return db.query(Paciente).all()


def update_paciente(db: Session, paciente_id: UUID, paciente_data: PacienteCreate):
    """Actualiza un paciente existente."""
    db_paciente = db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()
    if not db_paciente:
        return None

    db_paciente.nombrePaciente = paciente_data.nombrePaciente
    db_paciente.correoPaciente = paciente_data.correoPaciente
    db_paciente.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_paciente)
    return db_paciente

    return db_paciente


def delete_paciente(db: Session, paciente_id: UUID):
    """Elimina un paciente por su UUID."""
    db_paciente = db.query(Paciente).filter(Paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente
