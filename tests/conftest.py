import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from src.entities.usuario import Usuario
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import String
from sqlalchemy.ext.compiler import compiles
from src.auth.middleware import get_current_active_user


@compiles(UUID, "sqlite")
def compile_uuid(type_, compiler, **kw):
    """
    Le enseña a SQLite a tratar los UUID de Postgres como Strings (VARCHAR)
    """
    return "VARCHAR(36)"


# 1. CONFIGURACIÓN DE RUTAS
# Agregamos la raíz del proyecto al path de Python para que encuentre 'src' y 'database'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. IMPORTACIONES DEL PROYECTO
from main import app
from database.connection import Base, get_db

# Importamos las entidades para asegurar que SQLAlchemy las reconozca antes de crear tablas
# Aunque connection.py ya las importa, esto asegura que estén cargadas en el contexto del test
import src.entities


# 3. CONFIGURACIÓN DE DB EN MEMORIA (SQLite)
# Usamos SQLite en memoria. Es volátil (se borra al terminar), perfecto para tests.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # StaticPool es vital para tests en memoria
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que maneja la sesión de base de datos.
    Se ejecuta POR CADA TEST (scope="function").
    1. Crea las tablas.
    2. Entrega la sesión.
    3. Al terminar el test, elimina las tablas.
    """
    # Crea las tablas definidas en Base (Paciente, Medico, etc.)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpieza total después del test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture del Cliente HTTP.
    Reemplaza (Override) la dependencia 'get_db' real por nuestra 'db_session' de prueba.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def usuario_default(db_session):
    """
    Crea un usuario en la DB y lo retorna.
    Útil para llenar los campos de auditoría (id_usuario_creacion).
    """
    usuario = Usuario(
        username="test_user",  # Obligatorio
        email="test@example.com",  # Obligatorio
        nombre_completo="Usuario Test",  # Obligatorio
        password_hash="fakehash123",  # Obligatorio
        rol="admin",  # Opcional (tiene default)
        activo=True,  # Opcional (tiene default)
        # id_usuario_creacion lo dejamos vacío (None) porque es el primer usuario
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


@pytest.fixture(scope="function")
def auth_client(client, usuario_default):
    """
    Cliente HTTP autenticado como admin para todos los tests.
    """
    app.dependency_overrides[get_current_active_user] = lambda: usuario_default
    yield client
    # Limpieza
    if get_current_active_user in app.dependency_overrides:
        del app.dependency_overrides[get_current_active_user]
