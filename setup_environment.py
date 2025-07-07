#!/usr/bin/env python3
"""
Script para configurar diferentes entornos de OneSite
"""

import os
import sys
import shutil

def setup_environment(environment):
    """Configura el entorno especificado"""
    
    print(f"🔧 Configurando entorno: {environment.upper()}")
    print("=" * 50)
    
    # Configuraciones por entorno
    configs = {
        "development": {
            "env_file": "backend/.env",
            "description": "Desarrollo local",
            "features": [
                "Logging detallado",
                "CORS amplio",
                "Rate limiting bajo",
                "Debug habilitado"
            ]
        },
        "staging": {
            "env_file": "backend/.env.staging",
            "description": "Pre-producción",
            "features": [
                "Logging moderado",
                "CORS restringido",
                "Rate limiting medio",
                "Debug limitado"
            ]
        },
        "production": {
            "env_file": "backend/.env.production",
            "description": "Producción",
            "features": [
                "Logging mínimo",
                "CORS estricto",
                "Rate limiting alto",
                "Debug deshabilitado"
            ]
        }
    }
    
    if environment not in configs:
        print(f"❌ Entorno '{environment}' no válido")
        print("Entornos disponibles: development, staging, production")
        return False
    
    config = configs[environment]
    
    print(f"📋 Descripción: {config['description']}")
    print(f"📁 Archivo: {config['env_file']}")
    print("\n🔧 Características:")
    for feature in config['features']:
        print(f"   ✅ {feature}")
    
    # Verificar si existe el archivo de configuración
    if not os.path.exists(config['env_file']):
        print(f"\n⚠️  El archivo {config['env_file']} no existe")
        print("¿Quieres crear la configuración para este entorno? (y/n): ", end="")
        response = input().strip().lower()
        
        if response in ['y', 'yes', 'sí', 'si']:
            return create_environment_config(environment)
        else:
            print("❌ Configuración cancelada")
            return False
    
    # Copiar configuración al .env principal
    try:
        shutil.copy2(config['env_file'], 'backend/.env')
        print(f"\n✅ Configuración de {environment} aplicada")
        print(f"📁 Copiado: {config['env_file']} → backend/.env")
        return True
    except Exception as e:
        print(f"❌ Error al copiar configuración: {str(e)}")
        return False

def create_environment_config(environment):
    """Crea una nueva configuración para el entorno especificado"""
    
    print(f"\n🔧 Creando configuración para {environment}...")
    
    if environment == "development":
        return create_development_config()
    elif environment == "staging":
        return create_staging_config()
    elif environment == "production":
        return create_production_config()
    else:
        print(f"❌ Entorno '{environment}' no soportado")
        return False

def create_development_config():
    """Crea configuración de desarrollo"""
    
    print("📝 Configurando entorno de DESARROLLO...")
    
    # Solicitar información básica
    print("\n🏠 BASE DE DATOS PRINCIPAL (OneSite):")
    db_server = input("Servidor [SATURNO13]: ").strip() or "SATURNO13"
    db_name = input("Base de datos [OnesiteDW]: ").strip() or "OnesiteDW"
    db_user = input("Usuario [data_analysis_admin]: ").strip() or "data_analysis_admin"
    db_password = input("Contraseña: ").strip()
    
    if not db_password:
        print("❌ La contraseña es obligatoria")
        return False
    
    # Crear contenido del archivo
    env_content = f"""# =============================================================================
# CONFIGURACIÓN DE DESARROLLO - OneSite
# =============================================================================

# =============================================================================
# CONFIGURACIÓN DE ENTORNO
# =============================================================================
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=true

# =============================================================================
# BASE DE DATOS PRINCIPAL (OneSite)
# =============================================================================
DB_SERVER={db_server}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}

# =============================================================================
# BASE DE DATOS SATURNO13 (TheEliteGroup)
# =============================================================================
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
SATURNO13_USER=data_analysis_admin
SATURNO13_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc
SATURNO13_SCHEMA=TheEliteGroup_Parameters

# =============================================================================
# BASE DE DATOS JUPITER12MIA (EFLOWER_Reports)
# =============================================================================
JUPITER12MIA_SERVER=JUPITER12MIA
JUPITER12MIA_DB=EFLOWER_Reports
JUPITER12MIA_USER=data_analysis_admin
JUPITER12MIA_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD JWT
# =============================================================================
SECRET_KEY=dev-super-secret-key-2024-elite-group-development
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
CORS_ORIGINS=["https://teg.1sitesoft.com", "http://localhost:4200", "http://127.0.0.1:4200"]
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
LOG_LEVEL=DEBUG
LOG_FILE=onesite.log
"""
    
    # Guardar archivo
    with open('backend/.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuración de desarrollo creada")
    return True

def create_staging_config():
    """Crea configuración de staging"""
    print("📝 Configurando entorno de STAGING...")
    print("⚠️  Esta funcionalidad requiere configuración manual")
    print("   Copia backend/env.production.example a backend/.env.staging")
    print("   y ajusta los valores según tu entorno de staging")
    return False

def create_production_config():
    """Crea configuración de producción"""
    print("📝 Configurando entorno de PRODUCCIÓN...")
    print("⚠️  Esta funcionalidad requiere configuración manual")
    print("   Copia backend/env.production.example a backend/.env.production")
    print("   y ajusta los valores según tu entorno de producción")
    return False

def show_current_environment():
    """Muestra el entorno actual"""
    try:
        from dotenv import load_dotenv
        load_dotenv('backend/.env')
        
        environment = os.getenv('ENVIRONMENT', 'no configurado')
        db_server = os.getenv('DB_SERVER', 'no configurado')
        db_name = os.getenv('DB_NAME', 'no configurado')
        
        print("🌍 ENTORNO ACTUAL")
        print("=" * 30)
        print(f"📋 Entorno: {environment}")
        print(f"📡 Servidor: {db_server}")
        print(f"🗄️  Base de datos: {db_name}")
        
    except Exception as e:
        print(f"❌ Error al leer configuración: {str(e)}")

if __name__ == "__main__":
    print("🔧 Gestor de Entornos - OneSite")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        environment = sys.argv[1].lower()
        setup_environment(environment)
    else:
        print("Uso: python setup_environment.py [development|staging|production]")
        print("\nOpciones:")
        print("  development  - Entorno de desarrollo local")
        print("  staging      - Entorno de pre-producción")
        print("  production   - Entorno de producción")
        print("\nEjemplo: python setup_environment.py development")
        
        print("\n" + "=" * 40)
        show_current_environment() 