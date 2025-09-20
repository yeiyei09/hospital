from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import crud, schemas

# Creamos el router para los pacientes
# Define un prefijo para las rutas y etiquetas para la documentación
# En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter
router = APIRouter(
    prefix="/enfermeras",
    tags=["Enfermeras"]
)

#creacion de rutas para las enfermeras

@router.post("/enfermeras/", response_model=schemas.Enfermera, tags=["Enfermeras"])
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
    
@router.get("/enfermeras/", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_all_enfermeras(db: Session = Depends(get_db)):
    dbGetEnfermeras = crud.get_enfermeras(db)
    if not dbGetEnfermeras:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas")
    return dbGetEnfermeras

@router.get("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
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
    
@router.get("/enfermeras/area/{area}", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_enfermeras_por_area(area: str, db: Session = Depends(get_db)):
    db_enfermeras_area = crud.get_enfermeras_por_area(db, area=area)
    if not db_enfermeras_area:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas en esta area")
    return db_enfermeras_area

@router.delete("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
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

@router.put("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
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