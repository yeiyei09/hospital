from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import crud, schemas 

# Creamos el router para los pacientes
# Define un prefijo para las rutas y etiquetas para la documentación
# En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter
router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)

#Aqui empiezan las rutas para las citas

@router.post("/citas/", response_model=schemas.AgendarCita, tags=["Citas"])
def create_cita(cita: schemas.AgendarCitaCreate, db: Session = Depends(get_db)):
    paciente = crud.get_paciente(db, paciente_id=cita.idPaciente)
    medico = crud.get_medico(db, medico_id=cita.idMedico)
    if not paciente and not medico:
        raise HTTPException(status_code=400, detail="Paciente y medico no existen, intenta con un paciente y medico que ya esten registrados")
    elif not medico or not paciente:
        raise HTTPException(status_code=400, detail="Médico o paciente no existe, intenta con un médico o paciente que ya este registrado")
    cita_creada = crud.create_agendar_cita(db=db, cita=cita)    
    if cita_creada is None:                                                             #validacion
        raise HTTPException(status_code=400, detail="Error al crear la cita")
    else:
        return JSONResponse(status_code=201, content={
        "detail" : "Cita creada cerractamente",
        "Cuerpo de la respuesta": {
            "ID de la Cita": cita_creada.idCita,
            "Cedula del Paciente": cita_creada.idPaciente,
            "Cedula del Medico": cita_creada.idMedico,
            "Fecha de Agendamiento": str(cita_creada.fechaAgendamiento),
            "Fecha de Emision": str(cita_creada.fechaEmision),
            "Motivo de Consulta": cita_creada.motivoConsulta
        }
        })
     
@router.get("/citas/", response_model=list[schemas.AgendarCita], tags=["Citas"])
def read_all_citas(db: Session = Depends(get_db)):
    dbGetCitas = crud.get_agendar_citas(db)
    if not dbGetCitas:
        raise HTTPException(status_code=404, detail="No hay citas registradas")
    return dbGetCitas

@router.get("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def read_one_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = crud.get_agendar_cita(db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Cita encontrada",
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }
        })

@router.put("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def update_cita(cita_id: int, cita: schemas.AgendarCitaCreate, db: Session = Depends(get_db)):
    db_cita = crud.update_agendar_cita(db, cita_id=cita_id, cita=cita)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Cita actualizada correctamente", 
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }})
    
@router.delete("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = crud.delete_agendar_cita(db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Cita eliminada correctamente",
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }
        })