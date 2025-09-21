from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from entities.medico import Medico as medico_entity
import controller.medico as medico_controller

"""Creamos el router para los pacientes

Define un prefijo para las rutas y etiquetas para la documentación

En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/medicos", tags=["Médicos"])

"""Creamos rutas para los medicos"""


@router.post("/medicos/", response_model=medico_entity, tags=["Médicos"])
def create_medico(medico: medico_entity, db: Session = Depends(get_db)):
    db_medico = medico_controller.get_medico(db, medico_id=medico.idMedico)
    if db_medico:
        raise HTTPException(status_code=400, detail="Médico ya registrado")
    else:
        medico_creado = medico_controller.create_medico(db=db, medico=medico)
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Medico creado cerractamente",
                "Cuerpo de la respuesta": {
                    "Cedula del Medico": medico.idMedico,
                    "Nombre del Medico": medico.nombreMedico,
                    "Correo del Medico": medico.correoMedico,
                },
            },
        )


@router.get("/medicos/", response_model=list[medico_entity], tags=["Médicos"])
def read_all_medicos(db: Session = Depends(get_db)):
    dbGetMedicos = medico_controller.get_medicos(db)
    if not dbGetMedicos:
        raise HTTPException(status_code=404, detail="No hay medicos registrados")
    return dbGetMedicos


@router.get("/medicos/{medico_id}", response_model=medico_entity, tags=["Médicos"])
def read_one_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = medico_controller.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Médico encontrado",
                "data": {
                    "cedula medico": db_medico.idMedico,
                    "especializacion": db_medico.especializacion,
                    "nombre del medico": db_medico.nombreMedico,
                    "correo del medico": db_medico.correoMedico,
                },
            },
        )


@router.delete("/medicos/{medico_id}", response_model=medico_entity, tags=["Médicos"])
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = medico_controller.delete_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Médico eliminado correctamente",
                "data": {
                    "Cedula del Medico": db_medico.idMedico,
                    "Nombre del Medico": db_medico.nombreMedico,
                    "Correo del Medico": db_medico.correoMedico,
                },
            },
        )


@router.put("/medicos/{medico_id}", response_model=medico_entity, tags=["Médicos"])
def update_medico(medico_id: int, medico: medico_entity, db: Session = Depends(get_db)):
    db_medico = medico_controller.update_medico(db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Médico actualizado correctamente",
                "data": {
                    "Cedula del Medico": medico.idMedico,
                    "Nombre del Medico": medico.nombreMedico,
                    "Correo del Medico": medico.correoMedico,
                },
            },
        )
