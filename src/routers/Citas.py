from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import src.controller.cita as cita_controller
import src.controller.medico as medico_controller
import src.controller.paciente as paciente_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.cita import CitaCreate, CitaResponse

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.post("/", response_model=CitaResponse, status_code=201)
def create_cita(
    cita: CitaCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Crea una nueva cita médica y registra la auditoría."""

    paciente = paciente_controller.get_paciente(db, paciente_id=cita.idPaciente)
    medico = medico_controller.get_medico(db, medico_id=cita.idMedico)

    if not paciente or not medico:
        raise HTTPException(status_code=400, detail="Paciente o médico no existen")

    cita_creada = cita_controller.create_cita(
        db=db, cita_data=cita, user_id=current_user.id_usuario
    )

    return cita_creada


@router.get("/", response_model=list[CitaResponse])
def read_all_citas(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Obtiene todas las citas registradas."""
    citas = cita_controller.get_citas(db)
    if not citas:
        raise HTTPException(status_code=404, detail="No hay citas registradas")
    return citas


@router.get("/{cita_id}", response_model=CitaResponse)
def read_one_cita(
    cita_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Obtiene una cita por su UUID."""
    db_cita = cita_controller.get_cita(db, cita_id=cita_id)
    if not db_cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return db_cita


@router.put("/{cita_id}", response_model=CitaResponse)
def update_cita(
    cita_id: UUID,
    cita: CitaCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Actualiza una cita existente."""
    cita_actualizada = cita_controller.update_cita(
        db=db, cita_id=cita_id, cita_data=cita, user_id=current_user.id_usuario
    )
    if not cita_actualizada:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita_actualizada


@router.delete("/{cita_id}", response_model=CitaResponse)
def delete_cita(
    cita_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Elimina una cita existente."""
    cita_eliminada = cita_controller.delete_cita(db, cita_id=cita_id)
    if not cita_eliminada:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita_eliminada
