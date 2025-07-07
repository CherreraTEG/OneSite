#!/usr/bin/env python3
"""
Script de prueba para las tres bases de datos con información corregida
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

def test_analysisdw_companies():
    """Prueba específicamente la tabla de empresas en AnalysisDW"""
    try:
        # Configuración de AnalysisDW
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
            
            # Obtener estructura de la tabla
            columns_query = text(f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{schema}' 
                AND TABLE_NAME = 'Companies'
                ORDER BY ORDINAL_POSITION
            """)
            columns_result = connection.execute(columns_query)
            columns = columns_result.fetchall()
            
            print("📋 Estructura de la tabla Companies:")
            for column in columns:
                print(f"   {column[0]}: {column[1]} ({'NULL' if column[2] == 'YES' else 'NOT NULL'})")
            
            # Obtener algunos ejemplos (usando la primera columna como ID)
            if count > 0 and columns:
                first_column = columns[0][0]  # Usar la primera columna como orden
                sample_query = text(f"""
                    SELECT TOP 3 * 
                    FROM [{schema}].[Companies]
                    ORDER BY [{first_column}]
                """)
                sample_result = connection.execute(sample_query)
                samples = sample_result.fetchall()
                
                print(f"\n📝 Ejemplos de empresas (usando {first_column}):")
                for sample in samples:
                    print(f"   {sample}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al probar tabla de empresas: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Probando conexiones a las tres bases de datos (CORREGIDO)...")
    print("=" * 70)
    
    # Configuración corregida de las tres bases de datos
    databases = [
        {
            "server": "SATURNO13",
            "database": "OnesiteDW",
            "user": "data_analysis_admin",
            "password": "Hg1y3m9VFJsNrzjw8brjbc",
            "name": "BASE PRINCIPAL (OnesiteDW)"
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
    
    companies_success = test_analysisdw_companies()
    
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