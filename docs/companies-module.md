# Módulo de Empresas - OneSite

## Descripción
El módulo de empresas permite gestionar las diferentes empresas que utilizan el sistema OneSite. Cada empresa puede tener sus propios datos, configuraciones y usuarios asociados.

## Características Principales

### Backend (FastAPI + SQL Server)

#### Modelo de Datos
- **Servidor**: SATURNO13
- **Base de datos**: AnalysisDW
- **Esquema**: TheEliteGroup_Parameters
- **Tabla**: Companies
- **Campos**:
  - `id`: Identificador único (INT, AUTO_INCREMENT)
  - `name`: Nombre de la empresa (NVARCHAR(255))
  - `code`: Código de la empresa (NVARCHAR(50))
  - `description`: Descripción opcional (TEXT)
  - `is_active`: Estado activo/inactivo (BIT)
  - `created_at`: Fecha de creación (DATETIME)
  - `updated_at`: Fecha de última actualización (DATETIME)

#### Endpoints API

##### GET /api/v1/companies/
Obtiene una lista paginada de empresas.

**Parámetros de consulta**:
- `skip`: Número de registros a omitir (default: 0)
- `limit`: Número máximo de registros (default: 100, max: 1000)
- `active_only`: Solo empresas activas (default: true)

**Respuesta**:
```json
{
  "companies": [
    {
      "id": 1,
      "name": "Elite Flower",
      "code": "ELF",
      "description": "Empresa líder en exportación de flores",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 5
}
```

##### GET /api/v1/companies/active
Obtiene todas las empresas activas (sin paginación).

**Respuesta**:
```json
[
  {
    "id": 1,
    "name": "Elite Flower",
    "code": "ELF",
    "is_active": true
  }
]
```

##### GET /api/v1/companies/{company_id}
Obtiene una empresa específica por su ID.

##### POST /api/v1/companies/
Crea una nueva empresa.

**Body**:
```json
{
  "name": "Nueva Empresa",
  "code": "NEM",
  "description": "Descripción de la empresa",
  "is_active": true
}
```

##### PUT /api/v1/companies/{company_id}
Actualiza una empresa existente.

##### DELETE /api/v1/companies/{company_id}
Elimina una empresa (soft delete - marca como inactiva).

#### Operaciones CRUD
- **Crear**: Validación de código único
- **Leer**: Con paginación y filtros
- **Actualizar**: Validación de código único
- **Eliminar**: Soft delete (marca como inactiva)

### Frontend (Angular)

#### Componentes
- **SidebarComponent**: Selector de empresas en el sidebar
- **CompanyService**: Servicio para consumir la API

#### Funcionalidades
- **Selector de empresas**: Dropdown en el sidebar
- **Estado de carga**: Indicador visual durante la carga
- **Manejo de errores**: Mensajes de error amigables
- **Persistencia**: Guarda la empresa seleccionada en localStorage
- **Responsive**: Adapta el selector según el estado colapsado/expandido

#### Estados del Selector
1. **Cargando**: Muestra "Cargando empresas..."
2. **Error**: Muestra mensaje de error
3. **Normal**: Muestra el dropdown con las empresas
4. **Colapsado**: Muestra solo el nombre de la empresa seleccionada

## Instalación y Configuración

### 1. Base de Datos
El módulo utiliza la tabla existente en el servidor SATURNO13:
- **Servidor**: SATURNO13
- **Base de datos**: AnalysisDW
- **Esquema**: TheEliteGroup_Parameters
- **Tabla**: Companies

Para verificar la conexión, ejecutar:
```bash
python test_companies_connection.py
```

### 2. Backend
Los archivos ya están creados:
- `backend/app/models/company.py`
- `backend/app/schemas/company.py`
- `backend/app/crud/crud_company.py`
- `backend/app/api/v1/endpoints/companies.py`

### 3. Frontend
Los archivos ya están creados:
- `frontend/src/app/core/models/company.model.ts`
- `frontend/src/app/core/services/company.service.ts`
- Actualizado `frontend/src/app/shared/components/sidebar/sidebar.component.ts`

## Uso

### Seleccionar Empresa
1. El usuario ve el selector de empresas en el sidebar
2. Al hacer clic, se despliega la lista de empresas activas
3. Al seleccionar una empresa, se actualiza el estado global
4. La selección se guarda en localStorage

### Gestión de Empresas (Admin)
1. Acceder a los endpoints de la API
2. Crear, actualizar o eliminar empresas
3. Ver lista paginada de todas las empresas

## Seguridad
- Validación de datos en frontend y backend
- Códigos únicos para evitar duplicados
- Soft delete para mantener integridad referencial
- Autenticación requerida para operaciones CRUD

## Mantenimiento
- Índices en la base de datos para optimizar consultas
- Trigger para actualizar automáticamente `updated_at`
- Logs de errores en el frontend
- Documentación Swagger/OpenAPI automática

## Próximas Mejoras
- [ ] Interfaz de administración de empresas
- [ ] Filtros avanzados en la lista
- [ ] Exportación de datos
- [ ] Auditoría de cambios
- [ ] Integración con módulo de permisos por empresa 