from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.jwt_handler import verify_token
from src.entities.cita import Cita as cita

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_agendar_cita(db: Session, cita: cita, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera", "paciente"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_cita = cita(
        idPaciente=str(cita.idPaciente),
        idMedico=str(cita.idMedico),
        fechaAgendamiento=cita.fechaAgendamiento,
        motivoConsulta=cita.motivoConsulta,
    )
    db.add(new_cita)
    db.commit()
    db.refresh(new_cita)
    return new_cita


def get_agendar_cita(db: Session, cita_id: int, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    # Hace falta meterle mas logica, ya que debe de buscar un paciente cualquier cita pero SUYA
    if token_data["rol"] not in ["admin", "medico", "enfermera", "paciente"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(cita).filter(cita.idCita == cita_id).first()


def get_agendar_citas(db: Session, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(cita).all()


def update_agendar_cita(
    db: Session, cita_id: int, cita: cita, token: str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera", "paciente"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_cita = db.query(cita).filter(cita.idCita == cita_id).first()
    if db_cita:
        db_cita.idPaciente = str(cita.idPaciente)
        db_cita.idMedico = str(cita.idMedico)
        db_cita.fechaAgendamiento = cita.fechaAgendamiento
        db_cita.motivoConsulta = cita.motivoConsulta
        db.commit()
        db.refresh(db_cita)
    return db_cita


def delete_agendar_cita(db: Session, cita_id: int, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_cita = db.query(cita).filter(cita.idCita == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
    return db_cita