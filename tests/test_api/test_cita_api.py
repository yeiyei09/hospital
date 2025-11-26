import pytest
import uuid
from datetime import date, datetime
from fastapi import status

# --- FIXTURES LOCALES PARA ESTE TEST ---


@pytest.fixture
def paciente_db(db_session, usuario_default):
    """Crea un paciente real en la DB para usarlo en las citas"""
    from src.entities.paciente import Paciente

    paciente = Paciente(
        nombrePaciente="Paciente Cita",
        correoPaciente="cita@paciente.com",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente


@pytest.fixture
def medico_db(db_session, usuario_default):
    """Crea un médico real en la DB. AJUSTA LOS CAMPOS SI ES NECESARIO"""
    from src.entities.medico import Medico

    medico = Medico(
        nombreMedico="Dr. House",
        correoMedico="house@hospital.com",
        telefonoMedico="555-DOC",
        # idEspecialidad=... (Si tienes FK a especialidad, necesitarás crearla antes)
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico)
    db_session.commit()
    db_session.refresh(medico)
    return medico


# --- TESTS DE API ---


def test_crear_cita_exitoso(auth_client, paciente_db, medico_db):
    """Prueba POST /citas/ con datos válidos"""

    # Arrange: Preparamos el JSON
    datos_cita = {
        "idPaciente": str(paciente_db.idPaciente),  # Convertimos UUID a str
        "idMedico": str(medico_db.idMedico),
        "fechaAgendamiento": date.today().isoformat(),  # "YYYY-MM-DD"
        "motivoConsulta": "Dolor de cabeza intenso",
        "fechaEmision": datetime.now().isoformat(),  # "YYYY-MM-DDTHH:MM:SS..."
    }

    # Act
    response = auth_client.post("/citas/", json=datos_cita)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["motivoConsulta"] == "Dolor de cabeza intenso"
    assert data["idPaciente"] == str(paciente_db.idPaciente)
    assert "idCita" in data


def test_crear_cita_falla_si_paciente_no_existe(auth_client, medico_db):
    """Prueba POST /citas/ debe fallar si el paciente es inventado"""

    id_falso = str(uuid.uuid4())

    datos_cita = {
        "idPaciente": id_falso,
        "idMedico": str(medico_db.idMedico),
        "fechaAgendamiento": "2023-12-31",
        "motivoConsulta": "Test Fail",
        "fechaEmision": "2023-12-01T10:00:00",
    }

    response = auth_client.post("/citas/", json=datos_cita)

    # Tu router dice: if not paciente ... raise HTTPException(status_code=400)
    assert response.status_code == 400
    assert response.json()["detail"] == "Paciente o médico no existen"


def test_obtener_todas_citas(
    auth_client, db_session, paciente_db, medico_db, usuario_default
):
    """Prueba GET /citas/"""
    # Arrange: Crear una cita manualmente en la DB
    from src.entities.cita import Cita

    cita = Cita(
        idPaciente=paciente_db.idPaciente,
        idMedico=medico_db.idMedico,
        fechaAgendamiento=date.today(),
        motivoConsulta="Chequeo General",
        fechaEmision=datetime.now(),
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(cita)
    db_session.commit()

    # Act
    response = auth_client.get("/citas/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["motivoConsulta"] == "Chequeo General"


def test_actualizar_cita(
    auth_client, db_session, paciente_db, medico_db, usuario_default
):
    """Prueba PUT /citas/{id}"""
    # Arrange: Crear cita original
    from src.entities.cita import Cita

    cita = Cita(
        idPaciente=paciente_db.idPaciente,
        idMedico=medico_db.idMedico,
        fechaAgendamiento=date.today(),
        motivoConsulta="Original",
        fechaEmision=datetime.now(),
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(cita)
    db_session.commit()
    db_session.refresh(cita)

    # Datos nuevos (cambiamos el motivo)
    datos_update = {
        "idPaciente": str(paciente_db.idPaciente),
        "idMedico": str(medico_db.idMedico),
        "fechaAgendamiento": date.today().isoformat(),
        "motivoConsulta": "Actualizado",
        "fechaEmision": datetime.now().isoformat(),
    }

    # Act
    response = auth_client.put(f"/citas/{cita.idCita}", json=datos_update)

    # Assert
    assert response.status_code == 200
    assert response.json()["motivoConsulta"] == "Actualizado"


def test_eliminar_cita(
    auth_client, db_session, paciente_db, medico_db, usuario_default
):
    """Prueba DELETE /citas/{id}"""
    # Arrange
    from src.entities.cita import Cita

    cita = Cita(
        idPaciente=paciente_db.idPaciente,
        idMedico=medico_db.idMedico,
        fechaAgendamiento=date.today(),
        motivoConsulta="Borrar me",
        fechaEmision=datetime.now(),
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(cita)
    db_session.commit()
    db_session.refresh(cita)
    id_cita = cita.idCita

    # Act
    response = auth_client.delete(f"/citas/{id_cita}")

    # Assert
    assert response.status_code == 200

    # Verificar en DB
    cita_en_db = db_session.query(Cita).filter(Cita.idCita == id_cita).first()
    assert cita_en_db is None
