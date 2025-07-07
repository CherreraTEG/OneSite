from fastapi import APIRouter
from app.api.v1.endpoints import permisos, auth, companies
from app.api.v1.endpoints import trucks

api_router = APIRouter()

# Incluir el router de autenticación
api_router.include_router(auth.router, prefix="/auth", tags=["autenticación"])

# Incluir otros routers
api_router.include_router(permisos.router, prefix="/permisos", tags=["permisos"])

# Incluir router de trucks
api_router.include_router(trucks.router, prefix="", tags=["trucks"])

# Incluir router de empresas
api_router.include_router(companies.router, prefix="/companies", tags=["empresas"]) 