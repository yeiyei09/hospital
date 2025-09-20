from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas 

# Importar los routers
from routers import pacientes, Medicos, Enfermeras, Citas, Diagnosticos, Facturas

# Crear una instancia de FastAPI
app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para manejar pacientes, médicos y citas médicas.",
    version="1.0.0",
    openapi_tags=[
            {"name": "Pacientes", "description": "Operaciones relacionadas con el manejo de pacientes."},
        {"name": "Médicos", "description": "Gestión de información de médicos."},
        {"name": "Enfermeras", "description": "Gestion de información de enfermeras."},
        {"name": "Citas", "description": "Agendamiento y consulta de citas médicas."},
        {"name": "Diagnósticos", "description": "Registro y consulta de diagnósticos médicos."},
        {"name": "Facturas", "description": "Gestión de facturación y pagos."}
    ]
)

# Configuración de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes (orígenes)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todas las cabeceras
)

#Hacemos llamamiento de las rutas para poder usarlas
app.include_router(pacientes.router)
app.include_router(Medicos.router)
app.include_router(Enfermeras.router)
app.include_router(Citas.router)
app.include_router(Diagnosticos.router)
app.include_router(Facturas.router)

 
# Configuración de CORS
origins = [
    "http://localhost", # por si se usa otro puerto
    "http://localhost:3000",  #para desarrollo del frontend
    "https://mi-frontend.com" # para producción
]