from datetime import datetime, timedelta
from typing import Any, Union, Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE
import logging
import ssl
from ldap3 import Tls
import redis
import os

# Configurar logging seguro
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurar Redis para rate limiting y blacklist
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

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
        # Verificar si el token está en la blacklist
        if is_token_blacklisted(token):
            return None
            
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def is_token_blacklisted(token: str) -> bool:
    """Verifica si un token está en la blacklist"""
    try:
        return redis_client.exists(f"blacklist:{token}")
    except Exception as e:
        logger.error(f"Error verificando blacklist: {e}")
        return False

def add_token_to_blacklist(token: str, expires_at: datetime):
    """Agrega un token a la blacklist"""
    try:
        ttl = int((expires_at - datetime.utcnow()).total_seconds())
        if ttl > 0:
            redis_client.setex(f"blacklist:{token}", ttl, "blacklisted")
    except Exception as e:
        logger.error(f"Error agregando token a blacklist: {e}")

class SecureLogger:
    """Clase para logging seguro sin exponer información sensible"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def log_login_attempt(self, username: str, success: bool, ip_address: str, user_agent: str = None):
        """Registra intentos de login sin exponer contraseñas"""
        status = "SUCCESS" if success else "FAILED"
        log_message = f"Login attempt - User: {username}, Status: {status}, IP: {ip_address}"
        if user_agent:
            log_message += f", User-Agent: {user_agent[:100]}"
        
        if success:
            self.logger.info(log_message)
        else:
            self.logger.warning(log_message)
    
    def log_security_event(self, event_type: str, details: str, severity: str = "INFO"):
        """Registra eventos de seguridad"""
        self.logger.warning(f"Security Event - Type: {event_type}, Details: {details}, Severity: {severity}")

class AccountLockout:
    """Gestión de bloqueo de cuentas por intentos fallidos"""
    
    def __init__(self):
        self.max_attempts = settings.MAX_LOGIN_ATTEMPTS
        self.lockout_duration = settings.ACCOUNT_LOCKOUT_MINUTES * 60  # Convertir a segundos
    
    def is_account_locked(self, username: str) -> bool:
        """Verifica si una cuenta está bloqueada"""
        try:
            lock_key = f"lockout:{username}"
            return redis_client.exists(lock_key)
        except Exception as e:
            logger.error(f"Error verificando bloqueo de cuenta: {e}")
            return False
    
    def get_account_lockout_info(self, username: str) -> dict:
        """Obtiene información detallada sobre el estado de bloqueo de una cuenta"""
        try:
            lock_key = f"lockout:{username}"
            attempt_key = f"attempts:{username}"
            
            is_locked = redis_client.exists(lock_key)
            attempts = redis_client.get(attempt_key)
            lock_ttl = redis_client.ttl(lock_key) if is_locked else -1
            attempt_ttl = redis_client.ttl(attempt_key) if attempts else -1
            
            return {
                "is_locked": bool(is_locked),
                "failed_attempts": int(attempts) if attempts else 0,
                "lock_remaining_seconds": lock_ttl if lock_ttl > 0 else 0,
                "attempts_remaining_seconds": attempt_ttl if attempt_ttl > 0 else 0,
                "max_attempts": self.max_attempts,
                "lockout_duration_minutes": self.lockout_duration // 60
            }
        except Exception as e:
            logger.error(f"Error obteniendo información de bloqueo: {e}")
            return {
                "is_locked": False,
                "failed_attempts": 0,
                "lock_remaining_seconds": 0,
                "attempts_remaining_seconds": 0,
                "max_attempts": self.max_attempts,
                "lockout_duration_minutes": self.lockout_duration // 60
            }
    
    def record_failed_attempt(self, username: str):
        """Registra un intento fallido"""
        try:
            attempt_key = f"attempts:{username}"
            attempts = redis_client.incr(attempt_key)
            
            # Establecer TTL para el contador de intentos (1 hora)
            if attempts == 1:
                redis_client.expire(attempt_key, 3600)
            
            if attempts >= self.max_attempts:
                lock_key = f"lockout:{username}"
                redis_client.setex(lock_key, self.lockout_duration, "locked")
                redis_client.delete(attempt_key)
                logger.warning(f"Cuenta bloqueada: {username} por {self.max_attempts} intentos fallidos")
        except Exception as e:
            logger.error(f"Error registrando intento fallido: {e}")
    
    def reset_failed_attempts(self, username: str):
        """Resetea los intentos fallidos después de un login exitoso"""
        try:
            attempt_key = f"attempts:{username}"
            redis_client.delete(attempt_key)
        except Exception as e:
            logger.error(f"Error reseteando intentos fallidos: {e}")

# Cache global para la configuración SSL optimizada
_ssl_config_cache = {}

class LDAPAuth:
    def __init__(self):
        # Usar configuración SSL cacheada para evitar múltiples intentos
        self.server = self._get_cached_server()
        self.search_base = settings.AD_BASE_DN
        self.secure_logger = SecureLogger()
        self.account_lockout = AccountLockout()
    
    def _get_cached_server(self):
        """Obtiene un servidor LDAP con configuración SSL cacheada"""
        cache_key = f"{settings.AD_SERVER}:{settings.AD_PORT}:{settings.AD_USE_SSL}"
        
        if cache_key in _ssl_config_cache:
            logger.info("Usando configuración SSL cacheada")
            return _ssl_config_cache[cache_key]
        
        logger.info("Configurando conexión LDAP por primera vez")
        
        try:
            if settings.AD_USE_SSL:
                # Configuración SSL optimizada - intentar solo la mejor opción
                cert_path = self._find_certificate_path()
                server = self._create_ssl_server(cert_path)
                
                # Cachear la configuración exitosa
                _ssl_config_cache[cache_key] = server
                logger.info("Configuración SSL cacheada exitosamente")
                return server
            else:
                # Configuración sin SSL
                logger.warning("ADVERTENCIA: SSL deshabilitado - Conexión no segura")
                server = Server(
                    settings.AD_SERVER,
                    get_info=ALL,
                    port=389,
                    use_ssl=False,
                    connect_timeout=5  # Timeout de conexión de 5 segundos
                )
                _ssl_config_cache[cache_key] = server
                return server
                
        except Exception as e:
            logger.error(f"Error configurando servidor LDAP: {e}")
            # Fallback a conexión sin SSL
            server = Server(
                settings.AD_SERVER,
                get_info=ALL,
                port=389,
                use_ssl=False,
                connect_timeout=5  # Timeout de conexión de 5 segundos
            )
            _ssl_config_cache[cache_key] = server
            return server
    
    def _find_certificate_path(self):
        """Busca el certificado SSL en ubicaciones conocidas"""
        if settings.AD_SSL_CERT_PATH and os.path.exists(settings.AD_SSL_CERT_PATH):
            logger.info(f"Usando certificado configurado: {settings.AD_SSL_CERT_PATH}")
            return settings.AD_SSL_CERT_PATH
        
        # Buscar en ubicaciones específicas
        cert_paths = [
            '/mnt/c/Cursor/OneSite/backend/elite-clean-chain.pem',
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'elite-clean-chain.pem'),
            'elite-clean-chain.pem'
        ]
        
        for path in cert_paths:
            if os.path.exists(path):
                logger.info(f"Certificado encontrado en: {path}")
                return path
        
        logger.warning("No se encontró certificado SSL específico")
        return None
    
    def _create_ssl_server(self, cert_path):
        """Crea servidor SSL con configuración optimizada"""
        # Usar configuración SSL relajada directamente para evitar múltiples intentos
        # que causan lentitud
        # Usar SSL sin verificación estricta directamente (más confiable)
        try:
            tls_config = Tls(validate=ssl.CERT_NONE)
            server = Server(
                settings.AD_SERVER,
                get_info=ALL,
                port=settings.AD_PORT,
                use_ssl=True,
                tls=tls_config,
                connect_timeout=5  # Timeout de conexión de 5 segundos
            )
            logger.info("Configuración SSL sin verificación estricta para desarrollo")
            return server
        except Exception as e:
            logger.error(f"Error con SSL: {e}")
            # Fallback a conexión sin SSL
            try:
                server = Server(
                    settings.AD_SERVER,
                    get_info=ALL,
                    port=389,  # Puerto estándar LDAP
                    use_ssl=False,
                    connect_timeout=5
                )
                logger.warning("Fallback a conexión LDAP sin SSL")
                return server
            except Exception as e2:
                logger.error(f"Error con conexión sin SSL: {e2}")
                raise

    def authenticate(self, username: str, password: str, ip_address: str = "unknown", user_agent: str = None) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario contra el Directorio Activo
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            ip_address: Dirección IP del cliente
            user_agent: User-Agent del cliente
            
        Returns:
            Dict con la información del usuario si la autenticación es exitosa
            Dict con error específico si la autenticación falla
        """
        try:
            # Verificar si la cuenta está bloqueada
            if self.account_lockout.is_account_locked(username):
                self.secure_logger.log_login_attempt(username, False, ip_address, user_agent)
                logger.warning(f"Intento de login en cuenta bloqueada: {username}")
                return {
                    "error": "account_locked",
                    "message": "Cuenta bloqueada por múltiples intentos fallidos",
                    "username": username
                }
            
            # Formatear el nombre de usuario para LDAP
            user_dn = f"{username}@{settings.AD_DOMAIN}"
            logger.info(f"Intentando autenticar usuario: {username} desde IP: {ip_address}")
            
            # Crear conexión LDAP con timeouts optimizados
            conn = Connection(
                self.server,
                user=user_dn,
                password=password,
                authentication=SIMPLE,
                auto_bind=False,
                receive_timeout=5,  # Reducido de 10 a 5 segundos
                read_only=True,
                lazy=False,  # Conexión inmediata
                check_names=True,
                raise_exceptions=False  # Manejar errores manualmente
            )
            
            # Intentar hacer bind manualmente para capturar errores específicos
            try:
                if conn.bind():
                    self.secure_logger.log_login_attempt(username, True, ip_address, user_agent)
                    self.account_lockout.reset_failed_attempts(username)
                    logger.info("Autenticacion LDAP exitosa")
                    
                    # Buscar información del usuario
                    user_info = self._get_user_info(conn, username)
                    
                    if user_info:
                        return user_info
                    else:
                        logger.warning("Usuario no encontrado en el Directorio Activo")
                        self.secure_logger.log_login_attempt(username, False, ip_address, user_agent)
                        return {
                            "error": "user_not_found",
                            "message": "Usuario no encontrado en el Directorio Activo",
                            "username": username
                        }
                else:
                    logger.error("La autenticacion LDAP fallo")
                    self.secure_logger.log_login_attempt(username, False, ip_address, user_agent)
                    self.account_lockout.record_failed_attempt(username)
                    return {
                        "error": "invalid_credentials",
                        "message": "Credenciales incorrectas",
                        "username": username
                    }
            except Exception as bind_error:
                logger.error(f"Error durante el bind LDAP: {str(bind_error)}")
                self.secure_logger.log_login_attempt(username, False, ip_address, user_agent)
                self.account_lockout.record_failed_attempt(username)
                
                # Analizar el tipo de error
                error_message = str(bind_error).lower()
                
                if any(keyword in error_message for keyword in [
                    'invalid credentials', 'invalid_credentials', 'authentication failed',
                    'invalid username or password', 'wrong password', 'password incorrect',
                    'ldap.invalidCredentials', 'ldap_invalid_credentials', 'bind failed'
                ]):
                    return {
                        "error": "invalid_credentials",
                        "message": "Credenciales incorrectas",
                        "username": username
                    }
                else:
                    logger.error(f"Error LDAP detallado: {str(bind_error)}")
                    return {
                        "error": "ldap_error",
                        "message": f"Error de conexión con el Directorio Activo: {str(bind_error)[:100]}",
                        "username": username
                    }
                
        except Exception as e:
            logger.error(f"Error en la autenticacion LDAP: {str(e)}")
            self.secure_logger.log_login_attempt(username, False, ip_address, user_agent)
            self.account_lockout.record_failed_attempt(username)
            
            # Para errores de conexión más específicos
            return {
                "error": "ldap_error",
                "message": f"Error de conexión LDAP: {str(e)[:100]}",
                "username": username
            }
        finally:
            if 'conn' in locals():
                conn.unbind()

    def _get_user_info(self, conn: Connection, username: str) -> Optional[Dict[str, Any]]:
        """Obtiene información detallada del usuario desde AD"""
        try:
            # Buscar usuario en AD
            search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
            
            conn.search(
                search_base=self.search_base,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=[
                    'cn', 'mail', 'memberOf', 'displayName', 
                    'givenName', 'sn', 'department', 'title',
                    'manager', 'employeeID', 'userPrincipalName'
                ]
            )
            
            if conn.entries:
                user_entry = conn.entries[0]
                
                # Extraer grupos del usuario
                groups = self._extract_groups(user_entry.memberOf.values if hasattr(user_entry, 'memberOf') else [])
                
                # Mapear grupos AD a roles de OneSite
                roles = self._map_ad_groups_to_roles(groups)
                
                return {
                    "username": username,
                    "email": user_entry.mail.value if hasattr(user_entry, 'mail') else None,
                    "full_name": user_entry.displayName.value if hasattr(user_entry, 'displayName') else None,
                    "first_name": user_entry.givenName.value if hasattr(user_entry, 'givenName') else None,
                    "last_name": user_entry.sn.value if hasattr(user_entry, 'sn') else None,
                    "department": user_entry.department.value if hasattr(user_entry, 'department') else None,
                    "title": user_entry.title.value if hasattr(user_entry, 'title') else None,
                    "employee_id": user_entry.employeeID.value if hasattr(user_entry, 'employeeID') else None,
                    "ad_groups": groups,
                    "roles": roles,
                    "permissions": self._get_permissions_from_roles(roles)
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo información del usuario: {str(e)}")
            return None

    def _extract_groups(self, member_of: list) -> list:
        """Extrae nombres de grupos desde memberOf"""
        groups = []
        for group_dn in member_of:
            # Extraer CN del DN (ej: "CN=Operadores,OU=Groups,DC=ELITE,DC=local" -> "Operadores")
            if group_dn.startswith("CN="):
                group_name = group_dn.split(",")[0].replace("CN=", "")
                groups.append(group_name)
        return groups

    def _map_ad_groups_to_roles(self, ad_groups: list) -> list:
        """Mapea grupos de AD a roles de OneSite"""
        role_mapping = {
            "Operadores": "operadores",
            "Supervisores": "supervisores", 
            "Administradores": "administradores",
            "Gerentes": "gerentes",
            "Auditores": "auditores",
            "IT_Support": "soporte_tecnico"
        }
        
        roles = []
        for group in ad_groups:
            if group in role_mapping:
                roles.append(role_mapping[group])
        
        return roles

    def _get_permissions_from_roles(self, roles: list) -> list:
        """Obtiene permisos basados en roles"""
        permissions = {
            "operadores": ["trucks:read", "trucks:create"],
            "supervisores": ["trucks:read", "trucks:write", "trucks:delete", "reports:read"],
            "administradores": ["*"],  # Todos los permisos
            "gerentes": ["trucks:read", "trucks:write", "reports:read", "reports:write"],
            "auditores": ["trucks:read", "audit:read", "reports:read"],
            "soporte_tecnico": ["trucks:read", "system:read"]
        }
        
        user_permissions = []
        for role in roles:
            if role in permissions:
                if permissions[role] == ["*"]:
                    return ["*"]  # Administrador tiene todos los permisos
                user_permissions.extend(permissions[role])
        
        return list(set(user_permissions))  # Eliminar duplicados

# Instancia global del servicio de autenticación LDAP
ldap_auth = LDAPAuth() 