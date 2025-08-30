from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud, schemas

Base.metadata.create_all(bind=engine)
from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para manejar pacientes, médicos y citas médicas.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pacientes",
            "description": "Operaciones relacionadas con el manejo de pacientes."
        },
        {
            "name": "Médicos",
            "description": "Gestión de información de médicos."
        },
        {
            "name": "Enfermeras",
            "description": "Gestion de información de enfermeras."
        },
        {
            "name": "Citas",
            "description": "Agendamiento y consulta de citas médicas."
        },
        {
            "name": "Diagnósticos",
            "description": "Registro y consulta de diagnósticos médicos."
        },
        {
            "name": "Facturas",
            "description": "Gestión de facturación y pagos."
        }
    ]
)

#Creamos rutas para los pacientes

def get_db():
    db = SessionLocal() #crea sesion
    try:  #entrega la sesion
        yield db
    finally: #termina la sesion
        db.close()
        
@app.post("/pacientes/", response_model=schemas.Paciente, tags=["Pacientes"])
def create_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente.idPaciente)
    if db_paciente:                                                             #validacion
        raise HTTPException(status_code=400, detail="Paciente ya registrado")
    else: 
        paciente_creado = crud.create_paciente(db=db, paciente=paciente)

        return JSONResponse(status_code=201, content={
        "detail": "Paciente creado correctamente",
        "data": {
            "Cedula paciente": paciente_creado.idPaciente,
            "nombre de paciente": paciente_creado.nombrePaciente,
            "correo  de paciente": paciente_creado.correoPaciente
        }
        })



@app.get("/pacientes/", response_model=list[schemas.Paciente], tags=["Pacientes"])
def read_all_pacientes(db: Session = Depends(get_db)):
    pacientes_db = crud.get_pacientes(db)
    if not pacientes_db:
        raise HTTPException(status_code=404, detail="No hay pacientes registrados")
    return pacientes_db

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def read_one_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.get_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente encontrado",
            "data": {
                "cedula paciente": db_paciente.idPaciente,
                "nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

@app.delete("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def delete_paciente(paciente_id: str, db: Session = Depends(get_db)):
    db_paciente = crud.delete_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente eliminado correctamente",
            "data": {
                "Cedula paciente": db_paciente.idPaciente,
                "Nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

@app.put("/pacientes/{paciente_id}", response_model=schemas.Paciente, tags=["Pacientes"])
def update_paciente(paciente_id: str, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = crud.update_paciente(db, paciente_id=paciente_id, paciente=paciente)
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Paciente actualizado correctamente",
            "data": {
                "Cedula paciente": db_paciente.idPaciente,
                "Nombre de paciente": db_paciente.nombrePaciente,
                "correo de paciente": db_paciente.correoPaciente
            }
        })

#Creamos rutas para los medicos.

@app.post("/medicos/", response_model=schemas.Medico, tags=["Médicos"])
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico.idMedico)
    if db_medico:                                                             #validacion
        raise HTTPException(status_code=400, detail="Médico ya registrado")
    else:
        medico_creado = crud.create_medico(db=db, medico=medico)
        return JSONResponse(status_code=201, content={
        "detail" : "Medico creado cerractamente",
        "Cuerpo de la respuesta": {
            "Cedula del Medico": medico_creado.idMedico,
            "Nombre del Medico": medico_creado.nombreMedico,
            "Correo del Medico": medico_creado.correoMedico,
        }
        })

@app.get("/medicos/", response_model=list[schemas.Medico], tags=["Médicos"])
def read_all_medicos(db: Session = Depends(get_db)):
    dbGetMedicos = crud.get_medicos(db)
    if not dbGetMedicos:
        raise HTTPException(status_code=404, detail="No hay medicos registrados")
    return dbGetMedicos

@app.get("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def read_one_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.get_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Médico encontrado",
            "data": {
                "cedula medico": db_medico.idMedico,
                "especializacion": db_medico.especializacion,
                "nombre del medico": db_medico.nombreMedico,
                "correo del medico": db_medico.correoMedico
            }
        })

@app.delete("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    db_medico = crud.delete_medico(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Médico eliminado correctamente",
            "data": {
                "Cedula del Medico": db_medico.idMedico,
                "Nombre del Medico": db_medico.nombreMedico,
                "Correo del Medico": db_medico.correoMedico
            }
        })

@app.put("/medicos/{medico_id}", response_model=schemas.Medico, tags=["Médicos"])
def update_medico(medico_id: int, medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    db_medico = crud.update_medico(db, medico_id=medico_id, medico=medico)
    if db_medico is None:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Médico actualizado correctamente", 
            "data":{
                "Cedula del Medico": db_medico.idMedico,
                "Nombre del Medico": db_medico.nombreMedico,
                "Correo del Medico": db_medico.correoMedico
            }})

#creacion de rutas para las enfermeras

@app.post("/enfermeras/", response_model=schemas.Enfermera, tags=["Enfermeras"])
def create_enfermera(enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera.idEnfermera)
    if db_enfermera:                                                             #validacion
        raise HTTPException(status_code=400, detail="Enfermera ya registrada")
    else:
        enfermera_creada = crud.create_enfermera(db=db, enfermera=enfermera)
        return JSONResponse(status_code=201, content={
        "detail" : "Enfermera creada cerractamente",
        "Cuerpo de la respuesta": {
            "Cedula de la Enfermera": enfermera_creada.idEnfermera,
            "Nombre de la Enfermera": enfermera_creada.nombreEnfermera,
            "Correo de la Enfermera": enfermera_creada.correoEnfermera,
            "Area de la Enfermera": enfermera_creada.area
        }
        })
    
@app.get("/enfermeras/", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_all_enfermeras(db: Session = Depends(get_db)):
    dbGetEnfermeras = crud.get_enfermeras(db)
    if not dbGetEnfermeras:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas")
    return dbGetEnfermeras

@app.get("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def read_one_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.get_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Enfermera encontrada",
            "data": {
                "cedula enfermera": db_enfermera.idEnfermera,
                "nombre de enfermera": db_enfermera.nombreEnfermera,
                "area de enfermera": db_enfermera.area,
                "correo de enfermera": db_enfermera.correoEnfermera
            }
        })
    
@app.get("/enfermeras/area/{area}", response_model=list[schemas.Enfermera], tags=["Enfermeras"])
def read_enfermeras_por_area(area: str, db: Session = Depends(get_db)):
    db_enfermeras_area = crud.get_enfermeras_por_area(db, area=area)
    if not db_enfermeras_area:
        raise HTTPException(status_code=404, detail="No hay enfermeras registradas en esta area")
    return db_enfermeras_area

@app.delete("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def delete_enfermera(enfermera_id: int, db: Session = Depends(get_db)):
    db_enfermera = crud.delete_enfermera(db, enfermera_id=enfermera_id)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Enfermera eliminada correctamente",
            "data": {
                "Cedula de la Enfermera": db_enfermera.idEnfermera,
                "Nombre de la Enfermera": db_enfermera.nombreEnfermera,
                "Correo de la Enfermera": db_enfermera.correoEnfermera,
                "Area de la Enfermera": db_enfermera.area
            }
        })

@app.put("/enfermeras/{enfermera_id}", response_model=schemas.Enfermera, tags=["Enfermeras"])
def update_enfermera(enfermera_id: int, enfermera: schemas.EnfermeraCreate, db: Session = Depends(get_db)):
    db_enfermera = crud.update_enfermera(db, enfermera_id=enfermera_id, enfermera=enfermera)
    if db_enfermera is None:
        raise HTTPException(status_code=404, detail="Enfermera no encontrada")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Enfermera actualizada correctamente", 
            "data": {
                "Cedula de la Enfermera": db_enfermera.idEnfermera,
                "Nombre de la Enfermera": db_enfermera.nombreEnfermera,
                "Correo de la Enfermera": db_enfermera.correoEnfermera,
                "Area de la Enfermera": db_enfermera.area
            }}) 

#Aqui empiezan las rutas para las citas

@app.post("/citas/", response_model=schemas.AgendarCita, tags=["Citas"])
def create_cita(cita: schemas.AgendarCitaCreate, db: Session = Depends(get_db)):
    paciente = crud.get_paciente(db, paciente_id=cita.idPaciente)
    medico = crud.get_medico(db, medico_id=cita.idMedico)
    if not paciente and not medico:
        raise HTTPException(status_code=400, detail="Paciente y medico no existen, intenta con un paciente y medico que ya esten registrados")
    elif not medico or not paciente:
        raise HTTPException(status_code=400, detail="Médico o paciente no existe, intenta con un médico o paciente que ya este registrado")
    cita_creada = crud.create_agendar_cita(db=db, cita=cita)    
    if cita_creada is None:                                                             #validacion
        raise HTTPException(status_code=400, detail="Error al crear la cita")
    else:
        return JSONResponse(status_code=201, content={
        "detail" : "Cita creada cerractamente",
        "Cuerpo de la respuesta": {
            "ID de la Cita": cita_creada.idCita,
            "Cedula del Paciente": cita_creada.idPaciente,
            "Cedula del Medico": cita_creada.idMedico,
            "Fecha de Agendamiento": str(cita_creada.fechaAgendamiento),
            "Fecha de Emision": str(cita_creada.fechaEmision),
            "Motivo de Consulta": cita_creada.motivoConsulta
        }
        })
    
@app.get("/citas/", response_model=list[schemas.AgendarCita], tags=["Citas"])
def read_all_citas(db: Session = Depends(get_db)):
    dbGetCitas = crud.get_agendar_citas(db)
    if not dbGetCitas:
        raise HTTPException(status_code=404, detail="No hay citas registradas")
    return dbGetCitas

@app.get("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def read_one_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = crud.get_agendar_cita(db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Cita encontrada",
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }
        })

@app.put("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def update_cita(cita_id: int, cita: schemas.AgendarCitaCreate, db: Session = Depends(get_db)):
    db_cita = crud.update_agendar_cita(db, cita_id=cita_id, cita=cita)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else: 
        return JSONResponse(status_code=201, content={
            "detail": "Cita actualizada correctamente", 
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }})
    
@app.delete("/citas/{cita_id}", response_model=schemas.AgendarCita, tags=["Citas"])
def delete_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = crud.delete_agendar_cita(db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Cita eliminada correctamente",
            "data": {
                "ID de la Cita": db_cita.idCita,
                "Cedula del Paciente": db_cita.idPaciente,
                "Cedula del Medico": db_cita.idMedico,
                "Fecha de Agendamiento": str(db_cita.fechaAgendamiento),
                "Fecha de Emision": str(db_cita.fechaEmision),
                "Motivo de Consulta": db_cita.motivoConsulta
            }
        })

#Aqui empiezan las rutas para los diagnosticos

@app.post("/diagnosticos/", response_model=schemas.Diagnostico, tags=["Diagnósticos"])
def create_diagnostico(diagnostico: schemas.DiagnosticoCreate, db: Session = Depends(get_db)):
    paciente = crud.get_paciente(db, paciente_id=diagnostico.idPaciente)
    medico = crud.get_medico(db, medico_id=diagnostico.idMedico)
    enfermera = crud.get_enfermera(db, enfermera_id=diagnostico.idEnfermera)
    cita = crud.get_agendar_cita(db, cita_id=diagnostico.idCita)
    if not paciente and not medico and not enfermera and not cita:
        raise HTTPException(status_code=400, detail="Paciente, medico, enfermera y cita no existen, intenta con un paciente, medico, enfermera y cita que ya esten registrados")
    elif not medico or not paciente or not enfermera or not cita:
        raise HTTPException(status_code=400, detail="Médico, paciente, enfermera o cita no existe, intenta con un médico, paciente, enfermera o cita que ya este registrado")
    diagnostico_creado = crud.create_diagnostico(db=db, diagnostico=diagnostico)
    if diagnostico_creado is None:                                                             #validacion
        raise HTTPException(status_code=400, detail="Error al crear el diagnóstico")
    else:
        return JSONResponse(status_code=201, content={
        "detail" : "Diagnóstico creado cerractamente",
        "Cuerpo de la respuesta": {
            "ID del Diagnóstico": diagnostico_creado.idDiagnostico,
            "ID de la Cita": diagnostico_creado.idCita,
            "Cedula del Medico": diagnostico_creado.idMedico,
            "Cedula del Paciente": diagnostico_creado.idPaciente,
            "Cedula de la Enfermera": diagnostico_creado.idEnfermera,
            "Fecha de Diagnóstico": str(diagnostico_creado.fechaDiagnostico),
            "Descripción del Diagnóstico": diagnostico_creado.descripcionDiagnostico
        }
        })
    
@app.get("/diagnosticos/", response_model=list[schemas.Diagnostico], tags=["Diagnósticos"])
def read_all_diagnosticos(db: Session = Depends(get_db)):
    dbGetDiagnosticos = crud.get_diagnosticos(db)
    if not dbGetDiagnosticos:
        raise HTTPException(status_code=404, detail="No hay diagnósticos registrados")
    return dbGetDiagnosticos

@app.get("/diagnosticos/{diagnostico_id}", response_model=schemas.Diagnostico, tags=["Diagnósticos"])
def read_one_diagnostico(diagnostico_id: int, db: Session = Depends(get_db)):
    db_diagnostico = crud.get_diagnostico(db, diagnostico_id=diagnostico_id)
    if db_diagnostico is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Diagnóstico encontrado",
            "data": {
                "ID del Diagnóstico": db_diagnostico.idDiagnostico,
                "ID de la Cita": db_diagnostico.idCita,
                "Cedula del Medico": db_diagnostico.idMedico,
                "Cedula del Paciente": db_diagnostico.idPaciente,
                "Cedula de la Enfermera": db_diagnostico.idEnfermera,
                "Fecha de Diagnóstico": str(db_diagnostico.fechaDiagnostico),
                "Descripción del Diagnóstico": db_diagnostico.descripcionDiagnostico
            }
        })
    
@app.delete("/diagnosticos/{diagnostico_id}", response_model=schemas.Diagnostico, tags=["Diagnósticos"])
def delete_diagnostico(diagnostico_id: int, db: Session = Depends (get_db)):
    db_diagnostico = crud.delete_diagnostico(db, diagnostico_id=diagnostico_id)
    if db_diagnostico is None:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Diagnóstico eliminado correctamente",
            "data": {
                "ID del Diagnóstico": db_diagnostico.idDiagnostico,
                "ID de la Cita": db_diagnostico.idCita,
                "Cedula del Medico": db_diagnostico.idMedico,
                "Cedula del Paciente": db_diagnostico.idPaciente,
                "Cedula de la Enfermera": db_diagnostico.idEnfermera,
                "Fecha de Diagnóstico": str(db_diagnostico.fechaDiagnostico),
                "Descripción del Diagnóstico": db_diagnostico.descripcionDiagnostico
            }
        })
    
#aqui empiezan las rutas para las facturas

@app.post("/facturas/", response_model=schemas.Factura, tags=["Facturas"])
def create_factura(factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    paciente = crud.get_paciente(db, paciente_id=factura.idPaciente)
    cita = crud.get_agendar_cita(db, cita_id=factura.idCita)
    if not paciente and not cita:
        raise HTTPException(status_code=400, detail="Paciente y cita no existen, intenta con un paciente y cita que ya esten registrados")
    elif not cita or not paciente:
        raise HTTPException(status_code=400, detail="Cita o paciente no existe, intenta con una cita o paciente que ya este registrado")
    factura_creada = crud.create_factura(db=db, factura=factura)
    if factura_creada is None:                                                             #validacion
        raise HTTPException(status_code=400, detail="Error al crear la factura")
    else:
        return JSONResponse(status_code=201, content={
        "detail" : "Factura creada cerractamente",
        "Cuerpo de la respuesta": {
            "ID de la Factura": factura_creada.idFactura,
            "Cedula del Paciente": factura_creada.idPaciente,
            "ID de la Cita": factura_creada.idCita,
            "Estado de la Factura": factura_creada.estadoFactura,
            "Fecha de Emision": str(factura_creada.fechaEmision),
            "Fecha de Vencimiento": str(factura_creada.fechaVencimiento),
            "Monto Total": factura_creada.montoTotal
        }
        })
    
@app.get("/facturas/", response_model=list[schemas.Factura], tags=["Facturas"])
def read_all_facturas(db: Session = Depends(get_db)):
    dbGetFacturas = crud.get_facturas(db)
    if not dbGetFacturas:
        raise HTTPException(status_code=404, detail="No hay facturas registradas")
    return dbGetFacturas

@app.get("/facturas/{factura_id}", response_model=schemas.Factura, tags=["Facturas"])
def read_one_factura(factura_id: int, db: Session = Depends(get_db)):
    db_factura = crud.get_factura(db, factura_id=factura_id)
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Factura encontrada",
            "data": {
                "ID de la Factura": db_factura.idFactura,
                "Cedula del Paciente": db_factura.idPaciente,
                "ID de la Cita": db_factura.idCita,
                "Estado de la Factura": db_factura.estadoFactura,
                "Fecha de Emision": str(db_factura.fechaEmision),
                "Monto Total": db_factura.montoTotal
            }
        })
    
@app.delete("/facturas/{factura_id}", response_model=schemas.Factura, tags=["Facturas"])
def delete_factura(factura_id: int, db: Session = Depends (get_db)):
    db_factura = crud.delete_factura(db, factura_id=factura_id)
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    else:
        return JSONResponse(status_code=200, content={
            "detail": "Factura eliminada correctamente",
            "data": {
                "ID de la Factura": db_factura.idFactura,
                "Cedula del Paciente": db_factura.idPaciente,
                "ID de la Cita": db_factura.idCita,
                "Estado de la Factura": db_factura.estadoFactura,
                "Fecha de Emision": str(db_factura.fechaEmision),
                "Monto Total": db_factura.montoTotal
            }
        })
        
#