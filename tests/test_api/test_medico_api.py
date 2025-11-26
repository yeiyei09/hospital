import pytest
from fastapi import status
from main import app
from src.auth.middleware import get_current_active_user


def test_crear_medico_api(auth_client):
    """Prueba POST /medicos/"""

    # Arrange: Datos que enviaría el Frontend (cumpliendo MedicoCreate)
    datos_medico = {
        "nombreMedico": "Medico API",
        "correoMedico": "api@test.com",
        "telefonoMedico": "5550000",
        "cedulaMedico": "10000456",
        "especializacion": "Cardiologia",
        "numeroColegiatura": "67890",
    }
    # Act: Hacemos el POST usando el cliente autenticado
    response = auth_client.post("/medicos/", json=datos_medico)

    # Assert
    # Verificamos que se creó 200 OK
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
    data = response.json()
    assert data["nombreMedico"] == "Medico API"
    assert "idMedico" in data  # Verificamos que devolvió el ID


def test_obtener_medicos_api(auth_client, db_session, usuario_default):
    """Prueba GET /medicos/"""

    # Arrange: Creamos un medico directamente en la DB para tener algo que leer
    from src.entities.medico import Medico

    # Necesitamos importar el usuario para el id_usuario_creacion, pero usamos el fixture
    # Sin embargo, necesitamos acceder al ID del usuario del fixture de auth.
    # Para simplificar, creamos uno rápido o confiamos en el orden.

    # NOTA: Como auth_client usa 'usuario_default', ese usuario ya existe en la DB.
    # Vamos a recuperar ese usuario para usar su ID.

    medico_db = Medico(
        nombreMedico="Lectura Test",
        correoMedico="leer@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico_db)
    db_session.commit()
    # Act
    response = auth_client.get("/medicos/")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    medico_encontrado = next(
        (p for p in data if p["nombreMedico"] == "Lectura Test"), None
    )
    assert medico_encontrado is not None
    assert medico_encontrado["correoMedico"] == "leer@test.com"


def test_obtener_medicos_vacios_api(auth_client, db_session):
    """Prueba GET /medicos/ cuando NO hay datos"""

    # Act
    response = auth_client.get("/medicos/")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No hay medicos registrados"


def test_obtener_medico_por_id_api(auth_client, db_session, usuario_default):
    """Prueba GET /medicos/{medico_id}"""

    # Arrange: Crear un medico primero
    from src.entities.medico import Medico

    medico_db = Medico(
        nombreMedico="Medico Buscar",
        correoMedico="buscar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico_db)
    db_session.commit()
    db_session.refresh(medico_db)
    # act
    response = auth_client.get(f"/medicos/{medico_db.idMedico}")
    # assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["idMedico"] == str(medico_db.idMedico)
    assert data["nombreMedico"] == "Medico Buscar"


def test_obtener_medico_por_id_no_existente_api(auth_client):
    """Prueba GET /medicos/{medico_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    response = auth_client.get(f"/medicos/{id_random}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Médico no encontrado"


def test_eliminar_medico_api(auth_client, db_session, usuario_default):
    """Prueba DELETE /medicos/{medico_id}"""

    # Arrange: Crear un medico primero
    from src.entities.medico import Medico

    medico_db = Medico(
        nombreMedico="Medico Eliminar",
        correoMedico="eliminar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico_db)
    db_session.commit()
    db_session.refresh(medico_db)
    id_medico = medico_db.idMedico  # Se guarda el id del medico creado
    # Act: Hacemos el DELETE usando el cliente autenticado
    response = auth_client.delete(f"/medicos/{id_medico}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["idMedico"] == str(id_medico)
    assert response.json()["nombreMedico"] == "Medico Eliminar"
    # Verificamos que ya no existe en la DB
    medico_en_db = db_session.query(Medico).filter(Medico.idMedico == id_medico).first()
    assert medico_en_db is None


def test_eliminar_medico_no_existente_api(auth_client):
    """Prueba DELETE /medicos/{medico_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    response = auth_client.delete(f"/medicos/{id_random}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Médico no encontrado"


def test_eliminar_medico_sin_permisos(client):
    """
    Prueba que un usuario NO autenticado (client normal) falle al intentar borrar.
    Aquí NO usamos auth_client, usamos client "a secas".
    """
    import uuid

    id_random = str(uuid.uuid4())

    response = client.delete(f"/medicos/{id_random}")

    # Debería dar 401 Unauthorized o 403 Forbidden
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


def test_actualizar_medico_api(auth_client, db_session, usuario_default):
    """Prueba PUT /medicos/{medico_id}"""

    # Arrange: Crear un medico primero
    from src.entities.medico import Medico

    medico_db = Medico(
        nombreMedico="Medico Actualizar",
        correoMedico="put@test.com",
        telefonoMedico="5558888",
        cedulaMedico="00000000",
        especializacion="Cardiologia",
        numeroColegiatura="12345",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico_db)
    db_session.commit()
    db_session.refresh(medico_db)

    datos_actualizados = {
        "nombreMedico": "Medico Actualizado API",
        "correoMedico": "medico@actualizado.com",
        "telefonoMedico": "5559999",
        "cedulaMedico": "11111111",
        "especializacion": "Neurologia",
        "numeroColegiatura": "22222",
    }

    # Act
    response = auth_client.put(
        f"/medicos/{medico_db.idMedico}", json=datos_actualizados
    )
    # Assert verificacion superficial
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombreMedico"] == "Medico Actualizado API"
    assert data["correoMedico"] == "medico@actualizado.com"
    assert data["telefonoMedico"] == "5559999"
    assert data["cedulaMedico"] == "11111111"
    assert data["especializacion"] == "Neurologia"
    assert data["numeroColegiatura"] == "22222"
    # assert verificamos en DB
    db_session.refresh(medico_db)
    assert medico_db.nombreMedico == "Medico Actualizado API"
    assert medico_db.correoMedico == "medico@actualizado.com"
    assert medico_db.telefonoMedico == "5559999"
    assert medico_db.cedulaMedico == "11111111"
    assert medico_db.especializacion == "Neurologia"
    assert medico_db.numeroColegiatura == "22222"


def test_actualizar_medico_no_existente_api(auth_client):
    """Prueba PUT /medicos/{medico_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    datos_actualizados = {
        "nombreMedico": "Medico No Existe",
        "correoMedico": "put@test.com",
        "telefonoMedico": "5558888",
        "cedulaMedico": "00000000",
        "especializacion": "Cardiologia",
        "numeroColegiatura": "12345",
    }
    response = auth_client.put(f"/medicos/{id_random}", json=datos_actualizados)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Médico no encontrado"
