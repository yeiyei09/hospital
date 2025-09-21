# A partir de aqui hacemos metodos para las enfermeras


def create_enfermera(db: Session, enfermera: EnfermeraCreate):
    new_enfermera = Enfermera(
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
    return db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()


def get_enfermeras(db: Session):
    return db.query(Enfermera).all()


def get_enfermeras_por_area(db: Session, area: str):
    return db.query(Enfermera).filter(Enfermera.area == area).all()


def update_enfermera(db: Session, enfermera_id: str, enfermera: EnfermeraCreate):
    db_enfermera = (
        db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()
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
        db.query(Enfermera).filter(Enfermera.idEnfermera == enfermera_id).first()
    )
    if db_enfermera:
        db.delete(db_enfermera)
        db.commit()
    return db_enfermera
