from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.jwt_handler import verify_token
from src.entities.factura import Factura as factura

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

"""A partir de aqui hacemos metodos para las facturas"""


def create_factura(db: Session, factura: factura, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_factura = factura(
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


def get_factura(db: Session, factura_id: int, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] not in ["admin", "paciente"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(factura).filter(factura.idFactura == factura_id).first()


def get_facturas(db: Session, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    # Hace falta meterle mas logica, ya que debe de buscar un paciente cualquier factura pero SUYA
    if token_data["rol"] not in ["admin"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(factura).all()


def delete_factura(db: Session, factura_id: int, token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if token_data["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_factura = db.query(factura).filter(factura.idFactura == factura_id).first()
    if db_factura:
        db.delete(db_factura)
        db.commit()
    return db_factura
