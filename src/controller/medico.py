from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.jwt_handler import verify_token

from src.entities.medico import Medico as medico

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

""" A partir de aqui hacemos metodos para los medicos"""


def create_medico(db: Session, medico: medico, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_medico = medico(
        idMedico=str(medico.idMedico),
        especializacion=medico.especializacion,
        nombreMedico=medico.nombreMedico,
        correoMedico=medico.correoMedico,
    )
    db.add(new_medico)
    db.commit()
    db.refresh(new_medico)
    return new_medico


def get_medico(db: Session, medico_id: str, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(medico).filter(medico.idMedico == medico_id).first()


def get_medicos(db: Session, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(medico).all()


def update_medico(
    db: Session, medico_id: str, medico: medico, token: str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_medico = db.query(medico).filter(medico.idMedico == medico_id).first()
    if db_medico:
        db_medico.especializacion = medico.especializacion
        db_medico.nombreMedico = medico.nombreMedico
        db_medico.correoMedico = medico.correoMedico
        db.commit()
        db.refresh(db_medico)
    return db_medico


def delete_medico(db: Session, medico_id: str, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_medico = db.query(medico).filter(medico.idMedico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico
