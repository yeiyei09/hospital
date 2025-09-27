from sqlalchemy.orm import Session

from src.entities.medico import Medico as medico

""" A partir de aqui hacemos metodos para los medicos"""


def create_medico(db: Session, medico: medico):
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


def get_medico(db: Session, medico_id: str):
    return db.query(medico).filter(medico.idMedico == medico_id).first()


def get_medicos(db: Session):
    return db.query(medico).all()


def update_medico(db: Session, medico_id: str, medico: medico):
    db_medico = db.query(medico).filter(medico.idMedico == medico_id).first()
    if db_medico:
        db_medico.especializacion = medico.especializacion
        db_medico.nombreMedico = medico.nombreMedico
        db_medico.correoMedico = medico.correoMedico
        db.commit()
        db.refresh(db_medico)
    return db_medico


def delete_medico(db: Session, medico_id: str):
    db_medico = db.query(medico).filter(medico.idMedico == medico_id).first()
    if db_medico:
        db.delete(db_medico)
        db.commit()
    return db_medico
