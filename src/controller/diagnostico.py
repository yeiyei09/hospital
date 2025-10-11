from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.auth.jwt_handler import verify_token
from src.entities.diagnostico import Diagnostico as diagnostico

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_diagnostico(
    db: Session, diagnostico: diagnostico, token: str = Depends(oauth2_scheme)
):
    tocken_data = verify_token(token)
    if tocken_data["rol"] not in ["admin", "medico"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    new_diagnostico = diagnostico(
        idCita=diagnostico.idCita,
        idMedico=str(diagnostico.idMedico),
        idPaciente=str(diagnostico.idPaciente),
        idEnfermera=str(diagnostico.idEnfermera),
        descripcionDiagnostico=diagnostico.descripcionDiagnostico,
    )
    db.add(new_diagnostico)
    db.commit()
    db.refresh(new_diagnostico)
    return new_diagnostico


def get_diagnostico(
    db: Session, diagnostico_id: int, token: str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "medico", "enfermera"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return (
        db.query(diagnostico)
        .filter(diagnostico.idDiagnostico == diagnostico_id)
        .first()
    )


def get_diagnosticos(db: Session, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(diagnostico).all()


def delete_diagnostico(
    db: Session, diagnostico_id: int, token: str = Depends(oauth2_scheme)
):
    token_data = verify_token(token)
    if token_data["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_diagnostico = (
        db.query(diagnostico)
        .filter(diagnostico.idDiagnostico == diagnostico_id)
        .first()
    )
    if db_diagnostico:
        db.delete(db_diagnostico)
        db.commit()
    return db_diagnostico
