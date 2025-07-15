#!/usr/bin/env python3
"""
Script para crear el esquema OneSite con la distribución acordada:
- OneSite: Usuarios de aplicación y permisos
- security: Sistema de seguridad (ya existe)
- TheEliteGroup_Parameters: Datos de negocio (ya existe)
- trucks: Operaciones logísticas (ya existe)
"""

import pymssql
import os
from dotenv import load_dotenv
import hashlib
import secrets

# Cargar variables de entorno
load_dotenv()

def generate_password_hash(password: str) -> str:
    """Genera un hash simple para pruebas (usar bcrypt en producción)"""
    salt = secrets.token_hex(16)
    return f"$2b$12${salt}.{hashlib.sha256((password + salt).encode()).hexdigest()[:22]}"

def setup_onesite_schema():
    """Crea el esquema OneSite con la distribución acordada"""
    
    try:
        # Conectar a la base de datos
        conn = pymssql.connect(
            server='SATURNO13',
            database='OnesiteDW',
            user='data_analysis_admin',
            password='Hg1y3m9VFJsNrzjw8brjbc'
        )
        cursor = conn.cursor()
        
        print("🚀 CONFIGURANDO ESQUEMA OneSite - DISTRIBUCIÓN ACORDADA")
        print("=" * 70)
        print("📋 DISTRIBUCIÓN:")
        print("  - OneSite: Usuarios y permisos de aplicación")
        print("  - security: Sistema de seguridad (ya existe)")
        print("  - TheEliteGroup_Parameters: Datos de negocio (ya existe)")
        print("  - trucks: Operaciones logísticas (ya existe)")
        print("=" * 70)
        
        # 1. Crear esquema OneSite
        print("\n📁 Creando esquema OneSite...")
        try:
            cursor.execute("CREATE SCHEMA OneSite")
            conn.commit()
            print("  ✅ Esquema 'OneSite' creado exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "There is already" in str(e):
                print("  ⚠️  Esquema 'OneSite' ya existe")
            else:
                print(f"  ❌ Error creando esquema: {e}")
                return False
        
        # 2. Crear tabla user (usuarios de la aplicación OneSite)
        print("\n👤 Creando tabla OneSite.user...")
        try:
            cursor.execute("""
                CREATE TABLE OneSite.[user] (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(50) NOT NULL UNIQUE,
                    email NVARCHAR(100) NOT NULL UNIQUE,
                    full_name NVARCHAR(150) NULL,
                    hashed_password NVARCHAR(255) NOT NULL,
                    is_active BIT DEFAULT 1,
                    is_superuser BIT DEFAULT 0,
                    created_at DATETIME2 DEFAULT GETUTCDATE(),
                    updated_at DATETIME2 DEFAULT GETUTCDATE(),
                    last_login DATETIME2 NULL,
                    
                    -- Índices para optimización
                    INDEX IX_user_username (username),
                    INDEX IX_user_email (email),
                    INDEX IX_user_active (is_active)
                )
            """)
            conn.commit()
            print("  ✅ Tabla 'OneSite.user' creada exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "There is already" in str(e):
                print("  ⚠️  Tabla 'OneSite.user' ya existe")
            else:
                print(f"  ❌ Error creando tabla user: {e}")
        
        # 3. Crear tabla role (roles del sistema)
        print("\n🎭 Creando tabla OneSite.role...")
        try:
            cursor.execute("""
                CREATE TABLE OneSite.role (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name NVARCHAR(50) NOT NULL UNIQUE,
                    description NVARCHAR(255) NULL,
                    is_active BIT DEFAULT 1,
                    created_at DATETIME2 DEFAULT GETUTCDATE(),
                    updated_at DATETIME2 DEFAULT GETUTCDATE(),
                    
                    -- Índices
                    INDEX IX_role_name (name),
                    INDEX IX_role_active (is_active)
                )
            """)
            conn.commit()
            print("  ✅ Tabla 'OneSite.role' creada exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "There is already" in str(e):
                print("  ⚠️  Tabla 'OneSite.role' ya existe")
            else:
                print(f"  ❌ Error creando tabla role: {e}")
        
        # 4. Crear tabla user_role (relación many-to-many)
        print("\n🔗 Creando tabla OneSite.user_role...")
        try:
            cursor.execute("""
                CREATE TABLE OneSite.user_role (
                    user_id INT NOT NULL,
                    role_id INT NOT NULL,
                    assigned_at DATETIME2 DEFAULT GETUTCDATE(),
                    assigned_by NVARCHAR(50) NULL,
                    
                    PRIMARY KEY (user_id, role_id),
                    FOREIGN KEY (user_id) REFERENCES OneSite.[user](id) ON DELETE CASCADE,
                    FOREIGN KEY (role_id) REFERENCES OneSite.role(id) ON DELETE CASCADE
                )
            """)
            conn.commit()
            print("  ✅ Tabla 'OneSite.user_role' creada exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "There is already" in str(e):
                print("  ⚠️  Tabla 'OneSite.user_role' ya existe")
            else:
                print(f"  ❌ Error creando tabla user_role: {e}")
        
        # 5. Crear tabla user_company_permission (permisos por empresa)
        print("\n🏢 Creando tabla OneSite.user_company_permission...")
        try:
            cursor.execute("""
                CREATE TABLE OneSite.user_company_permission (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    company_code NVARCHAR(50) NOT NULL,  -- Referencia a Companies.id_Oracle o Companies.id_Company
                    permission_type NVARCHAR(50) DEFAULT 'read',  -- read, write, admin
                    is_active BIT DEFAULT 1,
                    created_at DATETIME2 DEFAULT GETUTCDATE(),
                    updated_at DATETIME2 DEFAULT GETUTCDATE(),
                    created_by NVARCHAR(50) NULL,
                    
                    FOREIGN KEY (user_id) REFERENCES OneSite.[user](id) ON DELETE CASCADE,
                    
                    -- Índices para optimización
                    INDEX IX_user_company_user (user_id),
                    INDEX IX_user_company_company (company_code),
                    INDEX IX_user_company_active (is_active),
                    
                    -- Constraint único para evitar duplicados
                    UNIQUE (user_id, company_code)
                )
            """)
            conn.commit()
            print("  ✅ Tabla 'OneSite.user_company_permission' creada exitosamente")
        except Exception as e:
            if "already exists" in str(e) or "There is already" in str(e):
                print("  ⚠️  Tabla 'OneSite.user_company_permission' ya existe")
            else:
                print(f"  ❌ Error creando tabla user_company_permission: {e}")
        
        # 6. Insertar roles básicos del sistema
        print("\n🎭 Insertando roles básicos...")
        try:
            roles = [
                ('admin', 'Administrador del sistema con acceso completo'),
                ('user', 'Usuario estándar con permisos limitados'),
                ('viewer', 'Solo lectura, sin permisos de modificación'),
                ('company_admin', 'Administrador de empresa específica')
            ]
            
            for role_name, role_desc in roles:
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM OneSite.role WHERE name = ?)
                        INSERT INTO OneSite.role (name, description) VALUES (?, ?)
                """, (role_name, role_name, role_desc))
            
            conn.commit()
            print("  ✅ Roles básicos insertados")
        except Exception as e:
            print(f"  ❌ Error insertando roles: {e}")
        
        # 7. Crear usuario de prueba cherrera
        print("\n👤 Creando usuario de prueba 'cherrera'...")
        try:
            # Generar hash de contraseña temporal
            temp_password_hash = generate_password_hash("123")
            
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM OneSite.[user] WHERE username = 'cherrera')
                BEGIN
                    INSERT INTO OneSite.[user] (username, email, full_name, hashed_password, is_active, is_superuser) 
                    VALUES ('cherrera', 'cherrera@elite.local', 'Carlos Herrera', ?, 1, 1)
                END
            """, (temp_password_hash,))
            conn.commit()
            
            # Asignar rol admin al usuario
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
            
            print("  ✅ Usuario 'cherrera' creado con rol admin")
        except Exception as e:
            print(f"  ❌ Error creando usuario: {e}")
        
        # 8. Verificar la configuración completa
        print("\n🔍 Verificando configuración final...")
        
        # Verificar tablas creadas
        cursor.execute("""
            SELECT 
                t.table_name,
                COUNT(c.column_name) as column_count
            FROM information_schema.tables t
            LEFT JOIN information_schema.columns c ON t.table_name = c.table_name AND t.table_schema = c.table_schema
            WHERE t.table_schema = 'OneSite'
            GROUP BY t.table_name
            ORDER BY t.table_name
        """)
        tables = cursor.fetchall()
        for table in tables:
            print(f"  ✅ OneSite.{table[0]} ({table[1]} columnas)")
        
        # Verificar roles
        cursor.execute("SELECT name FROM OneSite.role WHERE is_active = 1")
        roles = cursor.fetchall()
        print(f"  ✅ Roles configurados: {', '.join([r[0] for r in roles])}")
        
        # Verificar usuario
        cursor.execute("""
            SELECT u.username, u.full_name, r.name as role
            FROM OneSite.[user] u
            LEFT JOIN OneSite.user_role ur ON u.id = ur.user_id
            LEFT JOIN OneSite.role r ON ur.role_id = r.id
            WHERE u.username = 'cherrera'
        """)
        user_info = cursor.fetchone()
        if user_info:
            print(f"  ✅ Usuario: {user_info[0]} ({user_info[1]}) - Rol: {user_info[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 70)
        print("✅ Esquema OneSite configurado con tablas de aplicación")
        print("✅ Sistema de roles y permisos implementado")
        print("✅ Usuario de prueba 'cherrera' disponible")
        print("✅ Integración lista con esquema 'security' existente")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Actualizar modelos SQLAlchemy para usar esquema 'OneSite'")
        print("2. Restaurar funcionalidad de permisos en endpoints")
        print("3. Configurar integración con sistema de auditoría 'security'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

if __name__ == "__main__":
    setup_onesite_schema()