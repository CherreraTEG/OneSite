import requests
import json
from datetime import datetime, date, time

def test_create_truck():
    """Prueba la creación de un registro de truck"""
    url = "http://127.0.0.1:8000/api/v1/trucks"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Datos de prueba
    data = {
        "id_empresa": 1,
        "id_warehouse": 1,
        "ship_date": "2025-06-26",
        "deliv_date": "2025-06-27",
        "carrier": "Transporte ABC",
        "customer_facility": "Almacén Central",
        "po": "PO-2025-001",
        "qty": 100.5,
        "estatus": 1,
        "time_in": "08:30:00",
        "door": "A1",
        "time_out": "16:45:00",
        "comments": "Carga urgente para cliente VIP",
        "pickup_location": "Zona de carga norte",
        "load_number": "LOAD-2025-001",
        "id_customer": 1,
        "estado_cargue": 1,
        "update_date": "2025-06-26T12:00:00",
        "update_user": "admin",
        "file_name": "truck_data_001.csv"
    }

    print("=== PRUEBA DE CREACIÓN DE TRUCK ===")
    print(f"URL: {url}")
    print(f"Datos enviados: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Truck creado con ID: {result.get('id')}")
            print(f"Respuesta completa: {json.dumps(result, indent=2)}")
            return result.get('id')
        else:
            print(f"❌ ERROR - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return None

def test_get_truck(truck_id):
    """Prueba la obtención de un truck específico"""
    if not truck_id:
        print("❌ No se puede probar GET sin ID válido")
        return
        
    url = f"http://127.0.0.1:8000/api/v1/trucks/{truck_id}"
    headers = {'accept': 'application/json'}
    
    print(f"\n=== PRUEBA DE OBTENCIÓN DE TRUCK (ID: {truck_id}) ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Truck encontrado")
            print(f"Respuesta: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ ERROR - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

def test_get_trucks():
    """Prueba la obtención de la lista de trucks"""
    url = "http://127.0.0.1:8000/api/v1/trucks"
    headers = {'accept': 'application/json'}
    
    print(f"\n=== PRUEBA DE LISTADO DE TRUCKS ===")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Se encontraron {len(result)} trucks")
            if result:
                print(f"Primer truck: {json.dumps(result[0], indent=2)}")
        else:
            print(f"❌ ERROR - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

def test_validation_errors():
    """Prueba errores de validación"""
    url = "http://127.0.0.1:8000/api/v1/trucks"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Datos inválidos
    invalid_data = {
        "id_empresa": "no_es_numero",  # Debería ser int
        "ship_date": "fecha_invalida",  # Formato de fecha inválido
        "time_in": "hora_invalida"      # Formato de hora inválido
    }

    print(f"\n=== PRUEBA DE VALIDACIÓN DE ERRORES ===")
    print(f"URL: {url}")
    print(f"Datos inválidos: {json.dumps(invalid_data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=invalid_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 422:
            result = response.json()
            print(f"✅ ÉXITO - Error de validación capturado correctamente")
            print(f"Detalles del error: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ ERROR - Se esperaba 422, se obtuvo {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    print("🚛 INICIANDO PRUEBAS COMPLETAS DEL MÓDULO TRUCKS")
    print("=" * 60)
    
    # Prueba 1: Crear truck
    truck_id = test_create_truck()
    
    # Prueba 2: Obtener truck específico
    test_get_truck(truck_id)
    
    # Prueba 3: Listar trucks
    test_get_trucks()
    
    # Prueba 4: Validación de errores
    test_validation_errors()
    
    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS") 