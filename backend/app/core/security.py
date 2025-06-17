from datetime import datetime, timedelta
from typing import Any, Union, Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con la información del usuario
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifica y decodifica un token JWT
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

class LDAPAuth:
    def __init__(self):
        self.server = Server(
            "10.50.5.200",  # Servidor LDAP de Elite
            get_info=ALL,
            port=389,
            use_ssl=False
        )
        self.search_base = 'DC=ELITE,DC=local'

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario contra el Directorio Activo
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con la información del usuario si la autenticación es exitosa
            None si la autenticación falla
        """
        try:
            # Formatear el nombre de usuario para LDAP
            user_dn = f"{username}@elite.local"
            logger.info(f"Intentando autenticar usuario: {user_dn}")
            
            # Crear conexión LDAP
            conn = Connection(
                self.server,
                user=user_dn,
                password=password,
                authentication=SIMPLE,
                auto_bind=True,
                receive_timeout=10,
                read_only=True
            )
            
            if conn.bound:
                logger.info("✅ Autenticación LDAP exitosa")
                
                # Buscar información del usuario
                search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
                
                conn.search(
                    search_base=self.search_base,
                    search_filter=search_filter,
                    search_scope=SUBTREE,
                    attributes=['cn', 'mail', 'memberOf', 'displayName']
                )
                
                if conn.entries:
                    user_info = conn.entries[0]
                    user_data = {
                        "username": username,
                        "email": user_info.mail.value if hasattr(user_info, 'mail') else None,
                        "full_name": user_info.displayName.value if hasattr(user_info, 'displayName') else None,
                        "groups": [group.split(',')[0].split('=')[1] for group in user_info.memberOf.values] if hasattr(user_info, 'memberOf') else []
                    }
                    logger.info(f"✅ Usuario autenticado: {user_data['full_name']}")
                    return user_data
                else:
                    logger.warning("⚠️ Usuario no encontrado en el Directorio Activo")
                    return None
            else:
                logger.error("❌ La autenticación LDAP falló")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error en la autenticación LDAP: {str(e)}")
            return None
        finally:
            if 'conn' in locals():
                conn.unbind()

# Instancia global del servicio de autenticación LDAP
ldap_auth = LDAPAuth() 