#!/usr/bin/env python3
"""
Script para probar la validación de empresas asignadas al usuario
"""
import os
import sys
import requests
import json

# Configuración del servidor
BASE_URL = "http://127.0.0.1:8000"

def test_login():
    """Prueba el login para obtener un token"""
    print("🔐 Probando login...")
    
    # Datos de prueba (ajustar según sea necesario)
    login_data = {
        "username": "test_user",  # Cambiar por un usuario real
        "password": "test_password"  # Cambiar por una contraseña real
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login-json", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login exitoso")
            return token_data.get("access_token")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error conectando con el servidor: {e}")
        return None

def test_companies_endpoint(token):
    """Prueba el endpoint de empresas activas con token"""
    print("\n🏢 Probando endpoint de empresas activas...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/companies/active", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            companies = response.json()
            print(f"✅ Respuesta exitosa: {len(companies)} empresas encontradas")
            
            if len(companies) == 0:
                print("⚠️ No se encontraron empresas asignadas al usuario")
                return []
            else:
                print("📋 Empresas asignadas:")
                for company in companies:
                    print(f"  - ID: {company.get('id')}, Nombre: {company.get('Company', 'N/A')}")
                return companies
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return None

def test_without_token():
    """Prueba el endpoint sin token para verificar la seguridad"""
    print("\n🔒 Probando endpoint sin token (debe fallar)...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/companies/active")
        
        if response.status_code == 401:
            print("✅ Seguridad correcta: endpoint requiere autenticación")
        else:
            print(f"⚠️ Posible problema de seguridad: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")

def test_health_endpoint():
    """Prueba el endpoint de salud del servidor"""
    print("🏥 Probando endpoint de salud...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Servidor saludable")
            print(f"Version: {health_data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Servidor no saludable: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando con el servidor: {e}")
        return False

def main():
    print("🧪 Iniciando pruebas de validación de empresas")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    if not test_health_endpoint():
        print("\n❌ El servidor no está disponible. Verifica que el backend esté ejecutándose.")
        return 1
    
    # Probar seguridad sin token
    test_without_token()
    
    # Probar login (comentado ya que necesita credenciales reales)
    print(f"\n📝 Para probar completamente:")
    print(f"1. Actualiza las credenciales en la función test_login()")
    print(f"2. Ejecuta el script nuevamente")
    print(f"3. O prueba manualmente en: {BASE_URL}/docs")
    
    # token = test_login()
    # if token:
    #     test_companies_endpoint(token)
    # else:
    #     print("\n❌ No se pudo obtener token de autenticación")
    
    print(f"\n🌐 URLs de prueba:")
    print(f"- Documentación API: {BASE_URL}/docs")
    print(f"- Salud del servidor: {BASE_URL}/health")
    print(f"- Frontend: http://localhost:4200")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())