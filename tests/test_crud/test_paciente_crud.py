# tests/test_crud/test_paciente_crud.py
import src.controller.paciente as paciente_controller
from src.schemas.paciente import PacienteCreate
from datetime import date


def test_crear_usuario_exitoso(db_session, usuario_default):
    # 1. ARRANGE: Preparamos los datos como un objeto Pydantic (PacienteCreate)
    # El controlador espera un objeto con atributos (.nombrePaciente), no un diccionario.
    datos_paciente = PacienteCreate(
        nombrePaciente="Juan Controller",
        correoPaciente="juan.ctrl@test.com",
        telefonoPaciente="555-0101",
        cedulaPaciente="ABC-999",
        direccionPaciente="Calle Test 123",
        fechaNacimiento=date(1990, 1, 1),
    )
    # 2. ACT: Llamamos a la función del controlador
    nuevo_paciente = paciente_controller.create_paciente(
        db=db_session, paciente_data=datos_paciente, user_id=usuario_default.id_usuario
    )

    # 3. ASSERT: Verificamos que el controlador hizo su trabajo
    assert nuevo_paciente.idPaciente is not None
    assert nuevo_paciente.nombrePaciente == "Juan Controller"
    # Verificamos lógica de negocio (auditoría)
    assert nuevo_paciente.id_usuario_creacion == usuario_default.id_usuario
    assert nuevo_paciente.fecha_creacion is not None


def test_leer_paciente_controller(db_session, usuario_default):
    """Prueba get_paciente"""
    # Arrange: Crear uno primero
    datos = PacienteCreate(
        nombrePaciente="Ana Lectura",
        correoPaciente="ana@test.com",
        telefonoPaciente="111",
        cedulaPaciente="222",
        direccionPaciente="Dir",
        fechaNacimiento=date(1995, 5, 5),
    )
    creado = paciente_controller.create_paciente(
        db_session, datos, usuario_default.id_usuario
    )

    # Act
    leido = paciente_controller.get_paciente(db_session, creado.idPaciente)

    # Assert
    assert leido is not None
    assert leido.idPaciente == creado.idPaciente
    assert leido.nombrePaciente == "Ana Lectura"


def test_actualizar_paciente_controller(db_session, usuario_default):
    """Prueba update_paciente y verifica que actualice la fecha de modificación"""
    # Arrange
    datos_originales = PacienteCreate(
        nombrePaciente="Pedro Original",
        correoPaciente="pedro@orig.com",
        telefonoPaciente="111",
        cedulaPaciente="222",
        direccionPaciente="Dir",
        fechaNacimiento=date(1980, 1, 1),
    )
    paciente = paciente_controller.create_paciente(
        db_session, datos_originales, usuario_default.id_usuario
    )

    # Datos nuevos
    datos_nuevos = PacienteCreate(
        nombrePaciente="Pedro Actualizado",
        correoPaciente="pedro@new.com",
        telefonoPaciente="999",
        cedulaPaciente="888",
        direccionPaciente="Nueva Dir",
        fechaNacimiento=date(1980, 1, 1),
    )

    # Act
    actualizado = paciente_controller.update_paciente(
        db=db_session,
        paciente_id=paciente.idPaciente,
        paciente_data=datos_nuevos,
        user_id=usuario_default.id_usuario,
    )

    # Assert
    assert actualizado.nombrePaciente == "Pedro Actualizado"
    assert actualizado.correoPaciente == "pedro@new.com"
    # Verificamos lógica crítica de negocio: ¿Se llenaron los campos de auditoría?
    assert actualizado.id_usuario_actualizacion == usuario_default.id_usuario
    assert actualizado.fecha_actualizacion is not None


def test_eliminar_paciente_controller(db_session, usuario_default):
    """Prueba delete_paciente"""
    # Arrange
    datos = PacienteCreate(
        nombrePaciente="Borrar Me",
        correoPaciente="borrar@test.com",
        telefonoPaciente="000",
        cedulaPaciente="000",
        direccionPaciente="X",
        fechaNacimiento=date(2000, 1, 1),
    )
    paciente = paciente_controller.create_paciente(
        db_session, datos, usuario_default.id_usuario
    )

    # Act
    eliminado = paciente_controller.delete_paciente(db_session, paciente.idPaciente)

    # Assert
    assert eliminado is not None  # La función devuelve el objeto borrado
    # Verificamos que ya no esté en BD
    busqueda = paciente_controller.get_paciente(db_session, paciente.idPaciente)
    assert busqueda is None
