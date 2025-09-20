from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
import crud, schemas

# Creamos el router para los pacientes
# Define un prefijo para las rutas y etiquetas para la documentación
# En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter
router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)
 
#aqui empiezan las rutas para las facturas

@router.post("/facturas/", response_model=schemas.Factura, tags=["Facturas"])
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
    
@router.get("/facturas/", response_model=list[schemas.Factura], tags=["Facturas"])
def read_all_facturas(db: Session = Depends(get_db)):
    dbGetFacturas = crud.get_facturas(db)
    if not dbGetFacturas:
        raise HTTPException(status_code=404, detail="No hay facturas registradas")
    return dbGetFacturas

@router.get("/facturas/{factura_id}", response_model=schemas.Factura, tags=["Facturas"])
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
    
@router.delete("/facturas/{factura_id}", response_model=schemas.Factura, tags=["Facturas"])
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