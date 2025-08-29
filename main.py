from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud, schemas

Base.metadata.create_all(bind=engine)
from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para manejar pacientes, médicos y citas médicas.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pacientes",
            "description": "Operaciones relacionadas con el manejo de pacientes."
        },
        {
            "name": "Médicos",
            "description": "Gestión de información de médicos."
        },
        {
            "name": "Enfermeras",
            "description": "Gestion de información de enfermeras."
        },
        {
            "name": "Citas",
            "description": "Agendamiento y consulta de citas médicas."
        }
    ]
)

#Creamos rutas para los pacientes

def get_db():
    db = SessionLocal() #crea sesion
    try:  #entrega la sesion
        yield db
    finally: #termina la sesion
        db.close()
        
@app.post("/pacientes/", response_model=schemas.Paciente, tags=["Pacientes"])
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente.idPaciente)
    if db_paciente:                                                             #validacion
        raise HTTPException(status_code=400, detail="Paciente ya registrado")
    else: 
        paciente_creado = crud.create_paciente(db=db, paciente=paciente)

        return JSONResponse(status_code=201, content={
        "detail": "Paciente creado correctamente",
        "data": {
        "Cedula paciente": paciente_creado.idPaciente,
        "nombre de paciente": paciente_creado.nombrePaciente,
        "correo de paciente": paciente_creado.correoPaciente
                }
                                                     }
                            )



@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=["Pacientes"])
def read_all_pacientes(db: Session = Depends(get_db)):
    pacientes_db = crud.get_pacientes(db)
    return pacientes_db

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def read_one_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente encontrado",
            "data": {
                "cedula paciente": db_paciente.idPaciente,
                "nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

@app.delete("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def delete_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.delete_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente eliminado correctamente",
            "data": {
                "Cedula paciente": db_paciente.idPaciente,
                "Nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def update_paciente(paciente_id: str, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, paciente_id=paciente_id, paciente=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente actualizado correctamente",
            "data": {
                "Cedula paciente": db_paciente.idPaciente,
                "Nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

#Creamos rutas para los medicos.

@app.post("/medicos/", response_model=schemas.Medico, tags=["Médicos"])
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico.idMedico)
    if db_medico:                                                             #validacion
        raise HTTPException(status_code=400, detail="Médico ya registrado")
    else:
        medico_creado = crud.create_medico(db=db, medico=medico)
        return JSONResponse(status_code=201, content={
        "detail" : "Medico creado cerractamente",
        "Cuerpo de la respuesta": {
            "Cedula del Medico": medico_creado.idMedico,
            "Nombre del Medico": medico_creado.nombreMedico,
            "Correo del Medico": medico_creado.correoMedico,
        }
        })

@app.get("/medicos/", response_model=list[schemas.Medico], tags=["Médicos"])
def read_all_medicos(db: Session = Depends(get_db)):
    dbGetMedicos = crud.get_medicos(db)
    return dbGetMedicos

@app.get("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def read_one_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Médico encontrado",
            "data": {
                "cedula medico": db_medico.idMedico,
                "especializacion": db_medico.especializacion,
                "nombre del medico": db_medico.nombreMedico,
                "correo del medico": db_medico.correoMedico
            }
        })

@app.delete("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.delete_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Médico eliminado correctamente",
            "data": {
                "Cedula del Medico": db_medico.idMedico,
                "Nombre del Medico": db_medico.nombreMedico,
                "Correo del Medico": db_medico.correoMedico
            }
        })

@app.put("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def update_medico(medico_id: int, medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.update_medico(db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Médico actualizado correctamente", 
            "data":{
                "Cedula del Medico": db_medico.idMedico,
                "Nombre del Medico": db_medico.nombreMedico,
                "Correo del Medico": db_medico.correoMedico
            }})

#creacion de rutas para las enfermeras

@app.post("/enfermeras/", response_model=schemas.Enfermera, tags=["Enfermeras"])
def create_enfermera(enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera.idEnfermera)
    if db_enfermera:                                                             #validacion
        raise HTTPException(status_code=400, detail="Enfermera ya registrada")
    else:
        enfermera_creada = crud.create_enfermera(db=db, enfermera=enfermera)
        return JSONResponse(status_code=201, content={
        "detail" : "Enfermera creada cerractamente",
        "Cuerpo de la respuesta": {
            "Cedula de la Enfermera": enfermera_creada.idEnfermera,
            "Nombre de la Enfermera": enfermera_creada.nombreEnfermera,
            "Correo de la Enfermera": enfermera_creada.correoEnfermera,
            "Area de la Enfermera": enfermera_creada.area
        }
        })
    
@app.get("/enfermeras/", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_all_enfermeras(db: Session = Depends(get_db)):
    dbGetEnfermeras = crud.get_enfermeras(db)
    return dbGetEnfermeras

@app.get("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def read_one_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Enfermera encontrada",
            "data": {
                "cedula enfermera": db_enfermera.idEnfermera,
                "nombre de enfermera": db_enfermera.nombreEnfermera,
                "area de enfermera": db_enfermera.area,
                "correo de enfermera": db_enfermera.correoEnfermera
            }
        })

@app.delete("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def delete_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.delete_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Enfermera eliminada correctamente",
            "data": {
                "Cedula de la Enfermera": db_enfermera.idEnfermera,
                "Nombre de la Enfermera": db_enfermera.nombreEnfermera,
                "Correo de la Enfermera": db_enfermera.correoEnfermera,
                "Area de la Enfermera": db_enfermera.area
            }
        })

@app.put("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def update_enfermera(enfermera_id: int, enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.update_enfermera(db, enfermera_id=enfermera_id, enfermera=enfermera)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Enfermera actualizada correctamente", 
            "data": {
                "Cedula de la Enfermera": db_enfermera.idEnfermera,
                "Nombre de la Enfermera": db_enfermera.nombreEnfermera,
                "Correo de la Enfermera": db_enfermera.correoEnfermera,
                "Area de la Enfermera": db_enfermera.area
            }}) 

