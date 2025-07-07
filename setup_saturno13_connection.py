#!/usr/bin/env python3
"""
Script para configurar la conexión al servidor SATURNO13
"""

import os
import sys

def setup_saturno13_env():
    """Configura las variables de entorno para SATURNO13"""
    
    # Configuración para SATURNO13
    env_config = {
        'DB_SERVER': 'SATURNO13',
        'DB_NAME': 'AnalysisDW',
        'DB_USER': input('Ingrese el usuario de la base de datos: '),
        'DB_PASSWORD': input('Ingrese la contraseña de la base de datos: '),
        'SECRET_KEY': 'tu-super-secret-key-aqui-muy-larga-y-compleja-al-menos-32-caracteres',
        'ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '60',
        'AD_SERVER': '10.50.5.200',
        'AD_PORT': '636',
        'AD_USE_SSL': 'true',
        'AD_BASE_DN': 'DC=ELITE,DC=local',
        'AD_DOMAIN': 'elite.local',
        'RATE_LIMIT_PER_MINUTE': '5',
        'MAX_LOGIN_ATTEMPTS': '5',
        'ACCOUNT_LOCKOUT_MINUTES': '15',
        'CORS_ORIGINS': '["https://teg.1sitesoft.com", "http://localhost:4200"]',
        'CORS_CREDENTIALS': 'true',
        'CORS_METHODS': '["GET", "POST", "PUT", "DELETE"]',
        'CORS_HEADERS': '["Authorization", "Content-Type", "X-Requested-With"]',
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': '6379',
        'REDIS_DB': '0',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'onesite.log'
    }
    
    # Crear archivo .env en el backend
    env_file_path = os.path.join('backend', '.env')
    
    with open(env_file_path, 'w') as f:
        for key, value in env_config.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ Archivo .env creado en: {env_file_path}")
    print("📋 Configuración aplicada:")
    print(f"  📡 Servidor: {env_config['DB_SERVER']}")
    print(f"  🗄️  Base de datos: {env_config['DB_NAME']}")
    print(f"  👤 Usuario: {env_config['DB_USER']}")
    
    return True

def test_connection_with_env():
    """Prueba la conexión después de configurar las variables de entorno"""
    try:
        # Cargar las variables de entorno
        from dotenv import load_dotenv
        load_dotenv(os.path.join('backend', '.env'))
        
        # Importar y probar la conexión
        sys.path.append('backend')
        from app.core.config import settings
        
        print(f"\n🔍 Probando conexión con nueva configuración...")
        print(f"📡 Servidor: {settings.DB_SERVER}")
        print(f"🗄️  Base de datos: {settings.DB_NAME}")
        print(f"👤 Usuario: {settings.DB_USER}")
        print(f"🔗 URL de conexión: {settings.DATABASE_URL}")
        
        # Probar conexión básica
        from sqlalchemy import create_engine, text
        
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            print("✅ Conexión exitosa a SATURNO13")
            
            # Verificar esquema y tabla
            schema_query = text("""
                SELECT SCHEMA_NAME 
                FROM INFORMATION_SCHEMA.SCHEMATA 
                WHERE SCHEMA_NAME = 'TheEliteGroup_Parameters'
            """)
            schema_result = connection.execute(schema_query)
            schema_exists = schema_result.fetchone()
            
            if schema_exists:
                print("✅ Esquema 'TheEliteGroup_Parameters' encontrado")
                
                # Verificar tabla Companies
                table_query = text("""
                    SELECT COUNT(*) 
                    FROM [TheEliteGroup_Parameters].[Companies]
                """)
                count_result = connection.execute(table_query)
                count = count_result.fetchone()[0]
                
                print(f"✅ Tabla 'Companies' encontrada con {count} registros")
                return True
            else:
                print("❌ Esquema 'TheEliteGroup_Parameters' no encontrado")
                return False
                
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Configurando conexión a SATURNO13...")
    print("=" * 50)
    
    # Configurar variables de entorno
    if setup_saturno13_env():
        print("\n✅ Configuración completada")
        
        # Probar conexión
        if test_connection_with_env():
            print("\n🎉 ¡Configuración exitosa!")
            print("\n📋 Próximos pasos:")
            print("  1. Reiniciar el backend")
            print("  2. Ejecutar: python test_companies_connection.py")
            print("  3. Verificar endpoints en Swagger")
        else:
            print("\n❌ Error en la conexión")
            print("  Verifique las credenciales de la base de datos")
    else:
        print("\n❌ Error en la configuración") 