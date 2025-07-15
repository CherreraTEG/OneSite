from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, and_
from typing import List, Optional
from app.db.databases import get_main_db, get_companies_db
from app.crud.crud_user import crud_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.core.deps import get_current_user
from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.models.user_company_permission import UserCompanyPermission
from app.models.role import Role
from pydantic import BaseModel

router = APIRouter()

class UserCompanyPermissionCreate(BaseModel):
    company_code: str
    permission_type: str = "read"

class UserWithPermissions(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    companies: List[dict] = []
    roles: List[str] = []

class UserCreateRequest(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str
    is_active: bool = True
    is_superuser: bool = False
    company_permissions: List[UserCompanyPermissionCreate] = []

@router.get("/test")
def test_users():
    """Endpoint de prueba simple"""
    return {"message": "Users endpoint funcionando"}

@router.get("/", response_model=List[UserWithPermissions])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_main_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene una lista paginada de usuarios con sus permisos de empresa
    """
    try:
        # Verificar que el usuario actual tenga permisos de administrador
        if not current_user.get("permissions") or "*" not in current_user.get("permissions", []):
            if "users:read" not in current_user.get("permissions", []):
                raise HTTPException(status_code=403, detail="No tienes permisos para ver usuarios")
        
        # Construir consulta base
        query = db.query(UserModel)
        
        if active_only:
            query = query.filter(UserModel.is_active == True)
        
        if search:
            query = query.filter(
                UserModel.username.contains(search) |
                UserModel.email.contains(search) |
                UserModel.full_name.contains(search)
            )
        
        # Obtener usuarios paginados
        users = query.offset(skip).limit(limit).all()
        
        # Para cada usuario, obtener sus permisos de empresa
        result = []
        for user_obj in users:
            # Obtener permisos de empresa
            company_permissions = db.query(UserCompanyPermission).filter(
                and_(
                    UserCompanyPermission.user_id == user_obj.id,
                    UserCompanyPermission.is_active == True
                )
            ).all()
            
            companies = []
            for perm in company_permissions:
                companies.append({
                    "company_code": perm.company_code,
                    "permission_type": perm.permission_type
                })
            
            result.append(UserWithPermissions(
                id=user_obj.id,
                username=user_obj.username,
                email=user_obj.email,
                full_name=user_obj.full_name,
                is_active=user_obj.is_active,
                is_superuser=user_obj.is_superuser,
                companies=companies,
                roles=[]  # TODO: Implementar roles cuando exista la relación
            ))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo usuarios: {str(e)}")

@router.post("/", response_model=UserWithPermissions)
def create_user(
    user_data: UserCreateRequest,
    db: Session = Depends(get_main_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crea un nuevo usuario en OneSite con permisos de empresa
    """
    try:
        # Verificar que el usuario actual tenga permisos de administrador
        if not current_user.get("permissions") or "*" not in current_user.get("permissions", []):
            if "users:create" not in current_user.get("permissions", []):
                raise HTTPException(status_code=403, detail="No tienes permisos para crear usuarios")
        
        # Verificar que el username no exista
        existing_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Verificar que el email no exista
        existing_email = db.query(UserModel).filter(UserModel.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email ya existe")
        
        # Crear el usuario
        hashed_password = get_password_hash(user_data.password)
        new_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Crear permisos de empresa
        created_permissions = []
        for company_perm in user_data.company_permissions:
            permission = UserCompanyPermission(
                user_id=new_user.id,
                company_code=company_perm.company_code,
                permission_type=company_perm.permission_type,
                created_by=current_user["sub"]
            )
            db.add(permission)
            created_permissions.append({
                "company_code": company_perm.company_code,
                "permission_type": company_perm.permission_type
            })
        
        db.commit()
        
        return UserWithPermissions(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            is_active=new_user.is_active,
            is_superuser=new_user.is_superuser,
            companies=created_permissions,
            roles=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")

@router.get("/{user_id}", response_model=UserWithPermissions)
def get_user(
    user_id: int,
    db: Session = Depends(get_main_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene un usuario específico por ID
    """
    try:
        # Verificar permisos
        if not current_user.get("permissions") or "*" not in current_user.get("permissions", []):
            if "users:read" not in current_user.get("permissions", []):
                raise HTTPException(status_code=403, detail="No tienes permisos para ver usuarios")
        
        # Buscar usuario
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Obtener permisos de empresa
        company_permissions = db.query(UserCompanyPermission).filter(
            and_(
                UserCompanyPermission.user_id == user_obj.id,
                UserCompanyPermission.is_active == True
            )
        ).all()
        
        companies = []
        for perm in company_permissions:
            companies.append({
                "company_code": perm.company_code,
                "permission_type": perm.permission_type
            })
        
        return UserWithPermissions(
            id=user_obj.id,
            username=user_obj.username,
            email=user_obj.email,
            full_name=user_obj.full_name,
            is_active=user_obj.is_active,
            is_superuser=user_obj.is_superuser,
            companies=companies,
            roles=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo usuario: {str(e)}")

@router.put("/{user_id}", response_model=UserWithPermissions)
def update_user(
    user_id: int,
    user_data: UserCreateRequest,
    db: Session = Depends(get_main_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza un usuario existente
    """
    try:
        # Verificar permisos
        if not current_user.get("permissions") or "*" not in current_user.get("permissions", []):
            if "users:write" not in current_user.get("permissions", []):
                raise HTTPException(status_code=403, detail="No tienes permisos para modificar usuarios")
        
        # Buscar usuario
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Verificar username único (excluyendo el usuario actual)
        if user_data.username != user_obj.username:
            existing_user = db.query(UserModel).filter(
                and_(UserModel.username == user_data.username, UserModel.id != user_id)
            ).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Verificar email único (excluyendo el usuario actual)
        if user_data.email != user_obj.email:
            existing_email = db.query(UserModel).filter(
                and_(UserModel.email == user_data.email, UserModel.id != user_id)
            ).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="Email ya existe")
        
        # Actualizar datos del usuario
        user_obj.username = user_data.username
        user_obj.email = user_data.email
        user_obj.full_name = user_data.full_name
        user_obj.is_active = user_data.is_active
        user_obj.is_superuser = user_data.is_superuser
        
        # Actualizar contraseña si se proporciona
        if user_data.password:
            user_obj.hashed_password = get_password_hash(user_data.password)
        
        # Desactivar permisos existentes
        db.query(UserCompanyPermission).filter(
            UserCompanyPermission.user_id == user_id
        ).update({"is_active": False})
        
        # Crear nuevos permisos
        created_permissions = []
        for company_perm in user_data.company_permissions:
            permission = UserCompanyPermission(
                user_id=user_id,
                company_code=company_perm.company_code,
                permission_type=company_perm.permission_type,
                created_by=current_user["sub"]
            )
            db.add(permission)
            created_permissions.append({
                "company_code": company_perm.company_code,
                "permission_type": company_perm.permission_type
            })
        
        db.commit()
        db.refresh(user_obj)
        
        return UserWithPermissions(
            id=user_obj.id,
            username=user_obj.username,
            email=user_obj.email,
            full_name=user_obj.full_name,
            is_active=user_obj.is_active,
            is_superuser=user_obj.is_superuser,
            companies=created_permissions,
            roles=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando usuario: {str(e)}")

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_main_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Desactiva un usuario (soft delete)
    """
    try:
        # Verificar permisos
        if not current_user.get("permissions") or "*" not in current_user.get("permissions", []):
            if "users:delete" not in current_user.get("permissions", []):
                raise HTTPException(status_code=403, detail="No tienes permisos para eliminar usuarios")
        
        # Buscar usuario
        user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # No permitir eliminar el propio usuario
        if user_obj.username == current_user["sub"]:
            raise HTTPException(status_code=400, detail="No puedes eliminar tu propio usuario")
        
        # Desactivar usuario
        user_obj.is_active = False
        
        # Desactivar permisos
        db.query(UserCompanyPermission).filter(
            UserCompanyPermission.user_id == user_id
        ).update({"is_active": False})
        
        db.commit()
        
        return {"message": "Usuario desactivado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error eliminando usuario: {str(e)}")