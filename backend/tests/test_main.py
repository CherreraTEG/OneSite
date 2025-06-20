from fastapi.testclient import TestClient
import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
# Esto es necesario para que pytest pueda encontrar los módulos de la aplicación
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def test_read_root():
    """
    Prueba que el endpoint raíz ("/") devuelva una respuesta exitosa.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a OneSite API"} 