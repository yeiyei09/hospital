"""
Authentication router for login and registration.
"""

from datetime import datetime
from uuid import UUID
from typing import List
from src.auth.middleware import require_roles
from src.auth.email_handler import send_reset_email
from datetime import timedelta
from database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.jwt_handler import create_access_token, verify_token, verify_reset_token
from sqlalchemy.orm import Session
from src.auth.middleware import get_current_user
from fastapi import BackgroundTasks
from src.controller.auth_controller import get_user_by_email
from src.schemas.auth import (
    PasswordResetVerifyRequest,
    PasswordResetRequest,
    UserUpdate,
)
from src.controller.auth_controller import (
    authenticate_user,
    create_user,
    create_user_token,
    verify_reset_email,
    reset_user_password,
    get_user_by_id,
    update_user,
    delete_user,
)
from src.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserResponse,
    PasswordResetVerifyRequest,
    PasswordResetRequest,
)
from src.entities.usuario import Usuario
from src.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserResponse

# OAuth2 scheme para extraer el token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse, tags=["Autenticación"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.

    Args:
        user: Datos del usuario a registrar
        db: Sesión de base de datos

    Returns:
        UserResponse: Usuario registrado

    Raises:
        HTTPException: Si el usuario ya existe
    """
    try:
        db_user = create_user(db, user)
        return UserResponse(
            id_usuario=db_user.id_usuario,
            username=db_user.username,
            email=db_user.email,
            nombre_completo=db_user.nombre_completo,
            rol=db_user.rol,
            fecha_creacion=db_user.fecha_creacion,
            fecha_actualizacion=db_user.fecha_actualizacion,
            activo=db_user.activo,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse, tags=["Autenticación"])
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Autentica un usuario y genera un token JWT.

    Args:
        form_data: Credenciales de login (OAuth2PasswordRequestForm)
        db: Sesión de base de datos

    Returns:
        LoginResponse: Token JWT y datos del usuario

    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_token(user)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id_usuario=user.id_usuario,
            username=user.username,
            email=user.email,
            nombre_completo=user.nombre_completo,
            rol=user.rol,
            fecha_creacion=user.fecha_creacion,
            fecha_actualizacion=user.fecha_actualizacion,
            activo=user.activo,
        ),
    )


@router.post("/login-json", response_model=LoginResponse, tags=["Autenticación"])
def login_user_json(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica un usuario y genera un token JWT (usando JSON).

    Args:
        login_data: Credenciales de login
        db: Sesión de base de datos

    Returns:
        LoginResponse: Token JWT y datos del usuario

    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_user_token(user)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id_usuario=user.id_usuario,
            username=user.username,
            email=user.email,
            nombre_completo=user.nombre_completo,
            rol=user.rol,
            fecha_creacion=user.fecha_creacion,
            fecha_actualizacion=user.fecha_actualizacion,
            activo=user.activo,
        ),
    )


@router.get("/me", response_model=UserResponse, tags=["Autenticación"])
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    Obtiene la información del usuario actual.

    Args:
        current_user: Usuario actual autenticado

    Returns:
        UserResponse: Datos del usuario actual
    """
    return current_user


@router.get(
    "/usuarios",
    response_model=List[UserResponse],
    dependencies=[Depends(require_roles("admin"))],
)
def list_users(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios existentes."""
    return db.query(Usuario).all()


@router.post("/verify-reset-email", tags=["Autenticación"])
def verify_reset_email_route(
    request: PasswordResetVerifyRequest, db: Session = Depends(get_db)
):
    """
    Verifica si el correo pertenece a un usuario con rol 'paciente'.
    """
    try:
        user = verify_reset_email(db, request.email)
        return {
            "message": "Correo válido. Puede proceder con el restablecimiento de contraseña.",
            "email": user.email,
            "rol": user.rol,
        }
    except ValueError as e:
        detail = str(e)
        if "paciente" in detail.lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.post("/reset-password", tags=["Autenticación"])
def reset_password_route(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Restablece la contraseña del usuario verificado (rol paciente).
    """
    try:
        reset_user_password(db, request.email, request.new_password)
        return {"message": "Contraseña actualizada exitosamente."}
    except ValueError as e:
        detail = str(e)
        if "paciente" in detail.lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.post("/request-password-reset", tags=["Autenticación"])
async def request_password_reset(
    request: PasswordResetVerifyRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Envía un correo de recuperación de contraseña al usuario si es 'paciente'.
    """
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Correo no válido.")
    if user.rol.lower() != "paciente":
        raise HTTPException(
            status_code=403, detail="Correo no válido, comuníquese con TI."
        )

    # Crea token único (15 minutos de duración)
    token = create_access_token(
        data={"sub": user.username, "email": user.email, "type": "reset"},
        expires_delta=timedelta(minutes=15),
    )

    # Enviar email en segundo plano
    background_tasks.add_task(send_reset_email, user.email, token)

    return {
        "message": "Correo de restablecimiento enviado. Verifique su bandeja de entrada."
    }


@router.post("/confirm-password-reset", tags=["Autenticación"])
def confirm_password_reset(
    request: PasswordResetRequest, db: Session = Depends(get_db)
):
    payload = verify_reset_token(request.token)
    email = payload.get("email")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    from src.auth.jwt_handler import get_password_hash

    user.password_hash = get_password_hash(request.new_password)
    db.commit()
    db.refresh(user)
    return {"message": "Contraseña actualizada correctamente"}


@router.put(
    "/usuarios/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_roles("admin"))],
)
def update_user(
    user_id: UUID,
    updated_user: UserUpdate,  # ✅ nota este cambio
    db: Session = Depends(get_db),
):
    """
    Actualiza un usuario existente (sin requerir password).
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = updated_user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete(
    "/usuarios/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_roles("admin"))],
)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Elimina completamente un usuario (solo admin).
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_user)
    db.commit()
    return db_user
