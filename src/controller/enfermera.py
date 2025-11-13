from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.jwt_handler import verify_token
from uuid import UUID
from src.entities.enfermera import Enfermera
from src.schemas.enfermera import EnfermeraCreate
from datetime import datetime, date


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

"""A partir de aqui hacemos metodos para las enfermeras

Metodos para crear, leer, actualizar y eliminar enfermeras"""


def create_enfermera(
    db: Session, enfermera_data: EnfermeraCreate, user_id: UUID = None
):
    """Crea una nueva enfermera con UUID autogenerado."""
    new_enfermera = Enfermera(
        nombreEnfermera=enfermera_data.nombreEnfermera,
        correoEnfermera=enfermera_data.correoEnfermera,
        telefonoEnfermera=enfermera_data.telefonoEnfermera,
        cedulaEnfermera=enfermera_data.cedulaEnfermera,
        areaEnfermera=enfermera_data.areaEnfermera,
        id_usuario_creacion=user_id,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(new_enfermera)
    db.commit()
    db.refresh(new_enfermera)
    return new_enfermera


def get_enfermera(db: Session, enfermera_cedula: str):
    """Obtiene una enfermera por su cedula."""
    return (
        db.query(Enfermera)
        .filter(Enfermera.cedulaEnfermera == enfermera_cedula)
        .first()
    )


def get_enfermeras(db: Session):
    """Obtiene todas las enfermeras registradas."""
    return db.query(Enfermera).all()


def get_enfermeras_por_area(db: Session, area: str):
    """Obtiene todas las enfermeras por area."""
    return db.query(Enfermera).filter(Enfermera.areaEnfermera == area).all()


def update_enfermera(
    db: Session,
    enfermera_cedula: str,
    enfermera_data: EnfermeraCreate,
    user_id: UUID,
):
    """Actualiza una enfermera existente."""

    db_enfermera = (
        db.query(Enfermera)
        .filter(Enfermera.cedulaEnfermera == enfermera_cedula)
        .first()
    )
    if not db_enfermera:
        return None

    db_enfermera.nombreEnfermera = enfermera_data.nombreEnfermera
    db_enfermera.areaEnfermera = enfermera_data.areaEnfermera
    db_enfermera.correoEnfermera = enfermera_data.correoEnfermera
    db_enfermera.telefonoEnfermera = enfermera_data.telefonoEnfermera
    db_enfermera.cedulaEnfermera = enfermera_data.cedulaEnfermera
    db_enfermera.id_usuario_actualizacion = user_id
    db_enfermera.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_enfermera)
    return db_enfermera


def delete_enfermera(db: Session, enfermera_cedula: str):
    db_enfermera = (
        db.query(Enfermera)
        .filter(Enfermera.cedulaEnfermera == enfermera_cedula)
        .first()
    )
    if db_enfermera:
        db.delete(db_enfermera)
        db.commit()
    return db_enfermera
