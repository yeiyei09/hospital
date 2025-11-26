from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.enfermera as enfermera_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user, require_roles
from src.schemas.auth import UserResponse
from src.schemas.enfermera import EnfermeraCreate, EnfermeraResponse

"""Creamos el router para los pacientes
Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""
router = APIRouter(prefix="/enfermeras", tags=["Enfermeras"])

# creacion de rutas para las enfermeras


@router.post(
    "/",
    response_model=EnfermeraResponse,
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin"))],
)
def create_enfermera(
    enfermera: EnfermeraCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Crea una nueva enfermera (UUID autogenerado)"""

    enfermera_creada = enfermera_controller.create_enfermera(
        db=db, enfermera_data=enfermera, user_id=current_user.id_usuario
    )
    return enfermera_creada


@router.get(
    "/",
    response_model=list[EnfermeraResponse],
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin", "medico", "enfermera"))],
)
def read_all_enfermeras(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    enfermeras_db = enfermera_controller.get_enfermeras(db, skip=skip, limit=limit)
    if not enfermeras_db:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas")
    return enfermeras_db


@router.get(
    "/{enfermera_id}",
    response_model=EnfermeraResponse,
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin", "medico", "enfermera"))],
)
def read_one_enfermera(
    enfermera_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.get_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    return db_enfermera


@router.get(
    "/area/{area}",
    response_model=list[EnfermeraResponse],
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin", "medico", "enfermera"))],
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


@router.delete(
    "/{enfermera_id}",
    response_model=EnfermeraResponse,
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin"))],
)
def delete_enfermera(
    enfermera_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.delete_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    return db_enfermera


@router.put(
    "/{enfermera_id}",
    response_model=EnfermeraResponse,
    tags=["Enfermeras"],
    dependencies=[Depends(require_roles("admin"))],
)
def update_enfermera(
    enfermera_id: UUID,
    enfermera: EnfermeraCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    db_enfermera = enfermera_controller.get_enfermera(db, enfermera_id=enfermera_id)
    if not db_enfermera:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    enfermera_actualizada = enfermera_controller.update_enfermera(
        db,
        enfermera_id=enfermera_id,
        enfermera_data=enfermera,
        user_id=current_user.id_usuario,
    )
    return enfermera_actualizada
