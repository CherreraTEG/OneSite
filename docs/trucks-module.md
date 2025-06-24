# Módulo de Control de Camiones (Truck Control)

## Descripción
El módulo de Truck Control permite gestionar el control de camiones en los almacenes, incluyendo la creación, edición, visualización y búsqueda de registros de camiones por warehouse, carrier y fechas.

## Estructura de la Base de Datos

### Tabla: `trucks_control`

| Campo | Tipo | Descripción | Índice |
|-------|------|-------------|--------|
| `id` | bigint | Clave primaria autoincremental | PRIMARY KEY |
| `id_empresa` | int | ID de la empresa | ✓ |
| `id_warehouse` | int | ID del almacén | ✓ |
| `ship_date` | date | Fecha de envío | ✓ |
| `deliv_date` | date | Fecha de entrega | ✓ |
| `carrier` | nvarchar(200) | Transportista | ✓ |
| `customer_facility` | nvarchar(200) | Instalación del cliente | |
| `po` | nvarchar(200) | Orden de compra | ✓ |
| `qty` | float | Cantidad | |
| `estatus` | int | Estado del camión | ✓ |
| `time_in` | time(7) | Hora de entrada | |
| `door` | nvarchar(25) | Puerta | |
| `time_out` | time(7) | Hora de salida | |
| `comments` | nvarchar(1000) | Comentarios | |
| `pickup_location` | nvarchar(150) | Ubicación de recogida | |
| `load_number` | nvarchar(50) | Número de carga | ✓ |
| `id_customer` | int | ID del cliente | ✓ |
| `estado_cargue` | int | Estado de carga | |
| `update_date` | datetime | Fecha de actualización | ✓ |
| `update_user` | nvarchar(50) | Usuario que actualizó | |
| `file_name` | nvarchar(100) | Nombre del archivo | |

### Script SQL para Agregar Campo

```sql
-- Agregar el campo id_empresa a la tabla trucks_control
ALTER TABLE trucks.trucks_control ADD id_empresa int NULL;

-- Crear índice para el nuevo campo
CREATE INDEX idx_trucks_control_id_empresa ON trucks.trucks_control(id_empresa);

-- Índice compuesto para consultas por empresa y warehouse
CREATE INDEX idx_trucks_control_empresa_warehouse ON trucks.trucks_control(id_empresa, id_warehouse);
```

### Índices Optimizados

```sql
-- Índices principales para consultas frecuentes
CREATE INDEX idx_trucks_control_id_empresa ON trucks.trucks_control(id_empresa);
CREATE INDEX idx_trucks_control_id_warehouse ON trucks.trucks_control(id_warehouse);
CREATE INDEX idx_trucks_control_ship_date ON trucks.trucks_control(ship_date);
CREATE INDEX idx_trucks_control_deliv_date ON trucks.trucks_control(deliv_date);
CREATE INDEX idx_trucks_control_carrier ON trucks.trucks_control(carrier);
CREATE INDEX idx_trucks_control_id_customer ON trucks.trucks_control(id_customer);
CREATE INDEX idx_trucks_control_estatus ON trucks.trucks_control(estatus);
CREATE INDEX idx_trucks_control_load_number ON trucks.trucks_control(load_number);
CREATE INDEX idx_trucks_control_update_date ON trucks.trucks_control(update_date);
CREATE INDEX idx_trucks_control_po ON trucks.trucks_control(po);
CREATE INDEX idx_trucks_control_customer_facility ON trucks.trucks_control(customer_facility);

-- Índices compuestos para consultas complejas
CREATE INDEX idx_trucks_control_empresa_warehouse ON trucks.trucks_control(id_empresa, id_warehouse);
CREATE INDEX idx_trucks_control_empresa_warehouse_dates ON trucks.trucks_control(id_empresa, id_warehouse, ship_date, deliv_date);
CREATE INDEX idx_trucks_control_warehouse_dates ON trucks.trucks_control(id_warehouse, ship_date, deliv_date);
CREATE INDEX idx_trucks_control_warehouse_carrier_dates ON trucks.trucks_control(id_warehouse, carrier, ship_date, deliv_date);
```

## API Endpoints

### Base URL
```
/api/v1
```

### Endpoints Disponibles

#### 1. Obtener Lista de Camiones
```http
GET /trucks
```

**Parámetros de consulta:**
- `skip` (int, opcional): Número de registros a omitir (default: 0)
- `limit` (int, opcional): Número máximo de registros (default: 100)
- `id_empresa` (int, opcional): Filtrar por ID de empresa
- `id_warehouse` (int, opcional): Filtrar por ID de almacén
- `carrier` (string, opcional): Filtrar por transportista
- `date_from` (date, opcional): Fecha de inicio para filtro
- `date_to` (date, opcional): Fecha de fin para filtro
- `id_customer` (int, opcional): Filtrar por ID de cliente
- `estatus` (int, opcional): Filtrar por estado
- `load_number` (string, opcional): Filtrar por número de carga

**Ejemplo:**
```http
GET /api/v1/trucks?id_empresa=5&id_warehouse=1&carrier=ABC&date_from=2024-01-01&date_to=2024-01-31
```

#### 2. Obtener Camión por ID
```http
GET /trucks/{truck_id}
```

**Parámetros:**
- `truck_id` (int): ID del camión

#### 3. Crear Nuevo Camión
```http
POST /trucks
```

**Body (JSON):**
```json
{
  "id_empresa": 5,
  "id_warehouse": 1,
  "ship_date": "2024-01-15",
  "deliv_date": "2024-01-16",
  "carrier": "Transport Company",
  "customer_facility": "Customer Warehouse",
  "po": "PO123456",
  "qty": 100.5,
  "estatus": 1,
  "time_in": "08:30:00",
  "door": "A1",
  "time_out": "16:45:00",
  "comments": "Carga especial",
  "pickup_location": "Loading Dock 1",
  "load_number": "LN789",
  "id_customer": 5,
  "estado_cargue": 1,
  "update_user": "admin",
  "file_name": "truck_data.csv"
}
```

#### 4. Actualizar Camión
```http
PUT /trucks/{truck_id}
```

**Parámetros:**
- `truck_id` (int): ID del camión a actualizar

**Body:** Mismo formato que POST, pero solo los campos a actualizar

#### 5. Eliminar Camión
```http
DELETE /trucks/{truck_id}
```

**Parámetros:**
- `truck_id` (int): ID del camión a eliminar

#### 6. Obtener Camiones por Almacén y Fechas
```http
GET /trucks/warehouse/{id_warehouse}/dates
```

**Parámetros:**
- `id_warehouse` (int): ID del almacén
- `date_from` (date): Fecha de inicio
- `date_to` (date): Fecha de fin

#### 7. Obtener Camiones por Empresa y Almacén
```http
GET /trucks/empresa/{id_empresa}/warehouse/{id_warehouse}
```

**Parámetros:**
- `id_empresa` (int): ID de la empresa
- `id_warehouse` (int): ID del almacén

#### 8. Obtener Camiones por Empresa, Almacén y Fechas
```http
GET /trucks/empresa/{id_empresa}/warehouse/{id_warehouse}/dates
```

**Parámetros:**
- `id_empresa` (int): ID de la empresa
- `id_warehouse` (int): ID del almacén
- `date_from` (date): Fecha de inicio
- `date_to` (date): Fecha de fin

#### 9. Obtener Camiones por Almacén y Fechas
```http
GET /trucks/warehouse/{id_warehouse}/dates
```

**Parámetros:**
- `id_warehouse` (int): ID del almacén
- `date_from` (date): Fecha de inicio
- `date_to` (date): Fecha de fin

#### 10. Obtener Camiones por Transportista
```http
GET /trucks/carrier/{carrier}
```

**Parámetros:**
- `carrier` (string): Nombre del transportista

#### 11. Obtener Camión por Número de Carga
```http
GET /trucks/load/{load_number}
```

**Parámetros:**
- `load_number` (string): Número de carga

## Esquemas de Datos

### TruckBase
```python
class TruckBase(BaseModel):
    id_empresa: Optional[int] = None
    id_warehouse: Optional[int] = None
    ship_date: Optional[date] = None
    deliv_date: Optional[date] = None
    carrier: Optional[str] = None
    customer_facility: Optional[str] = None
    po: Optional[str] = None
    qty: Optional[float] = None
    estatus: Optional[int] = None
    time_in: Optional[time] = None
    door: Optional[str] = None
    time_out: Optional[time] = None
    comments: Optional[str] = None
    pickup_location: Optional[str] = None
    load_number: Optional[str] = None
    id_customer: Optional[int] = None
    estado_cargue: Optional[int] = None
    update_date: Optional[datetime] = None
    update_user: Optional[str] = None
    file_name: Optional[str] = None
```

### TruckCreate
Hereda de `TruckBase` para crear nuevos registros.

### TruckUpdate
Hereda de `TruckBase` para actualizar registros existentes.

### Truck
Hereda de `TruckBase` e incluye el campo `id` para respuestas completas.

## Operaciones CRUD

### Crear (Create)
```python
def create(self, db: Session, obj_in: TruckCreate) -> Truck:
    db_obj = Truck(**obj_in.dict(exclude_unset=True))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
```

### Leer (Read)
```python
def get(self, db: Session, truck_id: int) -> Optional[Truck]:
    return db.query(Truck).filter(Truck.id == truck_id).first()

def get_multi(self, db: Session, *, skip=0, limit=100, **filters) -> List[Truck]:
    query = db.query(Truck)
    # Aplicar filtros dinámicamente
    return query.offset(skip).limit(limit).all()
```

### Actualizar (Update)
```python
def update(self, db: Session, db_obj: Truck, obj_in: TruckUpdate) -> Truck:
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj
```

### Eliminar (Delete)
```python
def remove(self, db: Session, truck_id: int) -> Optional[Truck]:
    obj = db.query(Truck).get(truck_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
```

## Casos de Uso

### 1. Búsqueda por Empresa y Almacén
```python
# Obtener todos los camiones de la empresa 5 en el almacén 1
trucks = crud_truck.get_by_empresa_and_warehouse(
    db, 
    id_empresa=5, 
    id_warehouse=1
)
```

### 2. Búsqueda por Empresa, Almacén y Fechas
```python
# Obtener todos los camiones de la empresa 5 en el almacén 1 entre fechas específicas
trucks = crud_truck.get_by_empresa_warehouse_and_dates(
    db, 
    id_empresa=5, 
    id_warehouse=1, 
    date_from=date(2024, 1, 1), 
    date_to=date(2024, 1, 31)
)
```

### 3. Búsqueda por Almacén y Fechas
```python
# Obtener todos los camiones del almacén 1 entre el 1 y 31 de enero
trucks = crud_truck.get_by_warehouse_and_dates(
    db, 
    id_warehouse=1, 
    date_from=date(2024, 1, 1), 
    date_to=date(2024, 1, 31)
)
```

### 4. Búsqueda por Transportista
```python
# Obtener todos los camiones de un transportista específico
trucks = crud_truck.get_by_carrier(db, "ABC Transport")
```

### 5. Búsqueda por Número de Carga
```python
# Obtener un camión específico por su número de carga
truck = crud_truck.get_by_load_number(db, "LN789")
```

## Validaciones y Reglas de Negocio

1. **Campos Obligatorios**: Todos los campos son opcionales en la creación, pero se recomienda llenar los campos críticos como `id_warehouse`, `carrier`, y `ship_date`.

2. **Fechas**: Las fechas deben estar en formato ISO (YYYY-MM-DD).

3. **Horas**: Las horas deben estar en formato HH:MM:SS.

4. **Estados**: Los valores de `estatus` y `estado_cargue` son enteros que representan diferentes estados del camión.

5. **Auditoría**: Los campos `update_date` y `update_user` se pueden establecer automáticamente en el backend.

## Integración con Frontend

El módulo está diseñado para integrarse con el frontend Angular, proporcionando:

- Endpoints RESTful para todas las operaciones CRUD
- Filtrado avanzado por múltiples criterios
- Respuestas JSON estructuradas
- Manejo de errores HTTP estándar
- Soporte para paginación

## Próximos Pasos

1. **Implementar validaciones adicionales** en el backend
2. **Agregar autenticación y autorización** por roles
3. **Implementar logging** de todas las operaciones
4. **Crear reportes** y estadísticas
5. **Integrar con otros módulos** del sistema 