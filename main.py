"""
Sistema de Gestión Médica - API Principal

Este módulo contiene la configuración principal de la API FastAPI
para el sistema de gestión médica, incluyendo la configuración de CORS,
registro de routers y la función principal de ejecución.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import Citas, Diagnosticos, Enfermeras, Facturas, Medicos, pacientes

app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para manejar pacientes, médicos y citas médicas.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pacientes",
            "description": "Operaciones relacionadas con el manejo de pacientes.",
        },
        {"name": "Médicos", "description": "Gestión de información de médicos."},
        {"name": "Enfermeras", "description": "Gestion de información de enfermeras."},
        {"name": "Citas", "description": "Agendamiento y consulta de citas médicas."},
        {
            "name": "Diagnósticos",
            "description": "Registro y consulta de diagnósticos médicos.",
        },
        {"name": "Facturas", "description": "Gestión de facturación y pagos."},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pacientes.router)
app.include_router(Medicos.router)
app.include_router(Enfermeras.router)
app.include_router(Citas.router)
app.include_router(Diagnosticos.router)
app.include_router(Facturas.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://mi-frontend.com",
]


def main():
    """
    Función principal para ejecutar el servidor FastAPI.

    Configura y ejecuta el servidor con uvicorn, habilitando el modo de recarga
    automática para desarrollo y configurando el host y puerto apropiados.
    """
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
