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
            "name": "Citas",
            "description": "Agendamiento y consulta de citas médicas."
        }
    ]
)

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