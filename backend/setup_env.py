#!/usr/bin/env python3
"""
Script para configurar automáticamente las variables de entorno de OneSite
"""

import os
import shutil

def setup_environment():
    """Configura las variables de entorno para OneSite"""
    
    # Verificar si existe env.example
    if not os.path.exists('env.example'):
        print("❌ Error: No se encontró env.example")
        return False
    
    # Copiar env.example a .env si no existe
    if not os.path.exists('.env'):
        shutil.copy('env.example', '.env')
        print("✅ Archivo .env creado desde env.example")
    
    # Configurar variables específicas para Elite Flower
    env_content = """# Configuración de la base de datos SQL Server
DB_SERVER=SATURNO13
DB_NAME=OneSiteDW
DB_USER=Mtadm
DB_PASSWORD=CIOelite0630!!

# Configuración de seguridad JWT
SECRET_KEY=OneSite-Super-Secret-Key-2024-Elite-Flower-Enterprise-Grade-Security
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Configuración de Active Directory
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
CORS_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS=["Authorization", "Content-Type", "X-Requested-With", "Cache-Control", "Pragma", "Expires"]

# Configuración de Redis para rate limiting
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Configuración de logging
LOG_LEVEL=INFO
LOG_FILE=onesite.log
"""
    
    # Escribir el contenido al archivo .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Variables de entorno configuradas para OneSite")
    print("📋 Configuración aplicada:")
    print("   - Servidor SQL Server: SATURNO13")
    print("   - Base de datos: OneSiteDW")
    print("   - Usuario: Mtadm")
    print("   - Directorio Activo: elite.local")
    print("   - Rate limiting: 5 intentos/minuto")
    print("   - Bloqueo de cuenta: 15 minutos")
    print("   - CORS: teg.1sitesoft.com y localhost:4200")
    
    return True

if __name__ == "__main__":
    print("🔧 Configurando variables de entorno para OneSite...")
    if setup_environment():
        print("✅ Configuración completada exitosamente")
    else:
        print("❌ Error en la configuración") 