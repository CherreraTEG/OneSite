import requests
import json

url = "http://127.0.0.1:8000/api/v1/trucks"
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

data = {
    "id_empresa": 0,
    "id_warehouse": 0,
    "ship_date": "2025-06-26",
    "deliv_date": "2025-06-26",
    "carrier": "string",
    "customer_facility": "string",
    "po": "string",
    "qty": 0,
    "estatus": 0,
    "time_in": "01:26:07.972Z",
    "door": "string",
    "time_out": "01:26:07.972Z",
    "comments": "string",
    "pickup_location": "string",
    "load_number": "string",
    "id_customer": 0,
    "estado_cargue": 0,
    "update_date": "2025-06-26T01:26:07.972Z",
    "update_user": "string",
    "file_name": "string"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}") 