from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.cita import Cita
from src.schemas.cita import CitaCreate


def create_cita(db: Session, cita_data: CitaCreate, user_id: UUID):
    """Crea una nueva cita y registra auditoría."""
    new_cita = Cita(
        idPaciente=cita_data.idPaciente,
        idMedico=cita_data.idMedico,
        fechaAgendamiento=cita_data.fechaAgendamiento,
        motivoConsulta=cita_data.motivoConsulta,
        fechaEmision=cita_data.fechaEmision,
        id_usuario_creacion=user_id,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(new_cita)
    db.commit()
    db.refresh(new_cita)
    return new_cita


def get_cita(db: Session, cita_id: UUID):
    """Obtiene una cita por su UUID."""
    return db.query(Cita).filter(Cita.idCita == cita_id).first()


def get_citas(db: Session, skip: int = 0, limit: int = 10):
    print(">>> Ejecutando get_citas con skip:", skip, "limit:", limit)
    """Obtiene todas las citas registradas (paginadas)."""
    return db.query(Cita).offset(skip).limit(limit).all()


def update_cita(db: Session, cita_id: UUID, cita_data: CitaCreate, user_id: UUID):
    """Actualiza una cita existente y registra auditoría."""
    db_cita = db.query(Cita).filter(Cita.idCita == cita_id).first()
    if not db_cita:
        return None

    db_cita.idPaciente = cita_data.idPaciente
    db_cita.idMedico = cita_data.idMedico
    db_cita.fechaAgendamiento = cita_data.fechaAgendamiento
    db_cita.motivoConsulta = cita_data.motivoConsulta
    db_cita.fechaEmision = cita_data.fechaEmision
    db_cita.id_usuario_actualizacion = user_id
    db_cita.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_cita)
    return db_cita


def delete_cita(db: Session, cita_id: UUID):
    """Elimina una cita por su UUID."""
    db_cita = db.query(Cita).filter(Cita.idCita == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
    return db_cita
