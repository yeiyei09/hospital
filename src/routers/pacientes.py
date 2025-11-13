from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.paciente as paciente_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.paciente import PacienteCreate, PacienteResponse

"""Creamos el router para los pacientes
Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteResponse, tags=["Pacientes"])
def create_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Crea un nuevo paciente (UUID autogenerado)"""

    # Crear paciente sin buscar por id (porque aún no existe)
    paciente_creado = paciente_controller.create_paciente(
        db=db, paciente_data=paciente, user_id=current_user.id_usuario
    )

    return paciente_creado


@router.get("/", response_model=list[PacienteResponse], tags=["Pacientes"])
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


@router.get("/{paciente_cedula}", response_model=PacienteResponse, tags=["Pacientes"])
def read_one_paciente(
    paciente_cedula: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_paciente = paciente_controller.get_paciente(db, paciente_cedula=paciente_cedula)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente


@router.delete(
    "/{paciente_cedula}", response_model=PacienteResponse, tags=["Pacientes"]
)
def delete_paciente(
    paciente_cedula: str,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_paciente = paciente_controller.delete_paciente(db, paciente_cedula)
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return db_paciente


@router.put("/{paciente_id}", response_model=PacienteResponse, tags=["Pacientes"])
def update_paciente(
    paciente_cedula: str,
    paciente: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """
    Actualiza la información de un paciente existente por su UUID.
    """

    db_paciente = paciente_controller.get_paciente(db, paciente_cedula=paciente_cedula)

    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    paciente_actualizado = paciente_controller.update_paciente(
        db,
        paciente_cedula=paciente_cedula,
        paciente_data=paciente,
        user_id=current_user.id_usuario,
    )

    return paciente_actualizado
