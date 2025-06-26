# Documentación del Módulo de Camiones (Trucks)

## Descripción General

El módulo de camiones permite gestionar el control y seguimiento de camiones en el sistema OneSite. Proporciona endpoints para crear, leer, actualizar y eliminar registros de camiones, así como consultas especializadas por diferentes criterios.

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticación

Actualmente el módulo no requiere autenticación, pero se recomienda implementar JWT en producción.

## Endpoints Disponibles

### 1. Obtener Lista de Camiones

**GET** `/trucks`

Retorna una lista paginada de camiones con filtros opcionales.

#### Parámetros de Consulta

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `skip` | int | No | Registros a omitir (paginación) | 0 |
| `limit` | int | No | Máximo registros a retornar | 100 |
| `id_empresa` | int | No | Filtrar por empresa | 1 |
| `id_warehouse` | int | No | Filtrar por almacén | 1 |
| `carrier` | string | No | Filtrar por transportista | "ABC" |
| `date_from` | date | No | Fecha inicio (YYYY-MM-DD) | "2025-06-01" |
| `date_to` | date | No | Fecha fin (YYYY-MM-DD) | "2025-06-30" |
| `id_customer` | int | No | Filtrar por cliente | 1 |
| `estatus` | int | No | Filtrar por estado | 1 |
| `load_number` | string | No | Filtrar por número de carga | "LOAD-001" |

#### Ejemplo de Petición

```bash
curl -X GET "http://localhost:8000/api/v1/trucks?skip=0&limit=10&id_empresa=1" \
  -H "accept: application/json"
```

#### Respuesta Exitosa (200)

```json
[
  {
    "id": 1,
    "id_empresa": 1,
    "id_warehouse": 1,
    "ship_date": "2025-06-26",
    "deliv_date": "2025-06-27",
    "carrier": "Transporte ABC S.A.",
    "customer_facility": "Centro de Distribución Norte",
    "po": "PO-2025-001",
    "qty": 100.5,
    "estatus": 1,
    "time_in": "08:30:00.000000",
    "door": "A1",
    "time_out": "16:45:00.000000",
    "comments": "Carga urgente para cliente VIP",
    "pickup_location": "Zona de carga norte",
    "load_number": "LOAD-2025-001",
    "id_customer": 1,
    "estado_cargue": 1,
    "update_date": "2025-06-26T12:00:00.000000",
    "update_user": "admin",
    "file_name": "truck_data_001.csv"
  }
]
```

### 2. Obtener Camión por ID

**GET** `/trucks/{truck_id}`

Retorna los detalles completos de un camión específico.

#### Parámetros de Ruta

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `truck_id` | int | Sí | ID único del camión |

#### Ejemplo de Petición

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/1" \
  -H "accept: application/json"
```

#### Respuesta Exitosa (200)

```json
{
  "id": 1,
  "id_empresa": 1,
  "id_warehouse": 1,
  "ship_date": "2025-06-26",
  "deliv_date": "2025-06-27",
  "carrier": "Transporte ABC S.A.",
  "customer_facility": "Centro de Distribución Norte",
  "po": "PO-2025-001",
  "qty": 100.5,
  "estatus": 1,
  "time_in": "08:30:00.000000",
  "door": "A1",
  "time_out": "16:45:00.000000",
  "comments": "Carga urgente para cliente VIP",
  "pickup_location": "Zona de carga norte",
  "load_number": "LOAD-2025-001",
  "id_customer": 1,
  "estado_cargue": 1,
  "update_date": "2025-06-26T12:00:00.000000",
  "update_user": "admin",
  "file_name": "truck_data_001.csv"
}
```

#### Respuesta de Error (404)

```json
{
  "detail": "Truck not found"
}
```

### 3. Crear Nuevo Camión

**POST** `/trucks`

Crea un nuevo registro de camión.

#### Cuerpo de la Petición

```json
{
  "id_empresa": 1,
  "id_warehouse": 1,
  "ship_date": "2025-06-26",
  "deliv_date": "2025-06-27",
  "carrier": "Transporte ABC S.A.",
  "customer_facility": "Centro de Distribución Norte",
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
```

#### Ejemplo de Petición

```bash
curl -X POST "http://localhost:8000/api/v1/trucks" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "id_empresa": 1,
    "id_warehouse": 1,
    "ship_date": "2025-06-26",
    "carrier": "Transporte ABC S.A.",
    "load_number": "LOAD-2025-001",
    "estatus": 1,
    "update_user": "admin"
  }'
```

#### Respuesta Exitosa (201)

```json
{
  "id": 8,
  "id_empresa": 1,
  "id_warehouse": 1,
  "ship_date": "2025-06-26",
  "deliv_date": null,
  "carrier": "Transporte ABC S.A.",
  "customer_facility": null,
  "po": null,
  "qty": null,
  "estatus": 1,
  "time_in": null,
  "door": null,
  "time_out": null,
  "comments": null,
  "pickup_location": null,
  "load_number": "LOAD-2025-001",
  "id_customer": null,
  "estado_cargue": null,
  "update_date": null,
  "update_user": "admin",
  "file_name": null
}
```

### 4. Actualizar Camión

**PUT** `/trucks/{truck_id}`

Actualiza los datos de un camión existente.

#### Parámetros de Ruta

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `truck_id` | int | Sí | ID único del camión a actualizar |

#### Cuerpo de la Petición

```json
{
  "carrier": "Nuevo Transportista XYZ",
  "estatus": 2,
  "comments": "Camión actualizado con nueva información",
  "update_user": "admin"
}
```

#### Ejemplo de Petición

```bash
curl -X PUT "http://localhost:8000/api/v1/trucks/1" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "carrier": "Nuevo Transportista XYZ",
    "estatus": 2,
    "comments": "Camión actualizado con nueva información",
    "update_user": "admin"
  }'
```

#### Respuesta Exitosa (200)

```json
{
  "id": 1,
  "id_empresa": 1,
  "id_warehouse": 1,
  "ship_date": "2025-06-26",
  "deliv_date": "2025-06-27",
  "carrier": "Nuevo Transportista XYZ",
  "customer_facility": "Centro de Distribución Norte",
  "po": "PO-2025-001",
  "qty": 100.5,
  "estatus": 2,
  "time_in": "08:30:00.000000",
  "door": "A1",
  "time_out": "16:45:00.000000",
  "comments": "Camión actualizado con nueva información",
  "pickup_location": "Zona de carga norte",
  "load_number": "LOAD-2025-001",
  "id_customer": 1,
  "estado_cargue": 1,
  "update_date": "2025-06-26T12:00:00.000000",
  "update_user": "admin",
  "file_name": "truck_data_001.csv"
}
```

### 5. Eliminar Camión

**DELETE** `/trucks/{truck_id}`

Elimina un camión existente.

#### Parámetros de Ruta

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `truck_id` | int | Sí | ID único del camión a eliminar |

#### Ejemplo de Petición

```bash
curl -X DELETE "http://localhost:8000/api/v1/trucks/1" \
  -H "accept: application/json"
```

#### Respuesta Exitosa (200)

```json
{
  "id": 1,
  "id_empresa": 1,
  "id_warehouse": 1,
  "ship_date": "2025-06-26",
  "deliv_date": "2025-06-27",
  "carrier": "Transporte ABC S.A.",
  "customer_facility": "Centro de Distribución Norte",
  "po": "PO-2025-001",
  "qty": 100.5,
  "estatus": 1,
  "time_in": "08:30:00.000000",
  "door": "A1",
  "time_out": "16:45:00.000000",
  "comments": "Carga urgente para cliente VIP",
  "pickup_location": "Zona de carga norte",
  "load_number": "LOAD-2025-001",
  "id_customer": 1,
  "estado_cargue": 1,
  "update_date": "2025-06-26T12:00:00.000000",
  "update_user": "admin",
  "file_name": "truck_data_001.csv"
}
```

### 6. Consultas Especializadas

#### 6.1 Camiones por Empresa y Almacén

**GET** `/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}`

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/empresa/1/warehouse/1" \
  -H "accept: application/json"
```

#### 6.2 Camiones por Empresa, Almacén y Fechas

**GET** `/trucks/empresa/{id_empresa}/warehouse/{id_warehouse}/dates`

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/empresa/1/warehouse/1/dates?date_from=2025-06-01&date_to=2025-06-30" \
  -H "accept: application/json"
```

#### 6.3 Camiones por Almacén y Fechas

**GET** `/trucks/warehouse/{id_warehouse}/dates`

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/warehouse/1/dates?date_from=2025-06-01&date_to=2025-06-30" \
  -H "accept: application/json"
```

#### 6.4 Camiones por Transportista

**GET** `/trucks/carrier/{carrier}`

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/carrier/Transporte%20ABC" \
  -H "accept: application/json"
```

#### 6.5 Camión por Número de Carga

**GET** `/trucks/load/{load_number}`

```bash
curl -X GET "http://localhost:8000/api/v1/trucks/load/LOAD-2025-001" \
  -H "accept: application/json"
```

## Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos de entrada inválidos |
| 404 | Not Found - Recurso no encontrado |
| 422 | Unprocessable Entity - Error de validación |
| 500 | Internal Server Error - Error interno del servidor |

## Modelo de Datos

### Campos del Camión

| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id` | int | ID único del camión | Auto-incrementable |
| `id_empresa` | int | ID de la empresa | ≥ 1 |
| `id_warehouse` | int | ID del almacén | ≥ 1 |
| `ship_date` | date | Fecha de envío | YYYY-MM-DD |
| `deliv_date` | date | Fecha de entrega | YYYY-MM-DD |
| `carrier` | string | Transportista | Máx. 200 caracteres |
| `customer_facility` | string | Instalación del cliente | Máx. 200 caracteres |
| `po` | string | Número de orden de compra | Máx. 200 caracteres |
| `qty` | float | Cantidad de carga | ≥ 0 |
| `estatus` | int | Estado del camión | 0=Inactivo, 1=Activo, etc. |
| `time_in` | time | Hora de entrada | HH:MM:SS |
| `door` | string | Puerta asignada | Máx. 25 caracteres |
| `time_out` | time | Hora de salida | HH:MM:SS |
| `comments` | string | Comentarios | Máx. 1000 caracteres |
| `pickup_location` | string | Ubicación de recogida | Máx. 150 caracteres |
| `load_number` | string | Número de carga | Máx. 50 caracteres |
| `id_customer` | int | ID del cliente | ≥ 1 |
| `estado_cargue` | int | Estado de la carga | 0=Pendiente, 1=Cargando, 2=Completado |
| `update_date` | datetime | Fecha de actualización | ISO format |
| `update_user` | string | Usuario que actualizó | Máx. 50 caracteres |
| `file_name` | string | Nombre del archivo | Máx. 100 caracteres |

## Casos de Uso Comunes

### 1. Crear un Nuevo Camión

```bash
curl -X POST "http://localhost:8000/api/v1/trucks" \
  -H "Content-Type: application/json" \
  -d '{
    "id_empresa": 1,
    "id_warehouse": 1,
    "ship_date": "2025-06-26",
    "carrier": "Transporte ABC S.A.",
    "load_number": "LOAD-2025-001",
    "estatus": 1,
    "update_user": "admin"
  }'
```

### 2. Buscar Camiones por Fecha

```bash
curl -X GET "http://localhost:8000/api/v1/trucks?date_from=2025-06-01&date_to=2025-06-30" \
  -H "accept: application/json"
```

### 3. Actualizar Estado de un Camión

```bash
curl -X PUT "http://localhost:8000/api/v1/trucks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "estatus": 2,
    "update_user": "admin"
  }'
```

### 4. Obtener Camiones de una Empresa

```bash
curl -X GET "http://localhost:8000/api/v1/trucks?id_empresa=1&limit=50" \
  -H "accept: application/json"
```

## Notas Importantes

1. **Paginación**: Use `skip` y `limit` para paginar resultados grandes
2. **Filtros**: Combine múltiples filtros para consultas más específicas
3. **Fechas**: Use formato YYYY-MM-DD para fechas
4. **Horas**: Use formato HH:MM:SS para horas
5. **IDs**: Los IDs deben ser números enteros positivos
6. **Campos opcionales**: Todos los campos son opcionales en creación y actualización

## Errores Comunes

### Error de Validación (422)

```json
{
  "detail": [
    {
      "loc": ["body", "ship_date"],
      "msg": "invalid date format",
      "type": "value_error.date"
    }
  ]
}
```

### Error de Recurso No Encontrado (404)

```json
{
  "detail": "Truck not found"
}
```

### Error Interno del Servidor (500)

```json
{
  "detail": "Error interno del servidor: [descripción del error]"
}
```

## Swagger UI

Para acceder a la documentación interactiva de Swagger, visite:

```
http://localhost:8000/docs
```

Esto proporciona una interfaz web interactiva para probar todos los endpoints del módulo de camiones. 