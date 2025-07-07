#!/usr/bin/env python3
"""
Script para crear el archivo .env con la configuración de las tres bases de datos
"""

import os

def create_env_file():
    """Crea el archivo .env con la configuración de las tres bases de datos"""
    
    env_content = """# =============================================================================
# CONFIGURACIÓN DE BASES DE DATOS - MÚLTIPLES ENTORNOS
# =============================================================================

# =============================================================================
# CONFIGURACIÓN DE ENTORNO
# =============================================================================
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=true

# =============================================================================
# BASE DE DATOS PRINCIPAL (OneSite) - Para crear tablas, vistas, procedimientos
# =============================================================================
DB_SERVER=SATURNO13
DB_NAME=Onesite
DB_USER=data_analysis_admin
DB_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc

# =============================================================================
# BASE DE DATOS SATURNO13 (TheEliteGroup) - Para consultar datos existentes
# =============================================================================
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
SATURNO13_USER=data_analysis_admin
SATURNO13_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc
SATURNO13_SCHEMA=TheEliteGroup_Parameters

# =============================================================================
# BASE DE DATOS JUPITER12MIA (EFLOWER_Reports) - Para consultar datos
# =============================================================================
JUPITER12MIA_SERVER=JUPITER12MIA
JUPITER12MIA_DB=EFLOWER_Reports
JUPITER12MIA_USER=data_analysis_admin
JUPITER12MIA_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD JWT
# =============================================================================
SECRET_KEY=onesite-super-secret-key-2024-elite-group-very-long-and-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# =============================================================================
# CONFIGURACIÓN DE ACTIVE DIRECTORY
# =============================================================================
AD_SERVER=10.50.5.200
AD_PORT=636
AD_USE_SSL=true
AD_BASE_DN=DC=ELITE,DC=local
AD_DOMAIN=elite.local

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================
RATE_LIMIT_PER_MINUTE=5
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15

# =============================================================================
# CONFIGURACIÓN CORS
# =============================================================================
CORS_ORIGINS=["https://teg.1sitesoft.com", "http://localhost:4200"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["Authorization", "Content-Type", "X-Requested-With"]

# =============================================================================
# CONFIGURACIÓN DE REDIS
# =============================================================================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================
LOG_LEVEL=INFO
LOG_FILE=onesite.log
"""
    
    # Crear archivo .env en el backend
    env_file_path = os.path.join('backend', '.env')
    
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Archivo .env creado en: {env_file_path}")
    print("\n📋 CONFIGURACIÓN APLICADA:")
    print("=" * 50)
    print("🏠 BASE PRINCIPAL (OneSite):")
    print(f"   📡 Servidor: SATURNO13")
    print(f"   🗄️  Base de datos: Onesite")
    print(f"   👤 Usuario: data_analysis_admin")
    print()
    print("🪐 BASE SATURNO13 (AnalysisDW):")
    print(f"   📡 Servidor: SATURNO13")
    print(f"   🗄️  Base de datos: AnalysisDW")
    print(f"   👤 Usuario: data_analysis_admin")
    print(f"   📁 Esquema: TheEliteGroup_Parameters")
    print()
    print("🪐 BASE JUPITER12MIA (EFLOWER_Reports):")
    print(f"   📡 Servidor: JUPITER12MIA")
    print(f"   🗄️  Base de datos: EFLOWER_Reports")
    print(f"   👤 Usuario: data_analysis_admin")
    
    return True

if __name__ == "__main__":
    print("🔧 Creando archivo .env con configuración de tres bases de datos...")
    print("=" * 70)
    
    if create_env_file():
        print("\n✅ ¡Configuración completada!")
        print("\n📋 Próximos pasos:")
        print("  1. Ejecutar: python test_companies_connection.py")
        print("  2. Reiniciar el backend")
        print("  3. Verificar endpoints en Swagger")
    else:
        print("\n❌ Error al crear el archivo .env") 