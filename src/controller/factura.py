# A partir de aqui hacemos metodos para las facturas
def create_factura(db: Session, factura: FacturaCreate):
    new_factura = Factura(
        idPaciente=str(factura.idPaciente),
        idCita=factura.idCita,
        estadoFactura=factura.estadoFactura,
        fechaVencimiento=factura.fechaVencimiento,
        montoTotal=factura.montoTotal,
    )
    db.add(new_factura)
    db.commit()
    db.refresh(new_factura)
    return new_factura


def get_factura(db: Session, factura_id: int):
    return db.query(Factura).filter(Factura.idFactura == factura_id).first()


def get_facturas(db: Session):
    return db.query(Factura).all()


def delete_factura(db: Session, factura_id: int):
    db_factura = db.query(Factura).filter(Factura.idFactura == factura_id).first()
    if db_factura:
        db.delete(db_factura)
        db.commit()
    return db_factura
