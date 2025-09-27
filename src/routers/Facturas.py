from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.controller.cita as cita_controller
import src.controller.factura as factura_controller
import src.controller.paciente as paciente_controller
from database.connection import get_db
from src.schemas.factura import FacturaCreate, FacturaResponse

"""Creamos el router para los pacientes

Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post("/facturas/", response_model=FacturaResponse, tags=["Facturas"])
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    paciente = paciente_controller.get_paciente(db, paciente_id=factura.idPaciente)
    cita = cita_controller.get_agendar_cita(db, cita_id=factura.idCita)
    if not paciente and not cita:
        raise HTTPException(
            status_code=400,
            detail="Paciente y cita no existen, intenta con un paciente y cita que ya esten registrados",
        )
    elif not cita or not paciente:
        raise HTTPException(
            status_code=400,
            detail="Cita o paciente no existe, intenta con una cita o paciente que ya este registrado",
        )
    factura_creada = factura_controller.create_factura(db=db, factura=factura)
    if factura_creada is None:  # validacion
        raise HTTPException(status_code=400, detail="Error al crear la factura")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Factura creada cerractamente",
                "Cuerpo de la respuesta": {
                    "ID de la Factura": factura.idFactura,
                    "Cedula del Paciente": factura.idPaciente,
                    "ID de la Cita": factura.idCita,
                    "Estado de la Factura": factura.estadoFactura,
                    "Fecha de Emision": str(factura.fechaEmision),
                    "Fecha de Vencimiento": str(factura.fechaVencimiento),
                    "Monto Total": factura.montoTotal,
                },
            },
        )


@router.get("/facturas/", response_model=list[FacturaResponse], tags=["Facturas"])
def read_all_facturas(db: Session = Depends(get_db)):
    dbGetFacturas = factura_controller.get_facturas(db)
    if not dbGetFacturas:
        raise HTTPException(status_code=404, detail="No hay facturas registradas")
    return dbGetFacturas


@router.get("/facturas/{factura_id}", response_model=FacturaResponse, tags=["Facturas"])
def read_one_factura(factura_id: int, db: Session = Depends(get_db)):
    db_factura = factura_controller.get_factura(db, factura_id=factura_id)
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Factura encontrada",
                "data": {
                    "ID de la Factura": db_factura.idFactura,
                    "Cedula del Paciente": db_factura.idPaciente,
                    "ID de la Cita": db_factura.idCita,
                    "Estado de la Factura": db_factura.estadoFactura,
                    "Fecha de Emision": str(db_factura.fechaEmision),
                    "Monto Total": db_factura.montoTotal,
                },
            },
        )


@router.delete(
    "/facturas/{factura_id}", response_model=FacturaResponse, tags=["Facturas"]
)
def delete_factura(factura_id: int, db: Session = Depends(get_db)):
    db_factura = factura_controller.delete_factura(db, factura_id=factura_id)
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Factura eliminada correctamente",
                "data": {
                    "ID de la Factura": db_factura.idFactura,
                    "Cedula del Paciente": db_factura.idPaciente,
                    "ID de la Cita": db_factura.idCita,
                    "Estado de la Factura": db_factura.estadoFactura,
                    "Fecha de Emision": str(db_factura.fechaEmision),
                    "Monto Total": db_factura.montoTotal,
                },
            },
        )
