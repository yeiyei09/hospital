# hospital
Proyecto para trabajar con APIs en un programa para un hospital

AUTORES: Andres Felipe Gallego García y Yefferson Gómez Ramirez.
 
TITULO DEL PROYECTO: Hospital/Clinica

DESCRIPCIÓN: Este proyecto está orientado al entorno hospitalario o clínico. Permite gestionar empleados y pacientes, registrar agendamientos de citas médicas, diagnósticos posteriores a la consulta y generar facturas que detallan el valor de la atención junto con el motivo de la misma. Además, facilita el seguimiento del historial clínico y administrativo de cada proceso dentro de la entidad, manteniendo un control sobre los recursos humanos disponibles para garantizar una atención eficiente.

ARQUITECTURA: 
Se utiliza una arquitectura basada en capas implementada con FastAPI, lo que permite mantener el código organizado, escalable y fácil de mantener. Las capas principales son:

Models: Define las clases que representan las tablas de la base de datos utilizando SQLAlchemy.
Schemas: Contiene las clases Pydantic para validar y serializar los datos de entrada y salida.
CRUD: Implementa funciones que interactúan directamente con la base de datos.
Routes: Define los endpoints de la API, gestionando las peticiones HTTP.
Database (Dependencias): Configura la conexión con la base de datos y gestiona las sesiones.

REQUISITOS DE INSTALACIÓN: 
Para instalar las dependencias necesarias, se recomienda usar pip install con los siguientes paquetes:

greenlet: Permite la ejecución cooperativa de tareas (corutinas).
pydantic: Validación y serialización de datos.
pyodbc: Conector ODBC para bases de datos como SQL Server.
SQLAlchemy: ORM para interactuar con la base de datos mediante clases y objetos.
fastapi: Framework principal del proyecto.
uvicorn: Servidor ASGI para ejecutar aplicaciones FastAPI.

INSTRUCCIONES DE EJECUCIÓN: 
-Usar uvicorn para levantar el servidor con el siguiente comando:
uvicorn main:app --reload
main: nombre del archivo principal (ajústalo si tu archivo se llama diferente).
app: instancia de FastAPI.
--reload: permite recargar automáticamente el servidor al hacer cambios en el código (ideal para desarrollo).

-Acceder a documentación interactiva
Una vez el servidor esté corriendo, abre tu navegador y visita:
Documentación Swagger: http://localhost:8000/docs (Swagger)
Documentación ReDoc: http://localhost:8000/redoc 

-Una vez hecho eso puedes interactuar con swagger para probar cada uno de los endpoints.

DESCRIPCIÓN DE ENDPOINTS.

---- POST/pacientes && POST/medicos && POST/enfermeras --- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite registrar un nuevo paciente en la base de datos. Antes de crear el paciente, se valida que no exista previamente usando su número de cédula (idPaciente). Si ya está registrado, se devuelve un error.

Body (JSON):
{
  "idPaciente": "123456789",
  "nombrePaciente": "Juan Pérez",
  "correoPaciente": "juan.perez@example.com"
}

Validación: Si el paciente ya existe (por su cédula), se devuelve un error 400 con el mensaje "Paciente ya registrado".

Respuesta exitosa (201 Created):
{
  "detail": "Paciente creado correctamente",
  "data": {
    "Cedula paciente": "123456789",
    "nombre de paciente": "Juan Pérez",
    "correo  de paciente": "juan.perez@example.com"
  }
}
Tags: Pacientes, Medicos, Enfermeras

---- GET/pacientes && GET/medicos && GET/enfermeras --- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite obtener la lista completa de pacientes registrados en la base de datos. Si no hay pacientes, se devuelve un error indicando que no hay registros disponibles.

Parámetros:
No requiere parámetros de entrada.

Ejemplo de Uso: GET /pacientes/

Respuesta exitosa(200 OK)
[
  {
    "idPaciente": "123456789",
    "nombrePaciente": "Juan Pérez",
    "correoPaciente": "juan.perez@example.com"
  },
  {
    "idPaciente": "987654321",
    "nombrePaciente": "Ana Gómez",
    "correoPaciente": "ana.gomez@example.com"
  }
]

Respuesta en caso de error(404 Not Found):
{
  "detail": "No hay pacientes registrados"
}

Tags: Pacientes, Medicos, Enfermeras

---- GET /pacientes/{paciente_id} && GET /medicos/{medico_id} && GET /enfermeras/{enfermera_id} --- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite consultar los datos de un paciente específico usando su número de cédula (paciente_id). Si el paciente no existe en la base de datos, se devuelve un error.

Parámetros:
paciente_id (string): número de cédula del paciente que se desea consultar.

Ejemplo de Uso: GET /pacientes/123456789

Respuesta exitosa (200 OK)
{
  "detail": "Paciente encontrado",
  "data": {
    "cedula paciente": "123456789",
    "nombre de paciente": "Juan Pérez",
    "correo de paciente": "juan.perez@example.com"
  }
}

Respuesta en caso de error (404 Not Found):
{
  "detail": "Paciente no encontrado"
}

Tags: Pacientes, Medicos, Enfermeras 

---- DELETE /pacientes/{paciente_id} && DELETE /medicos/{medico_id} && DELETE /enfermeras/{enfermera_id} --- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite eliminar un paciente específico de la base de datos utilizando su número de cédula (paciente_id). Si el paciente no existe, se devuelve un error indicando que no se encontró.

Parámetros:
paciente_id (string): número de cédula del paciente que se desea eliminar.

Ejemplo de uso: DELETE /pacientes/123456789

Respuesta exitosa (200 OK):
{
  "detail": "Paciente eliminado correctamente",
  "data": {
    "Cedula paciente": "123456789",
    "Nombre de paciente": "Juan Pérez",
    "correo de paciente": "juan.perez@example.com"
  }
}

Respuesta en caso de error (404 Not Found):
{
  "detail": "Paciente no encontrado"
}

Tags: Pacientes, Medicos, Enfermeras

---- PUT /pacientes/{paciente_id} && PUT /medicos/{medico_id} && PUT /enfermeras/{enfermera_id} --- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite actualizar la información de un paciente existente en la base de datos, utilizando su número de cédula (paciente_id). Si el paciente no existe, se devuelve un error.

Parámetros:
paciente_id (string): número de cédula del paciente que se desea actualizar.

Body (JSON):
{
  "idPaciente": "123456789",
  "nombrePaciente": "Juan Pérez Actualizado",
  "correoPaciente": "juan.perez.actualizado@example.com"
}

Ejemplo de uso: PUT /pacientes/123456789

Respuesta exitosa (200 OK):
{
  "detail": "Paciente actualizado correctamente",
  "data": {
    "Cedula paciente": "123456789",
    "Nombre de paciente": "Juan Pérez Actualizado",
    "correo de paciente": "juan.perez.actualizado@example.com"
  }
}

Respuesta en caso de error (404 Not Found):
{
  "detail": "Paciente no encontrado"
}

Tags: Pacientes, Medicos, Enfermeras

---- POST/citas -----

Descripción: Este endpoint permite agendar una nueva cita médica entre un paciente y un médico. Antes de crear la cita, se valida que ambos estén registrados en la base de datos. Si alguno de los dos no existe, se devuelve un mensaje de error específico.

Body (JSON):
{
  "idPaciente": "123456789",
  "idMedico": 1,
  "fechaAgendamiento": "2025-09-01",
  "motivoConsulta": "Chequeo general"
}

Validaciones: 
Si el paciente y el médico no existen, se devuelve:
{
  "detail": "Paciente y medico no existen, intenta con un paciente y medico que ya esten registrados"
}
Si uno de los dos no existe, se devuelve:
{
  "detail": "Médico o paciente no existe, intenta con un médico o paciente que ya este registrado"
}
Si ocurre un error al crear la cita, se devuelve:
{
  "detail": "Error al crear la cita"
}
Respuesta exitosa (201 Created):
{
  "detail": "Cita creada cerractamente",
  "Cuerpo de la respuesta": {
    "ID de la Cita": 10,
    "Cedula del Paciente": "123456789",
    "Cedula del Medico": 1,
    "Fecha de Agendamiento": "2025-09-01",
    "Fecha de Emision": "2025-08-30T01:00:00",
    "Motivo de Consulta": "Chequeo general"
  }
}

Tags: Citas

---- GET/citas && GET/diagnosticos && GET/facturas ----- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite obtener la lista completa de citas médicas registradas en la base de datos. Si no hay citas disponibles, se devuelve un mensaje de error.

Parámetros:
No requiere parámetros de entrada.

Ejemplo de uso: GET /citas/

Respuesta exitosa (200 OK):
[
  {
    "idCita": 10,
    "idPaciente": "123456789",
    "idMedico": 1,
    "fechaAgendamiento": "2025-09-01",
    "fechaEmision": "2025-08-30T01:00:00",
    "motivoConsulta": "Chequeo general"
  },
  {
    "idCita": 11,
    "idPaciente": "987654321",
    "idMedico": 2,
    "fechaAgendamiento": "2025-09-02",
    "fechaEmision": "2025-08-30T01:30:00",
    "motivoConsulta": "Dolor abdominal"
  }
]

Respuesta en caso de error (404 Not Found):
{
  "detail": "No hay citas registradas"
}

Tags: Citas

---- GET /citas/{cita_id} && GET/diagnosticos/{diagnostico_id} && GET/facturas/{factura_id} ----- (Funciona del mismo modo para esos endpoints ) -----

Descripción: Este endpoint permite consultar los detalles de una cita específica utilizando su identificador único (cita_id). Si la cita no existe en la base de datos, se devuelve un mensaje de error.

Parámetro: 
cita_id (integer): ID de la cita que se desea consultar.

Ejemplo de uso: GET /citas/10

Respuesta exitosa (200 OK):
{
  "detail": "Cita encontrada",
  "data": {
    "ID de la Cita": 10,
    "Cedula del Paciente": "123456789",
    "Cedula del Medico": 1,
    "Fecha de Agendamiento": "2025-09-01",
    "Fecha de Emision": "2025-08-30T01:00:00",
    "Motivo de Consulta": "Chequeo general"
  }
}

Respuesta en caso de error (404 Not Found):
{
  "detail": "Cita no encontrada"
}

Tags: Citas, Diagnosticos, Facturas

---- PUT /citas/{cita_id} -----

Descripción: Este endpoint permite actualizar una cita médica existente. Se debe proporcionar el ID de la cita en la URL y los nuevos datos en el cuerpo de la solicitud. Antes de realizar la actualización, se valida que la cita exista en la base de datos. Si no se encuentra, se devuelve un mensaje de error.

Parámetros:
cita_id (int): ID de la cita que se desea actualizar.

Body (JSON):
{
  "idPaciente": "123456789",
  "idMedico": 2,
  "fechaAgendamiento": "2025-09-10",
  "motivoConsulta": "Dolor abdominal"
}

Validaciones: 
Si la cita no existe, se devuelve:
{
  "detail": "Cita no encontrada"
}

Si ocurre un error al actualizar la cita, se devuelve:
{
  "detail": "Error al actualizar la cita"
}

Respuesta exitosa (201 Created):
{
  "detail": "Cita actualizada correctamente",
  "data": {
    "ID de la Cita": 10,
    "Cedula del Paciente": "123456789",
    "Cedula del Medico": 2,
    "Fecha de Agendamiento": "2025-09-10",
    "Fecha de Emision": "2025-08-30T02:38:00",
    "Motivo de Consulta": "Dolor abdominal"
  }
}

Tags: Citas

---- POST /diagnosticos/ -----

Descripción: Este endpoint permite registrar un nuevo diagnóstico médico relacionado con una cita previamente agendada. Antes de crear el diagnóstico, se valida que el paciente, el médico, la enfermera y la cita existan en la base de datos. Si alguno de ellos no está registrado, se devuelve un mensaje de error específico.

Body (JSON):
{
  "idPaciente": "123456789",
  "idMedico": 1,
  "idEnfermera": 3,
  "idCita": 10,
  "fechaDiagnostico": "2025-08-30",
  "descripcionDiagnostico": "Paciente presenta síntomas de gastritis"
}

Validaciones:
Si ninguno de los registros existe, se devuelve:
{
  "detail": "Paciente, medico, enfermera y cita no existen, intenta con un paciente, medico, enfermera y cita que ya esten registrados"
}

Si alguno de los registros no existe, se devuelve:
{
  "detail": "Médico, paciente, enfermera o cita no existe, intenta con un médico, paciente, enfermera o cita que ya esté registrado"
}

Si ocurre un error al crear el diagnóstico, se devuelve:
{
  "detail": "Error al crear el diagnóstico"
}

Respuesta exitosa (201 Created):
{
  "detail": "Diagnóstico creado cerractamente",
  "Cuerpo de la respuesta": {
    "ID del Diagnóstico": 5,
    "ID de la Cita": 10,
    "Cedula del Medico": 1,
    "Cedula del Paciente": "123456789",
    "Cedula de la Enfermera": 3,
    "Fecha de Diagnóstico": "2025-08-30",
    "Descripción del Diagnóstico": "Paciente presenta síntomas de gastritis"
  }
}

Tags: Diagnósticos

---- POST/facturas/ -----

Descripción: Este endpoint permite registrar una nueva factura médica asociada a una cita y a un paciente. Antes de crear la factura, se valida que tanto el paciente como la cita existan en la base de datos. Si alguno de los dos no está registrado, se devuelve un mensaje de error específico.

Body (JSON):
{
  "idPaciente": "123456789",
  "idCita": 10,
  "estadoFactura": "Pendiente",
  "fechaEmision": "2025-08-30",
  "fechaVencimiento": "2025-09-15",
  "montoTotal": 150000
}

Validaciones:
Si el paciente y la cita no existen, se devuelve:
{
  "detail": "Paciente y cita no existen, intenta con un paciente y cita que ya estén registrados"
}

Si uno de los dos no existe, se devuelve:
{
  "detail": "Cita o paciente no existe, intenta con una cita o paciente que ya esté registrado"
}

Si ocurre un error al crear la factura, se devuelve:
{
  "detail": "Error al crear la factura"
}

Respuesta exitosa (201 Created):
{
  "detail": "Factura creada cerractamente",
  "Cuerpo de la respuesta": {
    "ID de la Factura": 7,
    "Cedula del Paciente": "123456789",
    "ID de la Cita": 10,
    "Estado de la Factura": "Pendiente",
    "Fecha de Emision": "2025-08-30",
    "Fecha de Vencimiento": "2025-09-15",
    "Monto Total": 150000
  }
}

Tags: Facturas