#!/usr/bin/env python3
"""
Test simple del endpoint de empresas
"""
import urllib.request
import json

def test_endpoint():
    """Prueba básica del endpoint"""
    try:
        # Test endpoint público
        print("🔍 Probando endpoint de test...")
        response = urllib.request.urlopen('http://localhost:8000/api/v1/companies/test')
        data = json.loads(response.read().decode())
        print("✅ Test endpoint:", data)
        
        # Test endpoint protegido (debe fallar)
        print("\n🔒 Probando endpoint protegido...")
        try:
            response = urllib.request.urlopen('http://localhost:8000/api/v1/companies/active')
            print("❌ ERROR: Endpoint no está protegido")
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print("✅ Endpoint protegido correctamente (401 Unauthorized)")
            else:
                print(f"⚠️ Error inesperado: {e.code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_endpoint()