from sqlalchemy.orm import Session

from src.entities.enfermera import Enfermera as enfermera


def create_enfermera(db: Session, enfermera: enfermera):
    new_enfermera = enfermera(
        idEnfermera=str(enfermera.idEnfermera),
        nombreEnfermera=enfermera.nombreEnfermera,
        area=enfermera.area,
        correoEnfermera=enfermera.correoEnfermera,
    )
    db.add(new_enfermera)
    db.commit()
    db.refresh(new_enfermera)
    return new_enfermera


def get_enfermera(db: Session, enfermera_id: str):
    return db.query(enfermera).filter(enfermera.idEnfermera == enfermera_id).first()


def get_enfermeras(db: Session):
    return db.query(enfermera).all()


def get_enfermeras_por_area(db: Session, area: str):
    return db.query(enfermera).filter(enfermera.area == area).all()


def update_enfermera(db: Session, enfermera_id: str, enfermera: enfermera):
    db_enfermera = (
        db.query(enfermera).filter(enfermera.idEnfermera == enfermera_id).first()
    )
    if db_enfermera:
        db_enfermera.nombreEnfermera = enfermera.nombreEnfermera
        db_enfermera.area = enfermera.area
        db_enfermera.correoEnfermera = enfermera.correoEnfermera
        db.commit()
        db.refresh(db_enfermera)
    return db_enfermera


def delete_enfermera(db: Session, enfermera_id: str):
    db_enfermera = (
        db.query(enfermera).filter(enfermera.idEnfermera == enfermera_id).first()
    )
    if db_enfermera:
        db.delete(db_enfermera)
        db.commit()
    return db_enfermera
