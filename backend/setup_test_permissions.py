#!/usr/bin/env python3
"""
Script para configurar permisos de prueba en user_company_permission
"""
import sys
import os

# Agregar el directorio app al path
sys.path.append('app')

def create_test_permissions():
    """Crea permisos de prueba en la base de datos"""
    try:
        from app.db.databases import get_main_db, get_companies_db
        from app.models.user import User
        from app.models.company import Company
        from app.models.user_company_permission import UserCompanyPermission
        
        print("🔍 Configurando permisos de prueba...")
        
        # Obtener sesiones de base de datos
        main_db = next(get_main_db())
        companies_db = next(get_companies_db())
        
        try:
            # Listar usuarios disponibles
            users = main_db.query(User).limit(5).all()
            print(f"\n👥 Usuarios disponibles ({len(users)}):")
            for user in users:
                print(f"  - ID: {user.id}, Username: {user.username}")
            
            # Listar empresas activas disponibles
            active_companies = companies_db.query(Company).filter(Company.Estado_Cargue == 1).limit(5).all()
            print(f"\n🏢 Empresas activas disponibles ({len(active_companies)}):")
            for company in active_companies:
                print(f"  - ID: {company.id_Company}, Nombre: {company.Company or company.BU}")
            
            # Verificar permisos existentes
            existing_permissions = companies_db.query(UserCompanyPermission).limit(10).all()
            print(f"\n🔐 Permisos existentes ({len(existing_permissions)}):")
            for perm in existing_permissions:
                print(f"  - Usuario ID: {perm.user_id}, Empresa ID: {perm.company_id}")
            
            if len(existing_permissions) == 0:
                print("\n⚠️  No hay permisos configurados.")
                print("💡 Para crear permisos de prueba, ejecuta manualmente:")
                print("   INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 1);")
                print("   (Reemplaza 1, 1 con IDs válidos de usuario y empresa)")
            
            print(f"\n📊 RESUMEN:")
            print(f"   - {len(users)} usuarios en el sistema")
            print(f"   - {len(active_companies)} empresas activas")
            print(f"   - {len(existing_permissions)} permisos configurados")
            
            return True
            
        finally:
            main_db.close()
            companies_db.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 CONFIGURACIÓN DE PERMISOS DE PRUEBA")
    print("=" * 50)
    
    success = create_test_permissions()
    
    if success:
        print("\n✅ Verificación completada")
        print("\n🔧 Para probar la funcionalidad:")
        print("1. Asegúrate de tener permisos configurados en user_company_permission")
        print("2. Haz login en el frontend")
        print("3. Observa el selector de empresas en el sidebar")
        print("4. Si no hay empresas, verás: 'No tienes empresas asignadas'")
    else:
        print("\n❌ Error en la verificación")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())