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

from src.entities.paciente import Paciente
from src.entities.medico import Medico
from src.entities.enfermera import Enfermera


def create_user(db: Session, user: UserCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.
    validando que exista un registro previo de paciente, médico o enfermera
    si el rol lo requiere.
    """

    rol_valido = user.rol.lower()
    # Validar rol permitido
    roles_permitidos = ["admin", "paciente", "medico", "enfermera"]
    if rol_valido not in roles_permitidos:
        raise ValueError(f"Rol no válido. Debe ser uno de: {roles_permitidos}")

    # Verificar si el usuario ya existe por nombre o correo
    if get_user_by_username(db, user.username):
        raise ValueError("El nombre de usuario ya existe")
    if get_user_by_email(db, user.email):
        raise ValueError("El correo electrónico ya está registrado")

    # Validar que exista el registro base antes de crear usuario
    if rol_valido == "paciente":
        existente = (
            db.query(Paciente).filter(Paciente.correoPaciente == user.email).first()
        )
    elif rol_valido == "medico":
        existente = db.query(Medico).filter(Medico.correoMedico == user.email).first()
    elif rol_valido == "enfermera":
        existente = (
            db.query(Enfermera).filter(Enfermera.correoEnfermera == user.email).first()
        )
    else:
        existente = True  # los admins no necesitan validar identidad
    if not existente:
        raise ValueError(
            f"No existe un registro en la tabla correspondiente para el rol '{rol_valido}'. "
            f"Debes registrar primero el {rol_valido} antes de crear el usuario."
        )

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


def update_user_password(
    db: Session, user_id: UUID, new_password: str, updated_by: UUID
) -> Usuario:
    """
    Actualiza únicamente la contraseña del usuario indicado.
    """

    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")

    hashed_password = get_password_hash(new_password)

    user.password_hash = hashed_password
    user.id_usuario_actualizacion = updated_by
    user.fecha_actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user


def verify_reset_email(db: Session, email: str) -> Usuario:
    """
    Verifica si el correo pertenece a un usuario con rol 'paciente'.

    Args:
        db: Sesión de base de datos
        email: Correo electrónico a verificar

    Returns:
        Usuario válido para restablecimiento

    Raises:
        ValueError: Si el correo no existe o no es de un paciente
    """
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Correo no válido")
    if user.rol.lower() != "paciente":
        raise ValueError("Correo no válido, comuníquese con el departamento de TI")
    return user


def reset_user_password(db: Session, email: str, new_password: str) -> Usuario:
    """
    Actualiza la contraseña de un usuario que haya pasado la verificación previa.

    Args:
        db: Sesión de base de datos
        email: Correo del usuario
        new_password: Nueva contraseña

    Returns:
        Usuario actualizado

    Raises:
        ValueError: Si el correo no existe o no pertenece a un paciente
    """
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Correo no válido")
    if user.rol.lower() != "paciente":
        raise ValueError("Correo no válido, comuníquese con el departamento de TI")

    hashed = get_password_hash(new_password)
    user.password_hash = hashed
    user.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: UUID, updated_data: dict) -> Usuario:
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")

    for key, value in updated_data.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)

    user.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: UUID) -> Usuario:
    user = get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")

    db.delete(user)
    db.commit()
    return user
