# A partir de aqui hacemos metodos para los diagnosticos


def create_diagnostico(db: Session, diagnostico: DiagnosticoCreate):
    new_diagnostico = Diagnostico(
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


def get_diagnostico(db: Session, diagnostico_id: int):
    return (
        db.query(Diagnostico)
        .filter(Diagnostico.idDiagnostico == diagnostico_id)
        .first()
    )


def get_diagnosticos(db: Session):
    return db.query(Diagnostico).all()


def delete_diagnostico(db: Session, diagnostico_id: int):
    db_diagnostico = (
        db.query(Diagnostico)
        .filter(Diagnostico.idDiagnostico == diagnostico_id)
        .first()
    )
    if db_diagnostico:
        db.delete(db_diagnostico)
        db.commit()
    return db_diagnostico
