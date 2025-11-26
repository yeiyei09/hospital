import pytest
from fastapi import status
from main import app
from src.auth.middleware import get_current_active_user


def test_crear_enfermera_api(auth_client):
    """Prueba POST /enfermeras/"""

    # Arrange: Datos que enviaría el Frontend (cumpliendo EnfermeraCreate)
    datos_enfermera = {
        "nombreEnfermera": "Enfermera API",
        "correoEnfermera": "api@test.cpm",
        "telefonoEnfermera": "5551111",
        "cedulaEnfermera": "20000456",
        "areaEnfermera": "Pediatria",
    }
    # Act: Hacemos el POST usando el cliente autenticado
    response = auth_client.post("/enfermeras/", json=datos_enfermera)
    # Assert
    # Verificamos que se creó 200 OK
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
    data = response.json()
    assert data["nombreEnfermera"] == "Enfermera API"
    assert "idEnfermera" in data  # Verificamos que devolvió el ID


def test_obtener_enfermeras_api(auth_client, db_session, usuario_default):
    """Prueba GET /enfermeras/"""

    # Arrange: Creamos una enfermera directamente en la DB para tener algo que leer
    from src.entities.enfermera import Enfermera

    # Necesitamos importar el usuario para el id_usuario_creacion, pero usamos el fixture
    # Sin embargo, necesitamos acceder al ID del usuario del fixture de auth.
    # Para simplificar, creamos uno rápido o confiamos en el orden.

    # NOTA: Como auth_client usa 'usuario_default', ese usuario ya existe en la DB.
    # Vamos a recuperar ese usuario para usar su ID.

    enfermera_db = Enfermera(
        nombreEnfermera="Lectura Test",
        correoEnfermera="leer@test.com",
        telefonoEnfermera="5551111",
        cedulaEnfermera="20000456",
        areaEnfermera="Pediatria",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(enfermera_db)
    db_session.commit()
    # Act
    response = auth_client.get("/enfermeras/")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    enfermera_encontrada = next(
        (p for p in data if p["nombreEnfermera"] == "Lectura Test"), None
    )
    assert enfermera_encontrada is not None
    assert enfermera_encontrada["correoEnfermera"] == "leer@test.com"
    assert enfermera_encontrada["telefonoEnfermera"] == "5551111"
    assert enfermera_encontrada["cedulaEnfermera"] == "20000456"
    assert enfermera_encontrada["areaEnfermera"] == "Pediatria"


def test_obtener_enfermeras_vacias_api(auth_client, db_session):
    """Prueba GET /enfermeras/ cuando no hay enfermeras"""

    # Act
    response = auth_client.get("/enfermeras/")
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No hay enfermeras registradas"


def test_obtener_enfermera_por_id_api(auth_client, db_session, usuario_default):
    """Prueba GET /enfermeras/{enfermera_id}"""

    # Arrange: Creamos una enfermera directamente en la DB para tener algo que leer
    from src.entities.enfermera import Enfermera

    enfermera_db = Enfermera(
        nombreEnfermera="Enfermera Buscar",
        correoEnfermera="buscar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(enfermera_db)
    db_session.commit()
    db_session.refresh(enfermera_db)
    # act
    response = auth_client.get(f"/enfermeras/{enfermera_db.idEnfermera}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombreEnfermera"] == "Enfermera Buscar"
    assert data["idEnfermera"] == str(enfermera_db.idEnfermera)
    assert data["correoEnfermera"] == "buscar@test.com"


def test_obtener_enfermera_por_id_no_existente_api(auth_client):
    """Prueba GET /enfermeras/{enfermera_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    # Act
    response = auth_client.get(f"/enfermeras/{id_random}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Enfermera no encontrada"


def test_eliminar_enfermera_api(auth_client, db_session, usuario_default):
    """Prueba DELETE /enfermeras/{enfermera_id}"""

    # Arrange: Crear una enfermera primero
    from src.entities.enfermera import Enfermera

    enfermera_db = Enfermera(
        nombreEnfermera="Enfermera Eliminar",
        correoEnfermera="eliminar@test.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(enfermera_db)
    db_session.commit()
    db_session.refresh(enfermera_db)
    id_enfermera = enfermera_db.idEnfermera  # Guardamos el ID para usarlo luego
    # Act: Hacemos el DELETE usando el cliente autenticado
    response = auth_client.delete(f"/enfermeras/{id_enfermera}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["idEnfermera"] == str(id_enfermera)
    assert response.json()["nombreEnfermera"] == "Enfermera Eliminar"
    # Verificamos que ya no existe en la DB
    enfermera_en_db = (
        db_session.query(Enfermera)
        .filter(Enfermera.idEnfermera == id_enfermera)
        .first()
    )
    assert enfermera_en_db is None


def test_eliminar_enfermera_no_existente_api(auth_client):
    """Prueba DELETE /enfermeras/{enfermera_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    # Act
    response = auth_client.delete(f"/enfermeras/{id_random}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Enfermera no encontrada"


def test_eliminar_enfermera_sin_permisos(client):
    """Prueba DELETE /enfermeras/{enfermera_id} sin autenticación"""

    import uuid

    id_random = str(uuid.uuid4())

    # Act
    response = client.delete(f"/enfermeras/{id_random}")

    # Assert
    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


def test_obtener_enfermeras_por_area_api(auth_client, db_session, usuario_default):
    """Prueba GET /enfermeras/area/{area}"""

    # Arrange: Creamos una enfermera directamente en la DB para tener algo que leer
    from src.entities.enfermera import Enfermera

    enfermera_db = Enfermera(
        nombreEnfermera="Enfermera Area",
        correoEnfermera="area@test.com",
        areaEnfermera="Cardiologia",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(enfermera_db)
    db_session.commit()
    db_session.refresh(enfermera_db)
    # act
    response = auth_client.get(f"/enfermeras/area/{enfermera_db.areaEnfermera}")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    enfermera_encontrada = next(
        (p for p in data if p["nombreEnfermera"] == "Enfermera Area"), None
    )
    assert enfermera_encontrada is not None
    assert enfermera_encontrada["correoEnfermera"] == "area@test.com"


def test_obtener_enfermeras_por_area_no_existente_api(auth_client):
    """Prueba GET /enfermeras/area/{area} con un area sin enfermeras"""
    # Act
    response = auth_client.get(f"/enfermeras/area/AreaInexistente")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No hay enfermeras registradas en esta area"


def test_actualizar_enfermera_api(auth_client, db_session, usuario_default):
    """Prueba PUT /enfermeras/{enfermera_id}"""

    # Arrange: Crear una enfermera primero
    from src.entities.enfermera import Enfermera

    enfermera_db = Enfermera(
        nombreEnfermera="Enfermera Actualizar",
        correoEnfermera="put@test.com",
        telefonoEnfermera="5552222",
        cedulaEnfermera="30000456",
        areaEnfermera="Urgencias",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(enfermera_db)
    db_session.commit()
    db_session.refresh(enfermera_db)

    datos_actualizados = {
        "nombreEnfermera": "Enfermera Actualizada",
        "correoEnfermera": "actualizado@correo.com",
        "telefonoEnfermera": "5553333",
        "cedulaEnfermera": "30000457",
        "areaEnfermera": "Cuidados Intensivos",
    }
    # Act
    response = auth_client.put(
        f"/enfermeras/{enfermera_db.idEnfermera}", json=datos_actualizados
    )
    # Assert vericacion superficial
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nombreEnfermera"] == "Enfermera Actualizada"
    assert data["correoEnfermera"] == "actualizado@correo.com"
    assert data["telefonoEnfermera"] == "5553333"
    assert data["cedulaEnfermera"] == "30000457"
    assert data["areaEnfermera"] == "Cuidados Intensivos"
    # Verificamos en la DB
    db_session.refresh(enfermera_db)
    assert enfermera_db.nombreEnfermera == "Enfermera Actualizada"
    assert enfermera_db.correoEnfermera == "actualizado@correo.com"
    assert enfermera_db.telefonoEnfermera == "5553333"
    assert enfermera_db.cedulaEnfermera == "30000457"
    assert enfermera_db.areaEnfermera == "Cuidados Intensivos"


def test_actualizar_enfermera_no_existente_api(auth_client):
    """Prueba PUT /enfermeras/{enfermera_id} con un UUID random"""
    import uuid

    id_random = str(uuid.uuid4())

    datos_actualizados = {
        "nombreEnfermera": "Enfermera Actualizada",
        "correoEnfermera": "put@test.com",
        "telefonoEnfermera": "5553333",
        "cedulaEnfermera": "30000457",
        "areaEnfermera": "Cuidados Intensivos",
    }
    # Act
    response = auth_client.put(f"/enfermeras/{id_random}", json=datos_actualizados)
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Enfermera no encontrada"
