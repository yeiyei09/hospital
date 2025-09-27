from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.controller.paciente as paciente_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.paciente import PacienteCreate, PacienteResponse

"""Creamos el router para los pacientes
Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/pacientes/", response_model=PacienteResponse, tags=["Pacientes"])
def create_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Busca en la base de datos si ya existe un paciente con la misma cédula (idPaciente)"""

    db_paciente = paciente_controller.get_paciente(db, paciente_id=paciente.idPaciente)

    """Si el paciente ya está registrado, lanza una excepción HTTP con código 400 (Bad Request)"""

    if db_paciente:

        raise HTTPException(status_code=400, detail="Paciente ya registrado")
    else:
        paciente_creado = paciente_controller.create_paciente(db=db, paciente=paciente)

        return JSONResponse(
            status_code=201,
            content={
                "detail": "Paciente creado correctamente",
                "data": {
                    "Cedula paciente": paciente.idPaciente,
                    "nombre de paciente": paciente.nombrePaciente,
                    "correo  de paciente": paciente.correoPaciente,
                },
            },
        )


@router.get("/pacientes/", response_model=list[PacienteResponse], tags=["Pacientes"])
def read_all_pacientes(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    pacientes_db = paciente_controller.get_pacientes(db)
    if not pacientes_db:
        raise HTTPException(status_code=404, detail="No hay pacientes registrados")
    return pacientes_db


"""
    Obtiene todos los pacientes registrados en la base de datos.

    Args:
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        list[schemas.Paciente]: Lista de pacientes registrados.

    Raises:
        HTTPException: Si no hay pacientes registrados, retorna un error 404 con el deta
"""


@router.get(
    "/pacientes/{paciente_id}", response_model=PacienteResponse, tags=["Pacientes"]
)
def read_one_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = paciente_controller.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Paciente encontrado",
                "data": {
                    "cedula paciente": db_paciente.idPaciente,
                    "nombre de paciente": db_paciente.nombrePaciente,
                    "correo de paciente": db_paciente.correoPaciente,
                },
            },
        )


@router.delete(
    "/pacientes/{paciente_id}", response_model=PacienteResponse, tags=["Pacientes"]
)
def delete_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = paciente_controller.delete_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Paciente eliminado correctamente",
                "data": {
                    "Cedula paciente": db_paciente.idPaciente,
                    "Nombre de paciente": db_paciente.nombrePaciente,
                    "correo de paciente": db_paciente.correoPaciente,
                },
            },
        )


@router.put(
    "/pacientes/{paciente_id}", response_model=PacienteResponse, tags=["Pacientes"]
)
def update_paciente(
    paciente_id: str, paciente: PacienteCreate, db: Session = Depends(get_db)
):
    db_paciente = paciente_controller.update_paciente(
        db, paciente_id=paciente_id, paciente=paciente
    )
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Paciente actualizado correctamente",
                "data": {
                    "Cedula paciente": paciente.idPaciente,
                    "Nombre de paciente": paciente.nombrePaciente,
                    "correo de paciente": paciente.correoPaciente,
                },
            },
        )
