import controller.cita as cita_controller
import controller.diagnostico as diagnostico_controller
import controller.enfermera as enfermera_controller
import controller.paciente as paciente_controller
import controller.medico as medicos_controller
import controller.factura as factura_controller
from entities.diagnostico import Diagnostico as diagnostico_entity
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.connection import SessionLocal, get_db

# Creamos el router para los pacientes
# Define un prefijo para las rutas y etiquetas para la documentación
# En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter
router = APIRouter(prefix="/diagnosticos", tags=["Diagnosticos"])

# Aqui empiezan las rutas para los diagnosticos


@router.post("/diagnosticos/", response_model=diagnostico_entity, tags=["Diagnósticos"])
def create_diagnostico(diagnostico: diagnostico_entity, db: Session = Depends(get_db)):
    paciente = paciente_controller.get_paciente(db, paciente_id=diagnostico.idPaciente)
    medico = medicos_controller.get_medico(db, medico_id=diagnostico.idMedico)
    enfermera = enfermera_controller.get_enfermera(
        db, enfermera_id=diagnostico.idEnfermera
    )
    cita = cita_controller.get_agendar_cita(db, cita_id=diagnostico.idCita)
    if not paciente and not medico and not enfermera and not cita:
        raise HTTPException(
            status_code=400,
            detail="Paciente, medico, enfermera y cita no existen, intenta con un paciente, medico, enfermera y cita que ya esten registrados",
        )
    elif not medico or not paciente or not enfermera or not cita:
        raise HTTPException(
            status_code=400,
            detail="Médico, paciente, enfermera o cita no existe, intenta con un médico, paciente, enfermera o cita que ya este registrado",
        )
    diagnostico_creado = diagnostico_controller.create_diagnostico(
        db=db, diagnostico=diagnostico
    )
    if diagnostico_creado is None:  # validacion
        raise HTTPException(status_code=400, detail="Error al crear el diagnóstico")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Diagnóstico creado cerractamente",
                "Cuerpo de la respuesta": {
                    "ID del Diagnóstico": diagnostico.idDiagnostico,
                    "ID de la Cita": diagnostico.idCita,
                    "Cedula del Medico": diagnostico.idMedico,
                    "Cedula del Paciente": diagnostico.idPaciente,
                    "Cedula de la Enfermera": diagnostico.idEnfermera,
                    "Fecha de Diagnóstico": str(diagnostico.fechaDiagnostico),
                    "Descripción del Diagnóstico": diagnostico.descripcionDiagnostico,
                },
            },
        )


@router.get(
    "/diagnosticos/", response_model=list[diagnostico_entity], tags=["Diagnósticos"]
)
def read_all_diagnosticos(db: Session = Depends(get_db)):
    dbGetDiagnosticos = diagnostico_controller.get_diagnosticos(db)
    if not dbGetDiagnosticos:
        raise HTTPException(status_code=404, detail="No hay diagnósticos registrados")
    return dbGetDiagnosticos


@router.get(
    "/diagnosticos/{diagnostico_id}",
    response_model=diagnostico_entity,
    tags=["Diagnósticos"],
)
def read_one_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    db_diagnostico = diagnostico_controller.get_diagnostico(
        db, diagnostico_id=diagnostico_id
    )
    if db_diagnostico is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Diagnóstico encontrado",
                "data": {
                    "ID del Diagnóstico": db_diagnostico.idDiagnostico,
                    "ID de la Cita": db_diagnostico.idCita,
                    "Cedula del Medico": db_diagnostico.idMedico,
                    "Cedula del Paciente": db_diagnostico.idPaciente,
                    "Cedula de la Enfermera": db_diagnostico.idEnfermera,
                    "Fecha de Diagnóstico": str(db_diagnostico.fechaDiagnostico),
                    "Descripción del Diagnóstico": db_diagnostico.descripcionDiagnostico,
                },
            },
        )


@router.delete(
    "/diagnosticos/{diagnostico_id}",
    response_model=diagnostico_entity,
    tags=["Diagnósticos"],
)
def delete_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    db_diagnostico = diagnostico_controller.delete_diagnostico(
        db, diagnostico_id=diagnostico_id
    )
    if db_diagnostico is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Diagnóstico eliminado correctamente",
                "data": {
                    "ID del Diagnóstico": db_diagnostico.idDiagnostico,
                    "ID de la Cita": db_diagnostico.idCita,
                    "Cedula del Medico": db_diagnostico.idMedico,
                    "Cedula del Paciente": db_diagnostico.idPaciente,
                    "Cedula de la Enfermera": db_diagnostico.idEnfermera,
                    "Fecha de Diagnóstico": str(db_diagnostico.fechaDiagnostico),
                    "Descripción del Diagnóstico": db_diagnostico.descripcionDiagnostico,
                },
            },
        )
