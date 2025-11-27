import pytest
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException
from src.auth.jwt_handler import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
)


class TestAuthSecurity:

    # --- PRUEBAS DE HASHING (Lo que pedía el README adaptado) ---

    def test_hash_password_genera_hash_diferente(self):
        """Prueba que el hash use Salt (mismo password, diferente hash)"""
        password = "MiPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Deben ser diferentes strings aunque el password sea igual
        assert hash1 != hash2
        assert hash1 != password

    def test_verify_password_correcta(self):
        """Prueba que el hash generado sea válido para el password"""
        password = "MiPassword123!"
        password_hash = get_password_hash(password)

        assert verify_password(password, password_hash) is True

    def test_verify_password_incorrecta(self):
        """Prueba que un password incorrecto falle"""
        password = "MiPassword123!"
        password_hash = get_password_hash(password)
        wrong_password = "WrongPassword123!"

        assert verify_password(wrong_password, password_hash) is False

    # --- PRUEBAS DE TOKENS (Reemplazan a las de 'fuerza de contraseña' que no tienes) ---

    def test_crear_y_verificar_token_valido(self):
        """Prueba el ciclo completo de JWT"""
        # Arrange
        data = {"sub": "usuario_test", "user_id": "123", "rol": "admin"}

        # Act
        token = create_access_token(data=data)
        decoded = verify_token(token)

        # Assert
        assert decoded["username"] == "usuario_test"
        assert decoded["user_id"] == "123"
        assert decoded["rol"] == "admin"

    def test_verificar_token_invalido(self):
        """Prueba que un token alterado falle"""
        # Creamos un token real
        data = {"sub": "hacker"}
        token_real = create_access_token(data)

        # Lo "hackeamos" alterando el string
        token_falso = token_real + "basura"

        # Debe lanzar HTTPException
        with pytest.raises(HTTPException) as excinfo:
            verify_token(token_falso)

        assert excinfo.value.status_code == 401
        assert "inválido" in excinfo.value.detail.lower()

    def test_token_expirado(self):
        """Prueba que un token vencido lance error"""
        # Creamos token que expiró hace 1 minuto
        data = {"sub": "antiguo"}
        token_vencido = create_access_token(
            data=data, expires_delta=timedelta(minutes=-1)  # Tiempo negativo
        )

        with pytest.raises(HTTPException) as excinfo:
            verify_token(token_vencido)

        assert excinfo.value.status_code == 401
        assert "expirado" in excinfo.value.detail.lower()
