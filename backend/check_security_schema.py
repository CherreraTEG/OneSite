#!/usr/bin/env python3
"""
Script para verificar qué contiene el esquema 'security' en OnesiteDW
"""

import pymssql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_security_schema():
    """Verifica el contenido del esquema security"""
    
    try:
        # Conectar usando las credenciales proporcionadas
        conn = pymssql.connect(
            server='SATURNO13',
            database='OnesiteDW',
            user='data_analysis_admin',
            password='Hg1y3m9VFJsNrzjw8brjbc'
        )
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO ESQUEMA 'security' EN OnesiteDW")
        print("=" * 60)
        
        # 1. Verificar tablas en esquema security
        print("\n📋 TABLAS EN ESQUEMA security:")
        cursor.execute("""
            SELECT 
                table_name, 
                table_type
            FROM information_schema.tables 
            WHERE table_schema = 'security'
            ORDER BY table_name
        """)
        security_tables = cursor.fetchall()
        
        if security_tables:
            for table in security_tables:
                print(f"  - {table[0]} ({table[1]})")
                
                # Ver columnas de cada tabla
                cursor.execute(f"""
                    SELECT 
                        column_name,
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns 
                    WHERE table_schema = 'security' AND table_name = '{table[0]}'
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                
                print(f"    Columnas:")
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"      - {col[0]} ({col[1]}) {nullable}{default}")
                
                # Ver datos de muestra si la tabla tiene pocos registros
                cursor.execute(f"SELECT COUNT(*) FROM security.[{table[0]}]")
                count = cursor.fetchone()[0]
                print(f"    Registros: {count}")
                
                if count > 0 and count <= 10:
                    cursor.execute(f"SELECT TOP 3 * FROM security.[{table[0]}]")
                    sample_data = cursor.fetchall()
                    print(f"    Muestra de datos:")
                    for row in sample_data:
                        print(f"      {row}")
                
                print()
        else:
            print("  ❌ No se encontraron tablas en el esquema security")
        
        # 2. Verificar vistas en esquema security
        print("\n👁️ VISTAS EN ESQUEMA security:")
        cursor.execute("""
            SELECT 
                table_name
            FROM information_schema.views 
            WHERE table_schema = 'security'
            ORDER BY table_name
        """)
        security_views = cursor.fetchall()
        
        if security_views:
            for view in security_views:
                print(f"  - {view[0]} (VIEW)")
        else:
            print("  ❌ No se encontraron vistas en el esquema security")
        
        # 3. Verificar procedimientos almacenados en esquema security
        print("\n⚙️ PROCEDIMIENTOS ALMACENADOS EN ESQUEMA security:")
        cursor.execute("""
            SELECT 
                routine_name,
                routine_type
            FROM information_schema.routines 
            WHERE routine_schema = 'security'
            ORDER BY routine_name
        """)
        security_routines = cursor.fetchall()
        
        if security_routines:
            for routine in security_routines:
                print(f"  - {routine[0]} ({routine[1]})")
        else:
            print("  ❌ No se encontraron procedimientos en el esquema security")
        
        cursor.close()
        conn.close()
        
        # 4. Análisis y recomendaciones
        print("\n💡 ANÁLISIS:")
        print("=" * 60)
        
        if security_tables:
            print("✅ El esquema 'security' ya existe y contiene elementos")
            print("\n🤔 CONSIDERACIONES PARA OneSite vs security:")
            print("- Si 'security' contiene autenticación/autorización existente,")
            print("  podríamos integrar OneSite con ese esquema")
            print("- Si 'security' es para otro propósito, mantener OneSite separado")
            print("- Evaluar si hay conflictos o duplicaciones")
        else:
            print("⚠️  El esquema 'security' existe pero está vacío")
            print("- Podríamos usar 'security' en lugar de 'OneSite'")
            print("- O mantener 'OneSite' para claridad conceptual")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando esquema security: {e}")
        return False

if __name__ == "__main__":
    check_security_schema()