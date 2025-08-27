from fastapi import FastAPI, Depends, HTTPException
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
    return crud.create_paciente(db=db, paciente=paciente), {"detail": "Paciente creado correctamente"}

@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=["Pacientes"])
def read_pacientes(db: Session = Depends(get_db)):
    return crud.get_pacientes(db), {"detail": "Pacientes obtenidos correctamente"}

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def read_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente, {"detail": "Paciente encontrado"}

@app.delete("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def delete_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.delete_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente, {"detail": "Paciente eliminado correctamente"}

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def update_paciente(paciente_id: str, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, paciente_id=paciente_id, paciente=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente, {"detail": "Paciente actualizado correctamente"}

#Creamos rutas para los medicos

@app.post("/medicos/", response_model=schemas.Medico, tags=["Médicos"])
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico.idMedico)
    if db_medico:                                                             #validacion
        raise HTTPException(status_code=400, detail="Médico ya registrado")
    return crud.create_medico(db=db, medico=medico), {"detail": "Médico creado correctamente"}

@app.get("/medicos/", response_model=list[schemas.Medico], tags=["Médicos"])
def read_medicos(db: Session = Depends(get_db)):
    return crud.get_medicos(db), {"detail": "Médicos obtenidos correctamente"}

@app.get("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def read_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico, {"detail": "Médico encontrado"}

@app.delete("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.delete_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico, {"detail": "Médico eliminado correctamente"}

@app.put("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def update_medico(medico_id: int, medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.update_medico(db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico, {"detail": "Médico actualizado correctamente"}

#creacion de rutas para las enfermeras

@app.post("/enfermeras/", response_model=schemas.Enfermera, tags=["Enfermeras"])
def create_enfermera(enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera.idEnfermera)
    if db_enfermera:                                                             #validacion
        raise HTTPException(status_code=400, detail="Enfermera ya registrada")
    return crud.create_enfermera(db=db, enfermera=enfermera), {"detail": "Enfermera creada correctamente"}

@app.get("/enfermeras/", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_enfermeras(db: Session = Depends(get_db)):
    return crud.get_enfermeras(db), {"detail": "Enfermeras obtenidas correctamente"}

@app.get("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def read_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    return db_enfermera, {"detail": "Enfermera encontrada"}

@app.delete("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def delete_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.delete_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    return db_enfermera, {"detail": "Enfermera eliminada correctamente"}

@app.put("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def update_enfermera(enfermera_id: int, enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.update_enfermera(db, enfermera_id=enfermera_id, enfermera=enfermera)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    return db_enfermera, {"detail": "Enfermera actualizada correctamente"}

#creacion de rutas para las citas