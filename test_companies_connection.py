#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a la tabla de empresas existente
en el servidor SATURNO13, base de datos AnalysisDW, esquema TheEliteGroup_Parameters
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from app.core.config import settings

def test_connection():
    """Prueba la conexión a la base de datos y la tabla de empresas"""
    try:
        # Crear conexión
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            print("✅ Conexión a la base de datos exitosa")
            
            # Verificar que existe el esquema
            schema_query = text("""
                SELECT SCHEMA_NAME 
                FROM INFORMATION_SCHEMA.SCHEMATA 
                WHERE SCHEMA_NAME = 'TheEliteGroup_Parameters'
            """)
            schema_result = connection.execute(schema_query)
            schema_exists = schema_result.fetchone()
            
            if not schema_exists:
                print("❌ El esquema 'TheEliteGroup_Parameters' no existe")
                return False
            
            print("✅ Esquema 'TheEliteGroup_Parameters' encontrado")
            
            # Verificar que existe la tabla Companies
            table_query = text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'TheEliteGroup_Parameters' 
                AND TABLE_NAME = 'Companies'
            """)
            table_result = connection.execute(table_query)
            table_exists = table_result.fetchone()
            
            if not table_exists:
                print("❌ La tabla 'Companies' no existe en el esquema 'TheEliteGroup_Parameters'")
                return False
            
            print("✅ Tabla 'Companies' encontrada")
            
            # Obtener estructura de la tabla
            columns_query = text("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'TheEliteGroup_Parameters' 
                AND TABLE_NAME = 'Companies'
                ORDER BY ORDINAL_POSITION
            """)
            columns_result = connection.execute(columns_query)
            columns = columns_result.fetchall()
            
            print("\n📋 Estructura de la tabla Companies:")
            print("-" * 60)
            for column in columns:
                print(f"  {column[0]}: {column[1]} ({'NULL' if column[2] == 'YES' else 'NOT NULL'})")
            
            # Contar registros
            count_query = text("SELECT COUNT(*) FROM [TheEliteGroup_Parameters].[Companies]")
            count_result = connection.execute(count_query)
            count = count_result.fetchone()[0]
            
            print(f"\n📊 Total de empresas en la tabla: {count}")
            
            # Obtener algunos registros de ejemplo
            if count > 0:
                sample_query = text("""
                    SELECT TOP 5 * 
                    FROM [TheEliteGroup_Parameters].[Companies]
                    ORDER BY id
                """)
                sample_result = connection.execute(sample_query)
                samples = sample_result.fetchall()
                
                print("\n📝 Ejemplos de empresas:")
                print("-" * 60)
                for sample in samples:
                    print(f"  ID: {sample[0]}, Nombre: {sample[1]}, Código: {sample[2]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_model_connection():
    """Prueba la conexión usando el modelo SQLAlchemy"""
    try:
        from app.models.company import Company
        from app.db.base import SessionLocal
        
        db = SessionLocal()
        
        # Intentar obtener todas las empresas
        companies = db.query(Company).all()
        
        print(f"\n✅ Modelo SQLAlchemy funcionando correctamente")
        print(f"📊 Empresas obtenidas con el modelo: {len(companies)}")
        
        if companies:
            print("\n📝 Primeras empresas del modelo:")
            print("-" * 60)
            for company in companies[:3]:
                print(f"  ID: {company.id}, Nombre: {company.name}, Código: {company.code}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error con el modelo SQLAlchemy: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Probando conexión a la tabla de empresas existente...")
    print("=" * 70)
    
    # Configuración actual
    print(f"📡 Servidor: {settings.DB_SERVER}")
    print(f"🗄️  Base de datos: {settings.DB_NAME}")
    print(f"👤 Usuario: {settings.DB_USER}")
    print(f"🔗 URL de conexión: {settings.DATABASE_URL}")
    print("-" * 70)
    
    # Probar conexión básica
    if test_connection():
        print("\n✅ Conexión básica exitosa")
        
        # Probar modelo SQLAlchemy
        if test_model_connection():
            print("\n🎉 ¡Todo funcionando correctamente!")
            print("\n📋 Resumen:")
            print("  ✅ Conexión a la base de datos")
            print("  ✅ Esquema TheEliteGroup_Parameters")
            print("  ✅ Tabla Companies")
            print("  ✅ Modelo SQLAlchemy")
            print("\n🚀 El selector de empresas está listo para usar")
        else:
            print("\n❌ Error con el modelo SQLAlchemy")
    else:
        print("\n❌ Error en la conexión básica") 