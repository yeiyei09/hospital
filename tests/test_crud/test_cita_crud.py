import pytest
from datetime import date, datetime
from src.schemas.cita import CitaCreate
import src.controller.cita as cita_controller


# --- FIXTURES DE APOYO ---
@pytest.fixture
def paciente_para_crud(db_session, usuario_default):
    from src.entities.paciente import Paciente

    paciente = Paciente(
        nombrePaciente="Paciente CRUD",
        correoPaciente="crud@paciente.com",
        telefonoPaciente="123",
        cedulaPaciente="ABC",
        direccionPaciente="Direccion CRUD",
        fechaNacimiento=date(2000, 1, 1),
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente


@pytest.fixture
def medico_para_crud(db_session, usuario_default):
    from src.entities.medico import Medico

    medico = Medico(
        nombreMedico="Medico CRUD",
        correoMedico="crud@medico.com",
        telefonoMedico="456",
        cedulaMedico="DEF",
        especializacion="General",
        numeroColegiatura="789",
        id_usuario_creacion=usuario_default.id_usuario,
    )
    db_session.add(medico)
    db_session.commit()
    db_session.refresh(medico)
    return medico


# --- TESTS DEL CONTROLADOR ---


def test_crear_cita_controller(
    db_session, paciente_para_crud, medico_para_crud, usuario_default
):
    """Prueba cita_controller.create_cita"""

    # Arrange: Datos Pydantic
    datos_cita = CitaCreate(
        idPaciente=paciente_para_crud.idPaciente,
        idMedico=medico_para_crud.idMedico,
        fechaAgendamiento=date(2024, 1, 1),
        motivoConsulta="Consulta CRUD",
        fechaEmision=datetime.now(),
        id_usuario_creacion=usuario_default.id_usuario,
    )

    # Act
    nueva_cita = cita_controller.create_cita(
        db=db_session, cita_data=datos_cita, user_id=usuario_default.id_usuario
    )

    # Assert
    assert nueva_cita.idCita is not None
    assert nueva_cita.motivoConsulta == "Consulta CRUD"
    assert nueva_cita.idPaciente == paciente_para_crud.idPaciente
    # Auditoría
    assert nueva_cita.id_usuario_creacion == usuario_default.id_usuario
    assert nueva_cita.fecha_creacion is not None


def test_leer_cita_controller(
    db_session, paciente_para_crud, medico_para_crud, usuario_default
):
    """Prueba cita_controller.get_cita"""
    # Arrange
    datos = CitaCreate(
        idPaciente=paciente_para_crud.idPaciente,
        idMedico=medico_para_crud.idMedico,
        fechaAgendamiento=date(2024, 2, 2),
        motivoConsulta="Leer CRUD",
        fechaEmision=datetime.now(),
    )
    creada = cita_controller.create_cita(db_session, datos, usuario_default.id_usuario)

    # Act
    leida = cita_controller.get_cita(db_session, creada.idCita)

    # Assert
    assert leida is not None
    assert leida.motivoConsulta == "Leer CRUD"


def test_actualizar_cita_controller(
    db_session, paciente_para_crud, medico_para_crud, usuario_default
):
    """Prueba cita_controller.update_cita"""
    # 1. Arrange: Crear cita original
    datos_orig = CitaCreate(
        idPaciente=paciente_para_crud.idPaciente,
        idMedico=medico_para_crud.idMedico,
        fechaAgendamiento=date(2024, 3, 3),
        motivoConsulta="Dolor Original",
        fechaEmision=datetime.now(),
    )
    cita = cita_controller.create_cita(
        db_session, datos_orig, usuario_default.id_usuario
    )

    # Preparamos los Nuevos datos
    datos_nuevos = CitaCreate(
        idPaciente=paciente_para_crud.idPaciente,
        idMedico=medico_para_crud.idMedico,
        fechaAgendamiento=date(2024, 12, 12),
        motivoConsulta="Dolor Actualizado",
        fechaEmision=datetime.now(),
    )

    # 2. Act: Llamamos al update
    actualizada = cita_controller.update_cita(
        db=db_session,
        cita_id=cita.idCita,
        cita_data=datos_nuevos,
        user_id=usuario_default.id_usuario,
    )

    # 3. Assert: Verificamos los cambios
    # Verificamos que el objeto devuelto no sea None
    assert actualizada is not None

    # Verificamos que los datos de negocio cambiaron
    assert actualizada.motivoConsulta == "Dolor Actualizado"
    assert actualizada.fechaAgendamiento == date(2024, 12, 12)

    # Verificamos la auditoría
    assert actualizada.id_usuario_actualizacion == usuario_default.id_usuario
    assert actualizada.fecha_actualizacion is not None


def test_eliminar_cita_controller(
    db_session, paciente_para_crud, medico_para_crud, usuario_default
):
    """Prueba cita_controller.delete_cita"""
    # Arrange
    datos = CitaCreate(
        idPaciente=paciente_para_crud.idPaciente,
        idMedico=medico_para_crud.idMedico,
        fechaAgendamiento=date(2024, 4, 4),
        motivoConsulta="Borrar",
        fechaEmision=datetime.now(),
    )
    cita = cita_controller.create_cita(db_session, datos, usuario_default.id_usuario)

    # Act
    eliminada = cita_controller.delete_cita(db_session, cita.idCita)

    # Assert
    assert eliminada is not None
    # Verificar en DB que no existe
    busqueda = cita_controller.get_cita(db_session, cita.idCita)
    assert busqueda is None
