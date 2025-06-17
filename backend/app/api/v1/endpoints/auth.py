from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import create_access_token, ldap_auth
from app.core.config import settings
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autenticación de usuario contra el Directorio Activo
    
    Args:
        form_data: Datos del formulario con username y password
        
    Returns:
        Token JWT y datos del usuario si la autenticación es exitosa
        
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Intentar autenticar con LDAP
    user = ldap_auth.authenticate(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "groups": user["groups"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    } 