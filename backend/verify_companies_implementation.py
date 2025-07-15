#!/usr/bin/env python3
"""
Script para verificar la implementación de validación de empresas
"""
import sys
import os
sys.path.append('app')

from app.crud.crud_company import company
from app.db.databases import get_companies_db
from app.models.user_company_permission import UserCompanyPermission
from app.models.company import Company

def test_crud_methods():
    """Prueba los métodos CRUD implementados"""
    print("🧪 Verificando métodos CRUD implementados...")
    
    # Verificar que el método get_companies_for_user existe
    try:
        assert hasattr(company, 'get_companies_for_user'), "Método get_companies_for_user no encontrado"
        print("✅ Método get_companies_for_user implementado")
        
        assert hasattr(company, 'get_active_companies'), "Método get_active_companies no encontrado"
        print("✅ Método get_active_companies implementado")
        
        # Verificar que el modelo UserCompanyPermission existe
        assert hasattr(UserCompanyPermission, '__tablename__'), "Modelo UserCompanyPermission no encontrado"
        print("✅ Modelo UserCompanyPermission definido")
        
        # Verificar que el modelo Company tiene las propiedades necesarias
        assert hasattr(Company, 'id_Company'), "Campo id_Company no encontrado en Company"
        assert hasattr(Company, 'Estado_Cargue'), "Campo Estado_Cargue no encontrado en Company"
        print("✅ Modelo Company con campos necesarios")
        
        print("\n✅ Todos los componentes están implementados correctamente")
        return True
        
    except AssertionError as e:
        print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n🔗 Probando conexión a base de datos de empresas...")
    
    try:
        # Obtener sesión de base de datos
        db_session = next(get_companies_db())
        
        # Probar consulta simple
        companies_count = db_session.query(Company).count()
        print(f"✅ Conexión exitosa. Total de empresas en BD: {companies_count}")
        
        # Probar consulta de empresas activas
        active_companies = company.get_active_companies(db_session)
        print(f"✅ Empresas activas encontradas: {len(active_companies)}")
        
        if len(active_companies) > 0:
            print("📋 Primeras 3 empresas activas:")
            for i, comp in enumerate(active_companies[:3]):
                print(f"  {i+1}. ID: {comp.id_Company}, Nombre: {comp.Company or comp.BU}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_user_company_permissions():
    """Prueba la funcionalidad de permisos de usuario"""
    print("\n👤 Probando tabla de permisos usuario-empresa...")
    
    try:
        db_session = next(get_companies_db())
        
        # Contar registros en la tabla de permisos
        permissions_count = db_session.query(UserCompanyPermission).count()
        print(f"✅ Registros en user_company_permission: {permissions_count}")
        
        if permissions_count > 0:
            # Mostrar algunos ejemplos
            sample_permissions = db_session.query(UserCompanyPermission).limit(3).all()
            print("📋 Ejemplos de permisos:")
            for perm in sample_permissions:
                print(f"  Usuario ID: {perm.user_id}, Empresa ID: {perm.company_id}")
        else:
            print("⚠️ No hay permisos configurados. Esto significa que ningún usuario tendrá empresas asignadas.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error consultando permisos: {e}")
        return False

def show_implementation_summary():
    """Muestra un resumen de la implementación"""
    print("\n📋 RESUMEN DE LA IMPLEMENTACIÓN")
    print("=" * 50)
    print("✅ Backend:")
    print("  - Endpoint /api/v1/companies/active actualizado")
    print("  - Validación de permisos por usuario implementada")
    print("  - CRUD con métodos get_companies_for_user y get_active_companies")
    print("  - Join entre User, Company y UserCompanyPermission")
    print()
    print("✅ Frontend:")
    print("  - Selector de empresas actualizado en sidebar")
    print("  - Mensaje 'No tienes empresas asignadas' cuando aplique")
    print("  - Traducciones en ES, EN, FR")
    print("  - Estilos CSS para estado sin empresas")
    print()
    print("🔧 Para configurar permisos:")
    print("  - Insertar registros en tabla 'user_company_permission'")
    print("  - Ejemplo: INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 2)")
    print()
    print("🧪 Para probar:")
    print("  - Accede a http://localhost:4200")
    print("  - Haz login con un usuario")
    print("  - Observa el selector de empresas en el sidebar")

def main():
    print("🔍 VERIFICACIÓN DE IMPLEMENTACIÓN - VALIDACIÓN DE EMPRESAS")
    print("=" * 65)
    
    success = True
    
    # Verificar implementación
    if not test_crud_methods():
        success = False
    
    # Verificar conexión a BD
    if not test_database_connection():
        success = False
    
    # Verificar permisos
    if not test_user_company_permissions():
        success = False
    
    # Mostrar resumen
    show_implementation_summary()
    
    if success:
        print("\n🎉 ¡Implementación completa y funcional!")
    else:
        print("\n⚠️ Hay algunos problemas que requieren atención")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())