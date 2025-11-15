"""
Pydantic schemas for authentication.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema for User with common fields."""

    username: str
    email: EmailStr
    nombre_completo: str
    rol: str = "usuario"  # usuario, admin, medico, enfermera


class UserCreate(UserBase):
    """Schema for creating a new User."""

    password: str


class UserResponse(UserBase):
    """Schema for User response."""

    id_usuario: UUID
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    activo: bool = True

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str
    password: str


class LoginResponse(BaseModel):
    """Schema for login response."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for token data."""

    username: Optional[str] = None
    user_id: Optional[UUID] = None
    rol: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    """Schema para actualizar únicamente la contraseña."""

    password: str


class PasswordResetVerifyRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str


class PasswordResetRequest(BaseModel):
    token: str
    new_password: str


class UserUpdate(BaseModel):
    """Schema para actualizar usuario (sin requerir contraseña)."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = None
    rol: Optional[str] = None
