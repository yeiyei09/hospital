import src.controller.medico as medico_controller
from src.schemas.medico import MedicoCreate
from datetime import date


def test_crear_medico_exitoso(db_session, usuario_default):
    # 1. ARRANGE: Preparamos los datos como un objeto Pydantic (MedicoCreate)
    # El controlador espera un objeto con atributos (.nombreMedico), no un diccionario.
    datos_medico = MedicoCreate(
        nombreMedico="medico test",
        correoMedico="corre@test.com",
        telefonoMedico="555000101",
        cedulaMedico="111100000",
        especializacion="Cardiologia test",
        numeroColegiatura="12345",
    )
    # 2. ACT: Llamamos a la función del controlador
    nuevo_medico = medico_controller.create_medico(
        db=db_session, medico_data=datos_medico, user_id=usuario_default.id_usuario
    )

    # 3. ASSERT: Verificamos que el controlador hizo su trabajo
    assert nuevo_medico.idMedico is not None
    assert nuevo_medico.nombreMedico == "medico test"
    # Verificamos lógica de negocio (auditoría)
    assert nuevo_medico.id_usuario_creacion == usuario_default.id_usuario
    assert nuevo_medico.fecha_creacion is not None


def test_leer_medico_controller(db_session, usuario_default):
    """Prueba get_medico"""
    # Arrange: Crear uno primero
    datos = MedicoCreate(
        nombreMedico="medico lectura",
        correoMedico="getmedico@test.com",
        telefonoMedico="5551234",
        cedulaMedico="0000011111",
        especializacion="Neurologia",
        numeroColegiatura="67890",
    )
    creado = medico_controller.create_medico(
        db_session, datos, usuario_default.id_usuario
    )
    # Act
    leido = medico_controller.get_medico(db_session, creado.idMedico)
    # Assert
    assert leido is not None
    assert leido.idMedico == creado.idMedico
    assert leido.nombreMedico == "medico lectura"


def test_actualizar_medico_controller(db_session, usuario_default):
    """Prueba update_medico y verifica que actualice la fecha de modificación"""
    # Arrange
    datos_originales = MedicoCreate(
        nombreMedico="medico original",
        correoMedico="medico@test.com",
        telefonoMedico="5551111",
        cedulaMedico="22223333",
        especializacion="Pediatria",
        numeroColegiatura="54321",
    )
    creado = medico_controller.create_medico(
        db_session, datos_originales, usuario_default.id_usuario
    )
    datos_actualizados = MedicoCreate(
        nombreMedico="medico actualizado",
        correoMedico="nuevocorreo@test.com",
        telefonoMedico="5552222",
        cedulaMedico="33334444",
        especializacion="Oncologia",
        numeroColegiatura="98765",
    )
    # Act
    actualizado = medico_controller.update_medico(
        db_session, creado.idMedico, datos_actualizados, usuario_default.id_usuario
    )
    # Assert
    assert actualizado is not None
    assert actualizado.nombreMedico == "medico actualizado"
    assert actualizado.correoMedico == "nuevocorreo@test.com"
    assert actualizado.fecha_actualizacion is not None
    assert actualizado.id_usuario_actualizacion == usuario_default.id_usuario


def test_eliminar_medico_controller(db_session, usuario_default):
    """Prueba delete_medico"""
    # Arrange: Crear uno primero
    datos = MedicoCreate(
        nombreMedico="medico a eliminar",
        correoMedico="borrar@test.com",
        telefonoMedico="5553333",
        cedulaMedico="44445555",
        especializacion="Dermatologia",
        numeroColegiatura="11223",
    )
    creado = medico_controller.create_medico(
        db_session, datos, usuario_default.id_usuario
    )
    # Act
    eliminado = medico_controller.delete_medico(db_session, creado.idMedico)
    # assert
    assert eliminado is not None
    assert eliminado.idMedico == creado.idMedico
    # Verificar que ya no existe en la base de datos
    buscado = medico_controller.get_medico(db_session, creado.idMedico)
    assert buscado is None
