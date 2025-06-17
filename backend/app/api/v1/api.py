from fastapi import APIRouter
from app.api.v1.endpoints import permisos, auth

api_router = APIRouter()

# Incluir el router de autenticación
api_router.include_router(auth.router, prefix="/auth", tags=["autenticación"])

# Incluir otros routers
api_router.include_router(permisos.router, prefix="/permisos", tags=["permisos"]) 