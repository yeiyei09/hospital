from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.jwt_handler import verify_token
from datetime import datetime, date
from uuid import UUID

from src.entities.medico import Medico
from src.schemas.medico import MedicoCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

""" A partir de aqui hacemos metodos para los medicos"""


def create_medico(db: Session, medico_data: MedicoCreate, user_id: UUID = None):
    """Crea un nuevo medico con UUID autogenerado."""
    new_medico = Medico(
        nombreMedico=medico_data.nombreMedico,
        correoMedico=medico_data.correoMedico,
        telefonoMedico=medico_data.telefonoMedico,
        cedulaMedico=medico_data.cedulaMedico,
        especializacion=medico_data.especializacion,
        numeroColegiatura=medico_data.numeroColegiatura,
        id_usuario_creacion=user_id,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    return new_medico


def get_medico(db: Session, medico_id: UUID):
    """Obtiene un paciente por su UUID."""
    return db.query(Medico).filter(Medico.idMedico == medico_id).first()


def get_medicos(db: Session, skip: int = 0, limit: int = 10):
    """Obtiene todos los médicos (con paginación)."""
    return db.query(Medico).offset(skip).limit(limit).all()


def update_medico(
    db: Session, medico_id: UUID, medico_data: MedicoCreate, user_id: UUID
):
    """Actualiza un medico existente."""
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if not db_medico:
        return None

    db_medico.nombreMedico = medico_data.nombreMedico
    db_medico.correoMedico = medico_data.correoMedico
    db_medico.especializacion = medico_data.especializacion
    db_medico.telefonoMedico = medico_data.telefonoMedico
    db_medico.cedulaMedico = medico_data.cedulaMedico
    db_medico.especializacion = medico_data.especializacion
    db_medico.numeroColegiatura = medico_data.numeroColegiatura
    db_medico.id_usuario_actualizacion = user_id
    db_medico.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_medico)
    return db_medico


def delete_medico(db: Session, medico_id: UUID):
    db_medico = db.query(Medico).filter(Medico.idMedico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico
