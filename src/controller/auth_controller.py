"""
Authentication controller for user management.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from src.auth.jwt_handler import create_access_token, get_password_hash, verify_password
from src.entities.usuario import Usuario
from src.schemas.auth import LoginRequest, UserCreate, UserResponse


def create_user(db: Session, user: UserCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.

    Args:
        db: Sesión de base de datos
        user: Datos del usuario a crear

    Returns:
        Usuario: Usuario creado
    """
    # Verificar si el usuario ya existe
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise ValueError("El nombre de usuario ya existe")

    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise ValueError("El correo electrónico ya está registrado")

    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        id_usuario=uuid4(),
        username=user.username,
        email=user.email,
        nombre_completo=user.nombre_completo,
        password_hash=hashed_password,
        rol=user.rol,
        activo=True,
        fecha_creacion=datetime.utcnow(),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por nombre de usuario.

    Args:
        db: Sesión de base de datos
        username: Nombre de usuario

    Returns:
        Usuario: Usuario encontrado o None
    """
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por correo electrónico.

    Args:
        db: Sesión de base de datos
        email: Correo electrónico

    Returns:
        Usuario: Usuario encontrado o None
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[Usuario]:
    """
    Obtiene un usuario por ID.

    Args:
        db: Sesión de base de datos
        user_id: ID del usuario

    Returns:
        Usuario: Usuario encontrado o None
    """
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[Usuario]:
    """
    Autentica un usuario verificando sus credenciales.

    Args:
        db: Sesión de base de datos
        username: Nombre de usuario
        password: Contraseña

    Returns:
        Usuario: Usuario autenticado o None
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.activo:
        return None
    return user


def create_user_token(user: Usuario) -> str:
    """
    Crea un token JWT para un usuario.

    Args:
        user: Usuario para el cual crear el token

    Returns:
        str: Token JWT
    """
    token_data = {
        "sub": user.username,
        "user_id": str(user.id_usuario),
        "rol": user.rol,
    }
    return create_access_token(data=token_data)
