"""
JWT authentication utilities.

Módulo de utilidades para autenticación JWT.

Proporciona funciones para generar, verificar y manejar tokens de acceso
utilizados en el sistema de gestión médica. Implementa cifrado con HMAC-SHA256
y control de expiración de sesiones
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()
print(">>> SECRET_KEY CARGADA DESDE ENV:", os.getenv("SECRET_KEY"))


# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no encontrada. Asegúrate de definirla en el archivo .env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña

    Returns:
        bool: True si la contraseña es correcta
    """
    try:
        return pwd_context.verify(plain_password[:72], hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de la contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password[:72])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT de acceso.

    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración personalizado

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifica y decodifica un token JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        dict: Datos decodificados del token

    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    print("🔐 Token recibido:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Token decodificado correctamente:", payload)
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        rol: str = payload.get("rol")

        if username is None or user_id is None:
            raise JWTError("Datos inválidos en el token")

        return {"username": username, "user_id": user_id, "rol": rol}
    except JWTError as e:
        print("❌ Error al verificar token:", e)
        raise HTTPException(status_code=401, detail=f"Token inválido o expirado: {e}")
    
    
