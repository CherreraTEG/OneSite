from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models.permisos import Permiso
from app.schemas.permisos import PermisoCreate, PermisoUpdate, PermisoInDB
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PermisoInDB])
async def get_permisos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene la lista de todos los permisos del sistema.
    
    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado actual
        
    Returns:
        List[PermisoInDB]: Lista de permisos
        
    Raises:
        HTTPException: Si hay un error al obtener los permisos
    """
    try:
        permisos = db.query(Permiso).all()
        return permisos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener permisos: {str(e)}"
        )

@router.post("/", response_model=PermisoInDB, status_code=status.HTTP_201_CREATED)
async def create_permiso(
    permiso: PermisoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crea un nuevo permiso en el sistema.
    
    Args:
        permiso: Datos del permiso a crear
        db: Sesión de base de datos
        current_user: Usuario autenticado actual
        
    Returns:
        PermisoInDB: Permiso creado
        
    Raises:
        HTTPException: Si hay un error al crear el permiso
    """
    try:
        db_permiso = Permiso(**permiso.dict())
        db.add(db_permiso)
        db.commit()
        db.refresh(db_permiso)
        return db_permiso
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear permiso: {str(e)}"
        ) 