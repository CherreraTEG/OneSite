import requests
import json

def test_get_trucks():
    """Prueba el endpoint GET para obtener la lista de trucks"""
    url = "http://127.0.0.1:8000/api/v1/trucks"
    headers = {'accept': 'application/json'}
    
    print("=== PRUEBA GET /api/v1/trucks ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Se encontraron {len(result)} trucks")
            if result:
                print(f"Primer truck: {json.dumps(result[0], indent=2)}")
            else:
                print("No hay trucks en la base de datos")
        else:
            print(f"❌ ERROR - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

def test_get_truck_by_id(truck_id):
    """Prueba el endpoint GET para obtener un truck específico"""
    url = f"http://127.0.0.1:8000/api/v1/trucks/{truck_id}"
    headers = {'accept': 'application/json'}
    
    print(f"\n=== PRUEBA GET /api/v1/trucks/{truck_id} ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Truck encontrado")
            print(f"Truck: {json.dumps(result, indent=2)}")
        elif response.status_code == 404:
            print(f"⚠️  Truck con ID {truck_id} no encontrado")
        else:
            print(f"❌ ERROR - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    print("🚛 INICIANDO PRUEBAS GET DEL MÓDULO TRUCKS")
    print("=" * 50)
    
    # Prueba 1: Obtener lista de trucks
    test_get_trucks()
    
    # Prueba 2: Obtener truck específico (ID 1)
    test_get_truck_by_id(1)
    
    # Prueba 3: Obtener truck específico (ID 7 - que sabemos que existe)
    test_get_truck_by_id(7)
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBAS GET COMPLETADAS") 