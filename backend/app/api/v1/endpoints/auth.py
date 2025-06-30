from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token, ldap_auth, add_token_to_blacklist, is_token_blacklisted
from app.core.config import settings
from app.core.deps import get_current_user
from pydantic import BaseModel, validator
from typing import Optional, List
import re

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict

class LoginCredentials(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9._-]{3,50}$', v):
            raise ValueError('Username inválido: debe contener solo letras, números, puntos, guiones bajos y guiones medios, entre 3 y 50 caracteres')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Contraseña debe tener al menos 6 caracteres')
        return v

class UserInfo(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    roles: List[str]
    permissions: List[str]

@router.post("/login", response_model=TokenResponse)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autenticación de usuario contra el Directorio Activo con rate limiting (OAuth2 Form)
    
    Args:
        request: Objeto Request de FastAPI para obtener IP del cliente
        form_data: Datos del formulario con username y password
        
    Returns:
        Token JWT y datos del usuario si la autenticación es exitosa
        
    Raises:
        HTTPException: Si las credenciales son inválidas o se excede el rate limit
    """
    return await _authenticate_user(request, form_data.username, form_data.password)

@router.post("/login-json", response_model=TokenResponse)
async def login_json(request: Request, credentials: LoginCredentials):
    """
    Autenticación de usuario contra el Directorio Activo con rate limiting (JSON)
    
    Args:
        request: Objeto Request de FastAPI para obtener IP del cliente
        credentials: Credenciales en formato JSON
        
    Returns:
        Token JWT y datos del usuario si la autenticación es exitosa
        
    Raises:
        HTTPException: Si las credenciales son inválidas o se excede el rate limit
    """
    return await _authenticate_user(request, credentials.username, credentials.password)

async def _authenticate_user(request: Request, username: str, password: str):
    """
    Función común para autenticación de usuarios
    
    Args:
        request: Objeto Request de FastAPI
        username: Nombre de usuario
        password: Contraseña
        
    Returns:
        Token JWT y datos del usuario
    """
    # Obtener información del cliente
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Validar que los campos no estén vacíos
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario y contraseña son requeridos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validar formato de username
    try:
        LoginCredentials(username=username, password=password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Intentar autenticar con LDAP
    auth_result = ldap_auth.authenticate(username, password, client_ip, user_agent)
    
    # Verificar si hay error específico
    if auth_result and "error" in auth_result:
        error_type = auth_result["error"]
        error_message = auth_result["message"]
        
        if error_type == "account_locked":
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif error_type == "user_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif error_type == "ldap_error":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            # Error genérico de credenciales
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Si no hay resultado, es un error genérico
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": auth_result["username"],
            "user_id": auth_result.get("employee_id"),
            "email": auth_result["email"],
            "full_name": auth_result["full_name"],
            "roles": auth_result["roles"],
            "permissions": auth_result["permissions"],
            "department": auth_result.get("department")
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "username": auth_result["username"],
            "email": auth_result["email"],
            "full_name": auth_result["full_name"],
            "department": auth_result.get("department"),
            "roles": auth_result["roles"],
            "permissions": auth_result["permissions"]
        }
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user), token: str = Depends(get_current_user)):
    """
    Logout seguro con invalidación de token
    
    Args:
        current_user: Usuario actual autenticado
        token: Token JWT actual
        
    Returns:
        Mensaje de confirmación de logout
    """
    try:
        # Agregar token a la blacklist
        from datetime import datetime
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        add_token_to_blacklist(token, expires_at)
        
        return {
            "message": "Logout exitoso",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error durante el logout"
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtiene información del usuario actual
    
    Args:
        current_user: Usuario actual autenticado
        
    Returns:
        Información del usuario actual
    """
    return {
        "username": current_user["sub"],
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name"),
        "department": current_user.get("department"),
        "roles": current_user.get("roles", []),
        "permissions": current_user.get("permissions", [])
    }

@router.get("/permissions")
async def get_user_permissions(current_user: dict = Depends(get_current_user)):
    """
    Obtiene los permisos del usuario actual
    
    Args:
        current_user: Usuario actual autenticado
        
    Returns:
        Lista de permisos del usuario
    """
    return {
        "permissions": current_user.get("permissions", []),
        "roles": current_user.get("roles", [])
    }

@router.post("/validate-token")
async def validate_token(current_user: dict = Depends(get_current_user)):
    """
    Valida si el token actual es válido
    
    Args:
        current_user: Usuario actual autenticado
        
    Returns:
        Estado de validez del token
    """
    return {
        "valid": True,
        "user": current_user["sub"],
        "expires_in": current_user.get("exp")
    }

@router.get("/account-status/{username}")
async def get_account_status(username: str):
    """
    Obtiene el estado de bloqueo de una cuenta
    
    Args:
        username: Nombre de usuario a verificar
        
    Returns:
        Información del estado de la cuenta
    """
    try:
        from app.core.security import ldap_auth
        lockout_info = ldap_auth.account_lockout.get_account_lockout_info(username)
        
        return {
            "username": username,
            "status": "locked" if lockout_info["is_locked"] else "active",
            "lockout_info": lockout_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estado de cuenta: {str(e)}"
        ) 