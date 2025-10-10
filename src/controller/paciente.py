from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.jwt_handler import verify_token

from src.entities.paciente import Paciente as paciente

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

"""A partir de aqui hacemos metodos para los pacientes

Metodos para crear, leer, actualizar y eliminar pacientes"""


def create_paciente(
    db: Session, paciente: paciente, token: str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_paciente = paciente(
        idPaciente=str(paciente.idPaciente),
        nombrePaciente=paciente.nombrePaciente,
        correoPaciente=paciente.correoPaciente,
    )
    db.add(new_paciente)
    db.commit()
    db.refresh(new_paciente)
    return new_paciente


def get_paciente(db: Session, paciente_id: str, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(paciente).filter(paciente.idPaciente == paciente_id).first()


def get_pacientes(db: Session, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(paciente).all()


def update_paciente(
    db: Session,
    paciente_id: str,
    paciente: paciente,
    token: str = Depends(oauth2_scheme),
):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_paciente = db.query(paciente).filter(paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db_paciente.nombrePaciente = paciente.nombrePaciente
        db_paciente.correoPaciente = paciente.correoPaciente
        db.commit()
        db.refresh(db_paciente)
    return db_paciente


def delete_paciente(db: Session, paciente_id: str, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_paciente = db.query(paciente).filter(paciente.idPaciente == paciente_id).first()
    if db_paciente:
        db.delete(db_paciente)
        db.commit()
    return db_paciente
