#!/usr/bin/env python3
"""
Script para verificar la estructura de la base de datos OnesiteDW
y determinar si necesitamos crear esquemas o tablas para OneSite
"""

import pymssql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_database_structure():
    """Verifica la estructura actual de la base de datos OnesiteDW"""
    
    try:
        # Conectar usando las credenciales proporcionadas
        conn = pymssql.connect(
            server='SATURNO13',
            database='OnesiteDW',
            user='data_analysis_admin',
            password='Hg1y3m9VFJsNrzjw8brjbc'
        )
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO ESTRUCTURA DE BASE DE DATOS OnesiteDW")
        print("=" * 60)
        
        # 1. Verificar esquemas existentes
        print("\n📁 ESQUEMAS EXISTENTES:")
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('db_owner', 'db_accessadmin', 'db_securityadmin', 
                                     'db_ddladmin', 'db_backupoperator', 'db_datareader', 
                                     'db_datawriter', 'db_denydatareader', 'db_denydatawriter',
                                     'sys', 'information_schema', 'guest')
            ORDER BY schema_name
        """)
        schemas = cursor.fetchall()
        for schema in schemas:
            print(f"  - {schema[0]}")
        
        # 2. Verificar si existe tabla user en algún esquema
        print("\n👤 BUSCANDO TABLA 'user' EN TODOS LOS ESQUEMAS:")
        cursor.execute("""
            SELECT 
                table_schema,
                table_name,
                table_type
            FROM information_schema.tables 
            WHERE table_name LIKE '%user%' OR table_name LIKE '%User%'
            ORDER BY table_schema, table_name
        """)
        user_tables = cursor.fetchall()
        if user_tables:
            for table in user_tables:
                print(f"  - {table[0]}.{table[1]} ({table[2]})")
        else:
            print("  ❌ No se encontraron tablas relacionadas con 'user'")
        
        # 3. Verificar tablas existentes en esquema dbo (principal)
        print("\n📋 TABLAS EN ESQUEMA dbo:")
        cursor.execute("""
            SELECT table_name, table_type
            FROM information_schema.tables 
            WHERE table_schema = 'dbo'
            ORDER BY table_name
        """)
        dbo_tables = cursor.fetchall()
        for table in dbo_tables:
            print(f"  - {table[0]} ({table[1]})")
        
        # 4. Verificar si existe esquema específico para OneSite
        print("\n🏢 VERIFICANDO ESQUEMA OneSite:")
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name IN ('OneSite', 'onesite', 'ONESITE')
        """)
        onesite_schema = cursor.fetchone()
        if onesite_schema:
            print(f"  ✅ Esquema encontrado: {onesite_schema[0]}")
            
            # Verificar tablas en esquema OneSite
            cursor.execute("""
                SELECT table_name, table_type
                FROM information_schema.tables 
                WHERE table_schema = ?
                ORDER BY table_name
            """, (onesite_schema[0],))
            onesite_tables = cursor.fetchall()
            print(f"  📋 Tablas en {onesite_schema[0]}:")
            for table in onesite_tables:
                print(f"    - {table[0]} ({table[1]})")
        else:
            print("  ❌ No existe esquema específico para OneSite")
        
        # 5. Verificar permisos del usuario actual
        print("\n🔐 PERMISOS DEL USUARIO ACTUAL:")
        cursor.execute("""
            SELECT 
                p.permission_name,
                p.state_desc,
                s.name as schema_name
            FROM sys.database_permissions p
            LEFT JOIN sys.schemas s ON p.major_id = s.schema_id
            JOIN sys.database_principals dp ON p.grantee_principal_id = dp.principal_id
            WHERE dp.name = USER_NAME()
            ORDER BY s.name, p.permission_name
        """)
        permissions = cursor.fetchall()
        for perm in permissions:
            schema_name = perm[2] if perm[2] else "DATABASE"
            print(f"  - {perm[0]} ({perm[1]}) en {schema_name}")
        
        # 6. Sugerencias de configuración
        print("\n💡 RECOMENDACIONES:")
        print("=" * 60)
        
        if not onesite_schema:
            print("1. ✨ Crear esquema 'OneSite' para organizar las tablas de la aplicación")
        
        if not user_tables:
            print("2. 👤 Crear tabla 'user' en el esquema OneSite")
            print("3. 🔗 Crear tabla 'role' para sistema de roles")
            print("4. 🔗 Crear tabla 'user_role' para relación many-to-many")
            print("5. 🏢 Crear tabla 'user_company_permission' para permisos por empresa")
        
        print("6. 🔄 Configurar SQLAlchemy para usar el esquema correcto")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return False

if __name__ == "__main__":
    check_database_structure()