from fastapi import APIRouter
from app.api.v1.endpoints import permisos

api_router = APIRouter()

api_router.include_router(permisos.router, prefix="/permisos", tags=["permisos"]) 