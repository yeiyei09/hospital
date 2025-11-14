from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.medico as medico_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user, require_roles
from src.schemas.auth import UserResponse
from src.schemas.medico import MedicoCreate, MedicoResponse

"""Creamos el router para los pacientes

Define un prefijo para las rutas y etiquetas para la documentación

En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/medicos", tags=["Médicos"])

"""Creamos rutas para los medicos"""


@router.post(
    "/",
    response_model=MedicoResponse,
    tags=["Médicos"],
    dependencies=[Depends(require_roles("admin"))],
)
def create_medico(
    medico: MedicoCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Crea un nuevo medico (UUID autogenerado)"""

    # Crear paciente sin buscar por id (porque aún no existe)
    medico_creado = medico_controller.create_medico(
        db=db, medico_data=medico, user_id=current_user.id_usuario
    )
    return medico_creado


@router.get(
    "/",
    response_model=list[MedicoResponse],
    tags=["Médicos"],
    dependencies=[Depends(require_roles("admin", "medico", "enfermera"))],
)
def read_all_medicos(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    dbGetMedicos = medico_controller.get_medicos(db)
    if not dbGetMedicos:
        raise HTTPException(status_code=404, detail="No hay medicos registrados")
    return dbGetMedicos


@router.get(
    "/{medico_id}",
    response_model=MedicoResponse,
    tags=["Médicos"],
    dependencies=[Depends(require_roles("admin", "medico", "enfermera"))],
)
def read_one_medico(
    medico_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_medico = medico_controller.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico  # devuelve JSON del medico


@router.delete(
    "/{medico_id}",
    response_model=MedicoResponse,
    tags=["Médicos"],
    dependencies=[Depends(require_roles("admin"))],
)
def delete_medico(
    medico_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_medico = medico_controller.delete_medico(db, medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return db_medico


@router.put(
    "/{medico_id}",
    response_model=MedicoResponse,
    tags=["Médicos"],
    dependencies=[Depends(require_roles("admin"))],
)
def update_medico(
    medico_id: UUID,
    medico: MedicoCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """
    Actualiza la información de un medico existente por su cedula.
    """
    db_medico = medico_controller.get_medico(db, medico_id=medico_id)

    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    medico_actualizado = medico_controller.update_medico(
        db,
        medico_id=medico_id,
        medico_data=medico,
        user_id=current_user.id_usuario,
    )
    return medico_actualizado
