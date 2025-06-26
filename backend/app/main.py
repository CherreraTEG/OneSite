from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para el sistema OneSite",
    version=settings.VERSION
)

# Configuración de CORS - Permitir todas las conexiones durante desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes durante desarrollo
    allow_credentials=False,  # Cambiar a False cuando allow_origins=["*"]
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir las rutas API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bienvenido a OneSite API"} 