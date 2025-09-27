"""
Authentication router for login and registration.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.connection import get_db
from src.auth.middleware import get_current_user
from src.controller.auth_controller import (
    authenticate_user,
    create_user,
    create_user_token,
)
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
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica un usuario y genera un token JWT.

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
