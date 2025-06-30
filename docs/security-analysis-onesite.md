# Análisis de Seguridad - OneSite

## 📋 Resumen Ejecutivo

Este documento presenta un análisis exhaustivo de la seguridad actual de OneSite y proporciona un plan de implementación para mejorar la autenticación por Directorio Activo con las mejores prácticas de seguridad.

## 🔍 Estado Actual del Sistema

### ✅ **Fortalezas Identificadas**
- Autenticación LDAP contra Directorio Activo implementada
- Uso de JWT para tokens de sesión
- Configuración de CORS básica
- Variables de entorno para datos sensibles
- Logging de autenticación

### ⚠️ **Vulnerabilidades Críticas**

#### **1. Configuración CORS Insegura**
```python
# PROBLEMA: CORS demasiado permisivo
allow_origins=["*"]  # ❌ Permite cualquier origen
allow_credentials=False
allow_methods=["*"]  # ❌ Permite todos los métodos
allow_headers=["*"]  # ❌ Permite todos los headers
```

#### **2. Conexión LDAP sin SSL/TLS**
```python
# PROBLEMA: Conexión no encriptada
self.server = Server(
    "10.50.5.200",
    port=389,  # ❌ Puerto no SSL
    use_ssl=False  # ❌ Sin encriptación
)
```

#### **3. Logging de Información Sensible**
```python
# PROBLEMA: Logs de debug pueden exponer información
logging.basicConfig(level=logging.DEBUG)  # ❌ Nivel muy detallado
logger.info(f"Intentando autenticar usuario: {user_dn}")  # ❌ Log de credenciales
```

#### **4. Falta de Rate Limiting**
```python
# PROBLEMA: No hay protección contra ataques de fuerza bruta
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # ❌ Sin rate limiting
```

#### **5. Validación de Entrada Insuficiente**
```python
# PROBLEMA: Validación básica
username: ['', [Validators.required]]  # ❌ Sin validación de formato
password: ['', [Validators.required, Validators.minLength(6)]]  # ❌ Mínimo muy bajo
```

#### **6. Falta de Headers de Seguridad**
```python
# PROBLEMA: No hay headers de seguridad HTTP
# ❌ Falta X-Frame-Options, X-Content-Type-Options, etc.
```

## 🛡️ Plan de Mejoras de Seguridad

### **Fase 1: Configuración de Seguridad Crítica**

#### **1.1 Configuración CORS Segura**
```python
# Configuración recomendada
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://teg.1sitesoft.com", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["X-Total-Count"],
    max_age=3600
)
```

#### **1.2 Headers de Seguridad HTTP**
```python
# Middleware de seguridad
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Headers de seguridad
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

#### **1.3 Configuración LDAP Segura**
```python
# Conexión SSL/TLS
import ssl
from ldap3 import Tls

tls_configuration = Tls(validate=ssl.CERT_REQUIRED)
self.server = Server(
    "10.50.5.200",
    port=636,  # Puerto SSL
    use_ssl=True,
    tls=tls_configuration
)
```

### **Fase 2: Implementación de Rate Limiting**

#### **2.1 Rate Limiting con Redis**
```python
# Dependencias
# pip install slowapi redis

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis

# Configuración
limiter = Limiter(key_func=get_remote_address)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Endpoint con rate limiting
@router.post("/login")
@limiter.limit("5/minute")  # 5 intentos por minuto
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    # Lógica de autenticación
```

#### **2.2 Bloqueo de Cuentas**
```python
class AccountLockout:
    def __init__(self):
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutos
    
    def is_account_locked(self, username: str) -> bool:
        lock_key = f"lockout:{username}"
        return redis_client.exists(lock_key)
    
    def record_failed_attempt(self, username: str):
        attempt_key = f"attempts:{username}"
        attempts = redis_client.incr(attempt_key)
        
        if attempts >= self.max_attempts:
            lock_key = f"lockout:{username}"
            redis_client.setex(lock_key, self.lockout_duration, "locked")
            redis_client.delete(attempt_key)
```

### **Fase 3: Logging Seguro**

#### **3.1 Configuración de Logging**
```python
import logging
from datetime import datetime

# Configuración segura
logging.basicConfig(
    level=logging.INFO,  # Cambiar de DEBUG a INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('onesite.log'),
        logging.StreamHandler()
    ]
)

class SecureLogger:
    def log_login_attempt(self, username: str, success: bool, ip_address: str):
        status = "SUCCESS" if success else "FAILED"
        logger.info(
            f"Login attempt - User: {username}, Status: {status}, "
            f"IP: {ip_address}, Timestamp: {datetime.utcnow()}"
        )
```

### **Fase 4: Validación de Entrada**

#### **4.1 Validación de Usuario**
```python
from pydantic import BaseModel, validator
import re

class LoginCredentials(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9._-]{3,50}$', v):
            raise ValueError('Username inválido')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Contraseña debe tener al menos 8 caracteres')
        return v
```

### **Fase 5: Gestión de Sesiones**

#### **5.1 Blacklist de Tokens**
```python
class TokenBlacklist:
    def add_to_blacklist(self, token: str, expires_at: datetime):
        redis_client.setex(
            f"blacklist:{token}",
            int((expires_at - datetime.utcnow()).total_seconds()),
            "blacklisted"
        )
    
    def is_blacklisted(self, token: str) -> bool:
        return redis_client.exists(f"blacklist:{token}")
```

## 🔧 Implementación Recomendada

### **1. Configuración de Variables de Entorno**
```bash
# .env
# Configuración de seguridad
SECRET_KEY=tu-super-secret-key-aqui-muy-larga-y-compleja
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Configuración LDAP segura
AD_SERVER=10.50.5.200
AD_PORT=636
AD_USE_SSL=true
AD_BASE_DN=DC=ELITE,DC=local
AD_DOMAIN=elite.local

# Configuración de seguridad
RATE_LIMIT_PER_MINUTE=5
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15

# Configuración CORS
CORS_ORIGINS=["https://teg.1sitesoft.com", "http://localhost:4200"]
CORS_CREDENTIALS=true

# Redis para rate limiting
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### **2. Estructura de Base de Datos para Auditoría**
```sql
-- Tabla de auditoría de autenticación
CREATE TABLE auth_audit_log (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    event_type VARCHAR(20) NOT NULL, -- LOGIN, LOGOUT, FAILED_LOGIN
    success BIT NOT NULL,
    timestamp DATETIME2 DEFAULT GETDATE(),
    details NVARCHAR(MAX)
);

-- Tabla de sesiones activas
CREATE TABLE active_sessions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    expires_at DATETIME2 NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_active BIT DEFAULT 1
);

-- Índices para rendimiento
CREATE INDEX IX_auth_audit_log_username ON auth_audit_log(username);
CREATE INDEX IX_auth_audit_log_timestamp ON auth_audit_log(timestamp);
CREATE INDEX IX_active_sessions_token ON active_sessions(session_token);
CREATE INDEX IX_active_sessions_user_id ON active_sessions(user_id);
```

### **3. Endpoints de Seguridad**
```python
# Endpoints adicionales de seguridad
@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout seguro con invalidación de token"""
    pass

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Obtiene información del usuario actual"""
    pass

@router.get("/sessions")
async def get_active_sessions(current_user: dict = Depends(get_current_user)):
    """Obtiene sesiones activas del usuario"""
    pass

@router.delete("/sessions/{session_id}")
async def terminate_session(session_id: str, current_user: dict = Depends(get_current_user)):
    """Termina una sesión específica"""
    pass
```

## 📊 Métricas de Seguridad

### **KPIs a Monitorear**
- Intentos de login fallidos por hora
- Tiempo promedio de respuesta del login
- Número de cuentas bloqueadas
- Intentos de acceso desde IPs sospechosas
- Tiempo de vida promedio de las sesiones
- Tasa de éxito de autenticación

### **Alertas Recomendadas**
- Más de 10 intentos fallidos en 5 minutos
- Login desde nueva ubicación geográfica
- Múltiples sesiones simultáneas
- Intentos de acceso fuera del horario laboral
- Errores de conexión LDAP frecuentes

## 🧪 Testing de Seguridad

### **Tests Automatizados**
```python
def test_rate_limiting():
    """Test de rate limiting"""
    pass

def test_account_lockout():
    """Test de bloqueo de cuentas"""
    pass

def test_ldap_connection():
    """Test de conexión LDAP"""
    pass

def test_jwt_validation():
    """Test de validación JWT"""
    pass

def test_cors_configuration():
    """Test de configuración CORS"""
    pass
```

## 📚 Referencias y Estándares

- **OWASP Top 10**: Aplicación de mejores prácticas
- **NIST Cybersecurity Framework**: Estándares de seguridad
- **ISO 27001**: Gestión de seguridad de la información
- **GDPR**: Protección de datos personales
- **Microsoft Security Baseline**: Configuración segura de AD

---

**Documento creado**: 2024-01-15
**Versión**: 1.0
**Autor**: Sistema de Análisis de Seguridad OneSite 