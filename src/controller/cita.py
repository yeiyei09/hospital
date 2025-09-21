from sqlalchemy.orm import Session

from entities import cita


def create_agendar_cita(db: Session, cita: cita):
    new_cita = AgendarCita(
        idPaciente=str(cita.idPaciente),
        idMedico=str(cita.idMedico),
        fechaAgendamiento=cita.fechaAgendamiento,
        motivoConsulta=cita.motivoConsulta,
    )
    db.add(new_cita)
    db.commit()
    db.refresh(new_cita)
    return new_cita


def get_agendar_cita(db: Session, cita_id: int):
    return db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()


def get_agendar_citas(db: Session):
    return db.query(AgendarCita).all()


def update_agendar_cita(db: Session, cita_id: int, cita: AgendarCitaCreate):
    db_cita = db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()
    if db_cita:
        db_cita.idPaciente = str(cita.idPaciente)
        db_cita.idMedico = str(cita.idMedico)
        db_cita.fechaAgendamiento = cita.fechaAgendamiento
        db_cita.motivoConsulta = cita.motivoConsulta
        db.commit()
        db.refresh(db_cita)
    return db_cita


def delete_agendar_cita(db: Session, cita_id: int):
    db_cita = db.query(AgendarCita).filter(AgendarCita.idCita == cita_id).first()
    if db_cita:
        db.delete(db_cita)
        db.commit()
    return db_cita
