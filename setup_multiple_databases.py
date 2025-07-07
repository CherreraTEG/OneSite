#!/usr/bin/env python3
"""
Script para configurar múltiples bases de datos de forma interactiva
"""

import os
import sys

def setup_multiple_databases():
    """Configura múltiples bases de datos de forma interactiva"""
    
    print("🔧 Configuración de Múltiples Bases de Datos")
    print("=" * 60)
    
    # Configuración de entorno
    print("\n📋 CONFIGURACIÓN DE ENTORNO")
    print("-" * 30)
    
    environment = input("Entorno (development/staging/production) [development]: ").strip() or "development"
    use_saturno13 = input("¿Usar tabla de empresas de SATURNO13? (y/n) [y]: ").strip().lower() or "y"
    use_saturno13_companies = "true" if use_saturno13 in ["y", "yes", "sí", "si"] else "false"
    
    # Base de datos principal (OneSite)
    print("\n🗄️  BASE DE DATOS PRINCIPAL (OneSite)")
    print("-" * 40)
    
    db_server = input("Servidor principal [localhost]: ").strip() or "localhost"
    db_name = input("Base de datos principal [onesite_db]: ").strip() or "onesite_db"
    db_user = input("Usuario principal [sa]: ").strip() or "sa"
    db_password = input("Contraseña principal: ").strip()
    
    # Base de datos SATURNO13
    print("\n🪐 BASE DE DATOS SATURNO13 (TheEliteGroup)")
    print("-" * 45)
    
    saturno13_server = input("Servidor SATURNO13 [SATURNO13]: ").strip() or "SATURNO13"
    saturno13_db = input("Base de datos SATURNO13 [AnalysisDW]: ").strip() or "AnalysisDW"
    saturno13_user = input("Usuario SATURNO13: ").strip()
    saturno13_password = input("Contraseña SATURNO13: ").strip()
    saturno13_schema = input("Esquema SATURNO13 [TheEliteGroup_Parameters]: ").strip() or "TheEliteGroup_Parameters"
    
    # Otras configuraciones
    print("\n🔐 CONFIGURACIÓN DE SEGURIDAD")
    print("-" * 30)
    
    secret_key = input("Secret Key JWT [tu-super-secret-key-aqui-muy-larga-y-compleja-al-menos-32-caracteres]: ").strip() or "tu-super-secret-key-aqui-muy-larga-y-compleja-al-menos-32-caracteres"
    
    # Crear archivo .env
    env_content = f"""# =============================================================================
# CONFIGURACIÓN DE BASES DE DATOS - MÚLTIPLES ENTORNOS
# =============================================================================

# =============================================================================
# CONFIGURACIÓN DE ENTORNO
# =============================================================================
ENVIRONMENT={environment}
USE_SATURNO13_COMPANIES={use_saturno13_companies}

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
SATURNO13_SERVER={saturno13_server}
SATURNO13_DB={saturno13_db}
SATURNO13_USER={saturno13_user}
SATURNO13_PASSWORD={saturno13_password}
SATURNO13_SCHEMA={saturno13_schema}

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD JWT
# =============================================================================
SECRET_KEY={secret_key}
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
    
    # Guardar archivo .env
    env_file_path = os.path.join('backend', '.env')
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Archivo .env creado en: {env_file_path}")
    
    # Mostrar resumen
    print("\n📋 RESUMEN DE CONFIGURACIÓN")
    print("=" * 40)
    print(f"🌍 Entorno: {environment}")
    print(f"🪐 Usar SATURNO13 para empresas: {use_saturno13_companies}")
    print(f"📡 Servidor principal: {db_server}")
    print(f"🗄️  Base principal: {db_name}")
    print(f"📡 Servidor SATURNO13: {saturno13_server}")
    print(f"🗄️  Base SATURNO13: {saturno13_db}")
    print(f"📁 Esquema SATURNO13: {saturno13_schema}")
    
    return True

def test_multiple_connections():
    """Prueba las conexiones a múltiples bases de datos"""
    try:
        # Cargar variables de entorno
        from dotenv import load_dotenv
        load_dotenv(os.path.join('backend', '.env'))
        
        # Importar y probar conexiones
        sys.path.append('backend')
        from app.db.databases import db_manager
        
        print("\n🔍 Probando conexiones a múltiples bases de datos...")
        print("=" * 60)
        
        results = db_manager.test_connections()
        
        print("\n📊 RESULTADOS DE PRUEBAS")
        print("=" * 30)
        
        all_success = True
        for db_name, result in results.items():
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"{status_icon} {db_name}: {result['message']}")
            if result["status"] != "success":
                all_success = False
        
        if all_success:
            print("\n🎉 ¡Todas las conexiones exitosas!")
            print("\n📋 Próximos pasos:")
            print("  1. Reiniciar el backend")
            print("  2. Verificar endpoints en Swagger")
            print("  3. Probar el selector de empresas")
        else:
            print("\n⚠️  Algunas conexiones fallaron")
            print("  Verifique las credenciales y configuraciones")
        
        return all_success
        
    except Exception as e:
        print(f"❌ Error al probar conexiones: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Configuración de Múltiples Bases de Datos")
    print("=" * 60)
    
    # Configurar bases de datos
    if setup_multiple_databases():
        print("\n✅ Configuración completada")
        
        # Probar conexiones
        if test_multiple_connections():
            print("\n🚀 ¡Configuración lista para usar!")
        else:
            print("\n❌ Error en las pruebas de conexión")
    else:
        print("\n❌ Error en la configuración") 