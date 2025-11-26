import src.controller.enfermera as enfermera_controller
from src.schemas.enfermera import EnfermeraCreate
from datetime import date


def test_crear_enfermera_exitoso(db_session, usuario_default):
    # 1. ARRANGE: Preparamos los datos como un objeto Pydantic (EnfermeraCreate)
    # El controlador espera un objeto con atributos (.nombreEnfermera), no un diccionario.
    datos_enfermera = EnfermeraCreate(
        nombreEnfermera="enfermera test",
        correoEnfermera="correo@test.com",
        telefonoEnfermera="555000101",
        cedulaEnfermera="111100000",
        areaEnfermera="Pediatria test",
    )
    # 2. ACT: Llamamos a la función del controlador
    nueva_enfermera = enfermera_controller.create_enfermera(
        db=db_session,
        enfermera_data=datos_enfermera,
        user_id=usuario_default.id_usuario,
    )

    # 3. ASSERT: Verificamos que el controlador hizo su trabajo
    assert nueva_enfermera.idEnfermera is not None
    assert nueva_enfermera.nombreEnfermera == "enfermera test"
    assert nueva_enfermera.correoEnfermera == "correo@test.com"
    assert nueva_enfermera.telefonoEnfermera == "555000101"
    assert nueva_enfermera.cedulaEnfermera == "111100000"
    assert nueva_enfermera.areaEnfermera == "Pediatria test"
    # Verificamos lógica de negocio (auditoría)
    assert nueva_enfermera.id_usuario_creacion == usuario_default.id_usuario
    assert nueva_enfermera.fecha_creacion is not None


def test_leer_enfermera_controller(db_session, usuario_default):
    """Prueba get_enfermera"""
    # Arrange: Crear uno primero
    datos = EnfermeraCreate(
        nombreEnfermera="enfermera lectura",
        correoEnfermera="getenfermera@tes.com",
        telefonoEnfermera="5551234",
        cedulaEnfermera="0000011111",
        areaEnfermera="Cardiologia",
    )
    creado = enfermera_controller.create_enfermera(
        db_session, datos, usuario_default.id_usuario
    )
    # Act
    leido = enfermera_controller.get_enfermera(db_session, creado.idEnfermera)
    # Assert
    assert leido is not None
    assert leido.idEnfermera == creado.idEnfermera
    assert leido.nombreEnfermera == "enfermera lectura"


def test_actualizar_enfermera_controller(db_session, usuario_default):
    """Prueba update_enfermera y verifica que actualice la fecha de modificación"""
    # Arrange
    datos_originales = EnfermeraCreate(
        nombreEnfermera="enfermera original",
        correoEnfermera="enfermera@test.com",
        telefonoEnfermera="5551111",
        cedulaEnfermera="22223333",
        areaEnfermera="Neurologia",
    )
    creado = enfermera_controller.create_enfermera(
        db_session, datos_originales, usuario_default.id_usuario
    )
    datos_actualizados = EnfermeraCreate(
        nombreEnfermera="enfermera actualizada",
        correoEnfermera="actualizada@test.com",
        telefonoEnfermera="5552222",
        cedulaEnfermera="33334444",
        areaEnfermera="Oncologia",
    )
    # Act
    actualizado = enfermera_controller.update_enfermera(
        db_session, creado.idEnfermera, datos_actualizados, usuario_default.id_usuario
    )
    # Assert
    assert actualizado is not None
    assert actualizado.idEnfermera == creado.idEnfermera
    assert actualizado.nombreEnfermera == "enfermera actualizada"
    assert actualizado.correoEnfermera == "actualizada@test.com"
    assert actualizado.telefonoEnfermera == "5552222"
    assert actualizado.cedulaEnfermera == "33334444"
    assert actualizado.areaEnfermera == "Oncologia"
    assert actualizado.fecha_actualizacion is not None
    assert actualizado.id_usuario_actualizacion == usuario_default.id_usuario


def test_eliminar_enfermera_controller(db_session, usuario_default):
    """Prueba delete_enfermera"""
    # Arrange: Crear uno primero
    datos = EnfermeraCreate(
        nombreEnfermera="enfermera a eliminar",
        correoEnfermera="borrar@test.com",
        telefonoEnfermera="5553333",
        cedulaEnfermera="44445555",
        areaEnfermera="Urgencias",
    )
    creado = enfermera_controller.create_enfermera(
        db_session, datos, usuario_default.id_usuario
    )
    # Act
    eliminado = enfermera_controller.delete_enfermera(db_session, creado.idEnfermera)
    # Assert
    assert eliminado is not None
    assert eliminado.idEnfermera == creado.idEnfermera
    # Verificar que ya no existe en la base de datos
    buscado = enfermera_controller.get_enfermera(db_session, creado.idEnfermera)
    assert buscado is None
