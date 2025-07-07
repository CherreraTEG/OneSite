#!/usr/bin/env python3
"""
Script de prueba para las tres bases de datos
"""

from sqlalchemy import create_engine, text

def test_database_connection(server, database, user, password, name):
    """Prueba la conexión a una base de datos específica"""
    try:
        # Crear URL de conexión
        connection_url = f"mssql+pymssql://{user}:{password}@{server}/{database}"
        
        # Crear engine
        engine = create_engine(connection_url)
        
        # Probar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            print(f"✅ {name}: Conexión exitosa")
            return True
            
    except Exception as e:
        print(f"❌ {name}: Error de conexión - {str(e)}")
        return False

def test_saturno13_companies():
    """Prueba específicamente la tabla de empresas en SATURNO13"""
    try:
        # Configuración de SATURNO13
        server = "SATURNO13"
        database = "AnalysisDW"
        user = "data_analysis_admin"
        password = "Hg1y3m9VFJsNrzjw8brjbc"
        schema = "TheEliteGroup_Parameters"
        
        # Crear URL de conexión
        connection_url = f"mssql+pymssql://{user}:{password}@{server}/{database}"
        
        # Crear engine
        engine = create_engine(connection_url)
        
        with engine.connect() as connection:
            # Verificar esquema
            schema_query = text(f"""
                SELECT SCHEMA_NAME 
                FROM INFORMATION_SCHEMA.SCHEMATA 
                WHERE SCHEMA_NAME = '{schema}'
            """)
            schema_result = connection.execute(schema_query)
            schema_exists = schema_result.fetchone()
            
            if not schema_exists:
                print(f"❌ Esquema '{schema}' no encontrado en {database}")
                return False
            
            print(f"✅ Esquema '{schema}' encontrado")
            
            # Verificar tabla Companies
            table_query = text(f"""
                SELECT COUNT(*) 
                FROM [{schema}].[Companies]
            """)
            count_result = connection.execute(table_query)
            count = count_result.fetchone()[0]
            
            print(f"✅ Tabla 'Companies' encontrada con {count} registros")
            
            # Obtener algunos ejemplos
            if count > 0:
                sample_query = text(f"""
                    SELECT TOP 3 id, name, code 
                    FROM [{schema}].[Companies]
                    ORDER BY id
                """)
                sample_result = connection.execute(sample_query)
                samples = sample_result.fetchall()
                
                print("📝 Ejemplos de empresas:")
                for sample in samples:
                    print(f"   ID: {sample[0]}, Nombre: {sample[1]}, Código: {sample[2]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al probar tabla de empresas: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Probando conexiones a las tres bases de datos...")
    print("=" * 70)
    
    # Configuración de las tres bases de datos
    databases = [
        {
            "server": "SATURNO13",
            "database": "Onesite",
            "user": "data_analysis_admin",
            "password": "Hg1y3m9VFJsNrzjw8brjbc",
            "name": "BASE PRINCIPAL (OneSite)"
        },
        {
            "server": "SATURNO13",
            "database": "AnalysisDW",
            "user": "data_analysis_admin",
            "password": "Hg1y3m9VFJsNrzjw8brjbc",
            "name": "SATURNO13 (AnalysisDW)"
        },
        {
            "server": "JUPITER12MIA",
            "database": "EFLOWER_Reports",
            "user": "data_analysis_admin",
            "password": "Hg1y3m9VFJsNrzjw8brjbc",
            "name": "JUPITER12MIA (EFLOWER_Reports)"
        }
    ]
    
    # Probar conexiones básicas
    print("\n📡 PRUEBAS DE CONEXIÓN BÁSICA")
    print("-" * 40)
    
    all_success = True
    for db in databases:
        success = test_database_connection(
            db["server"], 
            db["database"], 
            db["user"], 
            db["password"], 
            db["name"]
        )
        if not success:
            all_success = False
    
    # Probar tabla de empresas específicamente
    print("\n🏢 PRUEBA ESPECÍFICA DE TABLA DE EMPRESAS")
    print("-" * 45)
    
    companies_success = test_saturno13_companies()
    
    # Resumen final
    print("\n📊 RESUMEN FINAL")
    print("=" * 30)
    
    if all_success and companies_success:
        print("🎉 ¡Todas las conexiones exitosas!")
        print("\n📋 Próximos pasos:")
        print("  1. Reiniciar el backend")
        print("  2. Verificar endpoints en Swagger")
        print("  3. Probar el selector de empresas")
    else:
        print("⚠️  Algunas conexiones fallaron")
        if not all_success:
            print("  - Verificar conectividad de red")
            print("  - Comprobar credenciales")
        if not companies_success:
            print("  - Verificar que la tabla Companies existe")
            print("  - Comprobar el esquema TheEliteGroup_Parameters") 