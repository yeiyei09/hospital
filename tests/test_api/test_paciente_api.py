import pytest
from fastapi import status
from main import app
from src.auth.middleware import get_current_active_user


# 1. FIXTURE DE AUTORIZACIÓN


# 2. LOS TESTS


def test_crear_paciente_api(auth_client):
    """Prueba POST /pacientes/"""

    # Arrange: Datos que enviaría el Frontend (cumpliendo PacienteCreate)
    datos_paciente = {
        "nombrePaciente": "Paciente API",
        "correoPaciente": "api@test.com",
        "telefonoPaciente": "555-0000",
        "cedulaPaciente": "ABC-123",
        "direccionPaciente": "Av. Siempre Viva 742",
        "fechaNacimiento": "1990-01-01",
    }

    # Act: Hacemos el POST usando el cliente autenticado
    response = auth_client.post("/pacientes/", json=datos_paciente)

    # Assert
    # Verificamos que se creó (200 OK según tu router, aunque lo ideal sería 201)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

    data = response.json()
    assert data["nombrePaciente"] == "Paciente API"
    assert "idPaciente" in data  # Verificamos que devolvió el ID


def test_obtener_pacientes_api(auth_client, db_session, usuario_default):
    """Prueba GET /pacientes/"""

    # Arrange: Creamos un paciente directamente en la DB para tener algo que leer
    from src.entities.paciente import Paciente

    # Necesitamos importar el usuario para el id_usuario_creacion, pero usamos el fixture
    # Sin embargo, necesitamos acceder al ID del usuario del fixture de auth.
    # Para simplificar, creamos uno rápido o confiamos en el orden.

    # NOTA: Como auth_client usa 'usuario_default', ese usuario ya existe en la DB.
    # Vamos a recuperar ese usuario para usar su ID.

    paciente_db = Paciente(
        nombrePaciente="Lectura Test",
        correoPaciente="leer@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente_db)
    db_session.commit()

    # Act
    response = auth_client.get("/pacientes/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    paciente_encontrado = next(
        (p for p in data if p["nombrePaciente"] == "Lectura Test"), None
    )
    assert paciente_encontrado is not None


def test_obtener_todos_pacientes_vacio(auth_client, db_session):
    """Prueba GET /pacientes/ cuando NO hay datos"""
    # No hacemos Arrange (la base de datos está vacía por defecto)

    # Act
    response = auth_client.get("/pacientes/")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "No hay pacientes registrados"


def test_obtener_paciente_por_id_no_existente(auth_client):
    """Prueba GET /pacientes/{id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    response = auth_client.get(f"/pacientes/{id_random}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Paciente no encontrado"


def test_obtener_un_paciente_exitoso(auth_client, db_session, usuario_default):
    """Prueba GET /pacientes/{id} cuando SI existe"""
    # Arrange
    from src.entities.paciente import Paciente

    paciente = Paciente(
        nombrePaciente="Paciente Buscar",
        correoPaciente="buscar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)

    # Act
    # IMPORTANTE: Convertimos el UUID a string para la URL
    response = auth_client.get(f"/pacientes/{paciente.idPaciente}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["nombrePaciente"] == "Paciente Buscar"
    assert data["idPaciente"] == str(paciente.idPaciente)


def test_eliminar_paciente_sin_permisos(client):
    """
    Prueba que un usuario NO autenticado (client normal) falle al intentar borrar.
    Aquí NO usamos auth_client, usamos client "a secas".
    """
    import uuid

    id_random = str(uuid.uuid4())

    response = client.delete(f"/pacientes/{id_random}")

    # Debería dar 401 Unauthorized o 403 Forbidden
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


def test_eliminar_paciente_exitoso(auth_client, db_session, usuario_default):
    """Prueba DELETE /pacientes/{id}"""
    # Arrange
    from src.entities.paciente import Paciente

    paciente = Paciente(
        nombrePaciente="Paciente Borrar",
        correoPaciente="borrar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    id_paciente = paciente.idPaciente  # Guardamos ID antes de borrar

    # Act
    response = auth_client.delete(f"/pacientes/{id_paciente}")

    # Assert API
    assert response.status_code == 200
    assert response.json()["nombrePaciente"] == "Paciente Borrar"

    # Assert DB (Verificar que ya no existe)
    paciente_en_db = (
        db_session.query(Paciente).filter(Paciente.idPaciente == id_paciente).first()
    )
    assert paciente_en_db is None


def test_eliminar_paciente_no_existente(auth_client):
    """Prueba DELETE /pacientes/{id} con ID random"""
    import uuid

    id_random = str(uuid.uuid4())

    response = auth_client.delete(f"/pacientes/{id_random}")

    assert response.status_code == 404


def test_actualizar_paciente_exitoso(auth_client, db_session, usuario_default):
    """Prueba PUT /pacientes/{id}"""
    # Arrange: Crear paciente original
    from src.entities.paciente import Paciente

    paciente = Paciente(
        nombrePaciente="Juan Original",
        correoPaciente="juan@original.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)

    # Datos nuevos
    datos_actualizados = {
        "nombrePaciente": "Juan Editado",
        "correoPaciente": "juan@editado.com",
        "telefonoPaciente": "999-999",
        # Asegúrate de enviar los campos obligatorios que pida tu esquema PacienteCreate
    }

    # Act
    response = auth_client.put(
        f"/pacientes/{paciente.idPaciente}", json=datos_actualizados
    )

    # Assert API
    assert response.status_code == 200
    data = response.json()
    assert data["nombrePaciente"] == "Juan Editado"

    # Assert DB (Verificar que realmente cambió en la base de datos)
    db_session.refresh(paciente)
    assert paciente.nombrePaciente == "Juan Editado"
    assert paciente.correoPaciente == "juan@editado.com"


def test_actualizar_paciente_no_existente(auth_client):
    """Prueba PUT /pacientes/{id} con ID random"""
    import uuid

    id_random = str(uuid.uuid4())

    datos = {"nombrePaciente": "Fantasma", "correoPaciente": "nada@nada.com"}
    response = auth_client.put(f"/pacientes/{id_random}", json=datos)

    assert response.status_code == 404
