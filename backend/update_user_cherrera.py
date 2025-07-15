#!/usr/bin/env python3
"""
Script para actualizar la información del usuario cherrera
"""

import pymssql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def update_user_cherrera():
    """Actualiza la información del usuario cherrera"""
    
    try:
        conn = pymssql.connect(
            server='SATURNO13',
            database='OnesiteDW',
            user='data_analysis_admin',
            password='Hg1y3m9VFJsNrzjw8brjbc'
        )
        cursor = conn.cursor()
        
        print("📝 ACTUALIZANDO INFORMACIÓN DEL USUARIO CHERRERA")
        print("=" * 55)
        
        # 1. Verificar usuario actual
        print("\n🔍 Información actual del usuario:")
        cursor.execute("""
            SELECT id, username, email, full_name, is_active, is_superuser
            FROM OneSite.[user] 
            WHERE id = 1
        """)
        current_user = cursor.fetchone()
        
        if current_user:
            print(f"  - ID: {current_user[0]}")
            print(f"  - Username: {current_user[1]}")
            print(f"  - Email: {current_user[2]}")
            print(f"  - Nombre: {current_user[3]}")
            print(f"  - Activo: {'Sí' if current_user[4] else 'No'}")
            print(f"  - Superuser: {'Sí' if current_user[5] else 'No'}")
        else:
            print("  ❌ Usuario con ID=1 no encontrado")
            return False
        
        # 2. Actualizar información
        print("\n✏️  Actualizando información...")
        cursor.execute("""
            UPDATE OneSite.[user] 
            SET 
                email = 'cherrera@eliteflower.com',
                full_name = 'Claudia Herrera',
                updated_at = GETUTCDATE()
            WHERE id = 1
        """)
        conn.commit()
        print("  ✅ Información actualizada exitosamente")
        
        # 3. Verificar cambios
        print("\n🔍 Información actualizada:")
        cursor.execute("""
            SELECT id, username, email, full_name, is_active, is_superuser, updated_at
            FROM OneSite.[user] 
            WHERE id = 1
        """)
        updated_user = cursor.fetchone()
        
        if updated_user:
            print(f"  - ID: {updated_user[0]}")
            print(f"  - Username: {updated_user[1]}")
            print(f"  - Email: {updated_user[2]}")
            print(f"  - Nombre: {updated_user[3]}")
            print(f"  - Activo: {'Sí' if updated_user[4] else 'No'}")
            print(f"  - Superuser: {'Sí' if updated_user[5] else 'No'}")
            print(f"  - Actualizado: {updated_user[6]}")
        
        # 4. Verificar roles del usuario
        print("\n🎭 Roles asignados:")
        cursor.execute("""
            SELECT r.name, r.description
            FROM OneSite.role r
            JOIN OneSite.user_role ur ON r.id = ur.role_id
            WHERE ur.user_id = 1
        """)
        roles = cursor.fetchall()
        
        for role in roles:
            print(f"  - {role[0]}: {role[1]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 USUARIO ACTUALIZADO EXITOSAMENTE")
        print("=" * 55)
        print("✅ Email cambiado a: cherrera@eliteflower.com")
        print("✅ Nombre cambiado a: Claudia Herrera")
        print("✅ Timestamp de actualización registrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando usuario: {e}")
        return False

if __name__ == "__main__":
    update_user_cherrera()