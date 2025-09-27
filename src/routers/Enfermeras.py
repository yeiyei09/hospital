from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.controller.enfermera as enfermera_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.enfermera import EnfermeraCreate, EnfermeraResponse

# Creamos el router para los pacientes
# Define un prefijo para las rutas y etiquetas para la documentación
# En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter
router = APIRouter(prefix="/enfermeras", tags=["Enfermeras"])

# creacion de rutas para las enfermeras


@router.post("/", response_model=EnfermeraResponse, tags=["Enfermeras"])
def create_enfermera(
    enfermera: EnfermeraCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.get_enfermera(
        db, enfermera_id=enfermera.idEnfermera
    )
    if db_enfermera:  # validacion
        raise HTTPException(status_code=400, detail="Enfermera ya registrada")
    else:
        enfermera_creada = enfermera_controller.create_enfermera(
            db=db, enfermera=enfermera
        )
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Enfermera creada cerractamente",
                "Cuerpo de la respuesta": {
                    "Cedula de la Enfermera": enfermera.idEnfermera,
                    "Nombre de la Enfermera": enfermera.nombreEnfermera,
                    "Correo de la Enfermera": enfermera.correoEnfermera,
                    "Area de la Enfermera": enfermera.area,
                },
            },
        )


@router.get("/", response_model=list[EnfermeraResponse], tags=["Enfermeras"])
def read_all_enfermeras(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    dbGetEnfermeras = enfermera_controller.get_enfermeras(db)
    if not dbGetEnfermeras:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas")
    return dbGetEnfermeras


@router.get("/{enfermera_id}", response_model=EnfermeraResponse, tags=["Enfermeras"])
def read_one_enfermera(
    enfermera_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.get_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Enfermera encontrada",
                "data": {
                    "cedula enfermera": db_enfermera.idEnfermera,
                    "nombre de enfermera": db_enfermera.nombreEnfermera,
                    "area de enfermera": db_enfermera.area,
                    "correo de enfermera": db_enfermera.correoEnfermera,
                },
            },
        )


@router.get(
    "/area/{area}",
    response_model=list[EnfermeraResponse],
    tags=["Enfermeras"],
)
def read_enfermeras_por_area(
    area: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermeras_area = enfermera_controller.get_enfermeras_por_area(db, area=area)
    if not db_enfermeras_area:
        raise HTTPException(
            status_code=404, detail="No hay enfermeras registradas en esta area"
        )
    return db_enfermeras_area


@router.delete("/{enfermera_id}", response_model=EnfermeraResponse, tags=["Enfermeras"])
def delete_enfermera(
    enfermera_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.delete_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Enfermera eliminada correctamente",
                "data": {
                    "Cedula de la Enfermera": db_enfermera.idEnfermera,
                    "Nombre de la Enfermera": db_enfermera.nombreEnfermera,
                    "Correo de la Enfermera": db_enfermera.correoEnfermera,
                    "Area de la Enfermera": db_enfermera.area,
                },
            },
        )


@router.put("/{enfermera_id}", response_model=EnfermeraResponse, tags=["Enfermeras"])
def update_enfermera(
    enfermera_id: int,
    enfermera: EnfermeraCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.update_enfermera(
        db, enfermera_id=enfermera_id, enfermera=enfermera
    )
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Enfermera actualizada correctamente",
                "data": {
                    "Cedula de la Enfermera": enfermera.idEnfermera,
                    "Nombre de la Enfermera": enfermera.nombreEnfermera,
                    "Correo de la Enfermera": enfermera.correoEnfermera,
                    "Area de la Enfermera": enfermera.area,
                },
            },
        )
