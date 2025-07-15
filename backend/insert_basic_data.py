#!/usr/bin/env python3
"""
Script para insertar datos básicos en el esquema OneSite
"""

import pymssql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def insert_basic_data():
    """Inserta roles y usuario básicos"""
    
    try:
        conn = pymssql.connect(
            server='SATURNO13',
            database='OnesiteDW',
            user='data_analysis_admin',
            password='Hg1y3m9VFJsNrzjw8brjbc'
        )
        cursor = conn.cursor()
        
        print("📝 INSERTANDO DATOS BÁSICOS EN OneSite")
        print("=" * 50)
        
        # 1. Insertar roles básicos
        print("\n🎭 Insertando roles...")
        roles = [
            ("admin", "Administrador del sistema con acceso completo"),
            ("user", "Usuario estándar con permisos limitados"), 
            ("viewer", "Solo lectura, sin permisos de modificación"),
            ("company_admin", "Administrador de empresa específica")
        ]
        
        for role_name, role_desc in roles:
            try:
                cursor.execute(f"""
                    IF NOT EXISTS (SELECT 1 FROM OneSite.role WHERE name = '{role_name}')
                        INSERT INTO OneSite.role (name, description) VALUES ('{role_name}', '{role_desc}')
                """)
                conn.commit()
                print(f"  ✅ Rol '{role_name}' insertado")
            except Exception as e:
                print(f"  ⚠️  Error con rol '{role_name}': {e}")
        
        # 2. Insertar usuario cherrera
        print("\n👤 Insertando usuario cherrera...")
        try:
            # Hash temporal simple (usar bcrypt en producción)
            temp_hash = "$2b$12$dummy.hash.for.testing.purposes.only"
            
            cursor.execute(f"""
                IF NOT EXISTS (SELECT 1 FROM OneSite.[user] WHERE username = 'cherrera')
                    INSERT INTO OneSite.[user] (username, email, full_name, hashed_password, is_active, is_superuser) 
                    VALUES ('cherrera', 'cherrera@elite.local', 'Carlos Herrera', '{temp_hash}', 1, 1)
            """)
            conn.commit()
            print("  ✅ Usuario 'cherrera' insertado")
        except Exception as e:
            print(f"  ❌ Error insertando usuario: {e}")
        
        # 3. Asignar rol admin a cherrera
        print("\n🔗 Asignando rol admin...")
        try:
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM OneSite.user_role ur
                    JOIN OneSite.[user] u ON ur.user_id = u.id
                    JOIN OneSite.role r ON ur.role_id = r.id
                    WHERE u.username = 'cherrera' AND r.name = 'admin'
                )
                BEGIN
                    INSERT INTO OneSite.user_role (user_id, role_id, assigned_by)
                    SELECT u.id, r.id, 'system'
                    FROM OneSite.[user] u, OneSite.role r
                    WHERE u.username = 'cherrera' AND r.name = 'admin'
                END
            """)
            conn.commit()
            print("  ✅ Rol admin asignado a cherrera")
        except Exception as e:
            print(f"  ❌ Error asignando rol: {e}")
        
        # 4. Verificar datos insertados
        print("\n🔍 Verificando datos...")
        
        # Verificar roles
        cursor.execute("SELECT name, description FROM OneSite.role ORDER BY name")
        roles = cursor.fetchall()
        print("  📋 Roles disponibles:")
        for role in roles:
            print(f"    - {role[0]}: {role[1]}")
        
        # Verificar usuario
        cursor.execute("""
            SELECT u.username, u.full_name, u.email, u.is_active, u.is_superuser,
                   STRING_AGG(r.name, ', ') as roles
            FROM OneSite.[user] u
            LEFT JOIN OneSite.user_role ur ON u.id = ur.user_id
            LEFT JOIN OneSite.role r ON ur.role_id = r.id
            WHERE u.username = 'cherrera'
            GROUP BY u.username, u.full_name, u.email, u.is_active, u.is_superuser
        """)
        user_info = cursor.fetchone()
        if user_info:
            print(f"  👤 Usuario configurado:")
            print(f"    - Username: {user_info[0]}")
            print(f"    - Nombre: {user_info[1]}")
            print(f"    - Email: {user_info[2]}")
            print(f"    - Activo: {'Sí' if user_info[3] else 'No'}")
            print(f"    - Superuser: {'Sí' if user_info[4] else 'No'}")
            print(f"    - Roles: {user_info[5] or 'Sin roles'}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 DATOS BÁSICOS INSERTADOS EXITOSAMENTE")
        
        return True
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        return False

if __name__ == "__main__":
    insert_basic_data()