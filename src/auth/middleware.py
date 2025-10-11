"""
Authentication middleware for protecting endpoints.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.connection import get_db
from src.auth.jwt_handler import verify_token
from src.controller.auth_controller import get_user_by_id
from src.schemas.auth import UserResponse

# OAuth2 scheme para extraer el token del header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserResponse:
    """
    Dependency para obtener el usuario actual desde el token JWT.

    Args:
        token: Token JWT
        db: Sesión de base de datos

    Returns:
        UserResponse: Usuario actual

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token_data = verify_token(token)
    user = get_user_by_id(db, token_data["user_id"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse(
        id_usuario=user.id_usuario,
        username=user.username,
        email=user.email,
        nombre_completo=user.nombre_completo,
        rol=user.rol,
        fecha_creacion=user.fecha_creacion,
        fecha_actualizacion=user.fecha_actualizacion,
        activo=user.activo,
    )


def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """
    Dependency para obtener el usuario actual activo.

    Args:
        current_user: Usuario actual

    Returns:
        UserResponse: Usuario actual activo
    """
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )
    return current_user


def require_role(required_role: str):
    """
    Factory function para crear un dependency que requiere un rol específico.

    Args:
        required_role: Rol requerido

    Returns:
        Dependency function
    """

    def role_checker(
        current_user: UserResponse = Depends(get_current_active_user),
    ) -> UserResponse:
        if current_user.rol != required_role and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol '{required_role}' o 'admin'",
            )
        return current_user

    return role_checker


# Dependencies predefinidos para roles comunes
require_admin = require_role("admin")
require_medico = require_role("medico")
require_enfermera = require_role("enfermera")
