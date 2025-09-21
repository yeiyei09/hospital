import controller.cita as cita_controller
import controller.paciente as paciente_controller
import controller.medico as medicos_controller
from entities.cita import Cita as cita_entity
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.connection import get_db

router = APIRouter(prefix="/citas", tags=["Citas"])

# Aqui empiezan las rutas para las citas


@router.post("/citas/", response_model=cita_entity tags=["Citas"])
def create_cita(
    cita: cita_entity, db: Session = Depends(get_db)
) -> JSONResponse:
    paciente = paciente_controller.get_paciente(db, paciente_id=cita.idPaciente)   
    medico = medicos_controller.get_medico(db, medico_id=cita.idMedico)
    if not paciente and not medico:
        raise HTTPException(
            status_code=400,
            detail="Paciente y medico no existen, intenta con un paciente y medico que ya esten registrados",
        )
    elif not medico or not paciente:
        raise HTTPException(
            status_code=400,
            detail="Médico o paciente no existe, intenta con un médico o paciente que ya este registrado",
        )
    cita_creada = cita_controller.create_agendar_cita(db=db, cita=cita)
    if cita_creada is None:  # validacion
        raise HTTPException(status_code=400, detail="Error al crear la cita")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Cita creada cerractamente",
                "Cuerpo de la respuesta": {
                    "ID de la Cita": cita.idCita,
                    "Cedula del Paciente": cita.idPaciente,
                    "Cedula del Medico": cita.idMedico,
                    "Fecha de Agendamiento": str(cita.fechaAgendamiento),
                    "Fecha de Emision": str(cita.fechaEmision),
                    "Motivo de Consulta": cita.motivoConsulta,
                },
            },
        )
    


@router.get("/citas/", response_model=list[cita_entity], tags=["Citas"])
def read_all_citas(db: Session = Depends(get_db)):
    dbGetCitas = cita_controller.get_agendar_citas(db)
    if not dbGetCitas:
        raise HTTPException(status_code=404, detail="No hay citas registradas")
    return dbGetCitas


@router.get("/citas/{cita_id}", response_model=cita_entity, tags=["Citas"])
def read_one_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = cita_controller.get_agendar_cita(db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cita encontrada",
                "data": {
                    "ID de la Cita": db_cita.idCita,
                    "Cedula del Paciente": db_cita.idPaciente,
                    "Cedula del Medico": db_cita.idMedico,
                    "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                    "Fecha de Emision": str(db_cita.fechaEmision),
                    "Motivo de Consulta": db_cita.motivoConsulta,
                },
            },
        )


@router.put("/citas/{cita_id}", response_model=cita_entity, tags=["Citas"])
def update_cita(
    cita_id: int, cita: cita_entity, db: Session = Depends(get_db)
):
    db_cita = cita_controller.update_agendar_cita(db, cita_id=cita_id, cita=cita)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Cita actualizada correctamente",
                "data": {
                    "ID de la Cita": cita.idCita,
                    "Cedula del Paciente": cita.idPaciente,
                    "Cedula del Medico": cita.idMedico,
                    "Fecha de Agendamiento": str(cita.fechaAgendamiento),
                    "Fecha de Emision": str(cita.fechaEmision),
                    "Motivo de Consulta": cita.motivoConsulta,
                },
            },
        )


@router.delete("/citas/{cita_id}", response_model=cita_entity, tags=["Citas"])
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = cita_controller.delete_agendar_cita(db, cita_id=cita_id) 
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cita eliminada correctamente",
                "data": {
                    "ID de la Cita": db_cita.idCita,
                    "Cedula del Paciente": db_cita.idPaciente,
                    "Cedula del Medico": db_cita.idMedico,
                    "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                    "Fecha de Emision": str(db_cita.fechaEmision),
                    "Motivo de Consulta": db_cita.motivoConsulta,
                },
            },
        )
