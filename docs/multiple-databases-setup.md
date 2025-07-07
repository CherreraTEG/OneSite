# Configuración de Múltiples Bases de Datos - OneSite

## Descripción
Este documento explica cómo configurar OneSite para trabajar con múltiples bases de datos simultáneamente.

## Arquitectura de Bases de Datos

### Base de Datos Principal (OneSite)
- **Propósito**: Datos principales de la aplicación
- **Tablas**: users, trucks, permissions, etc.
- **Configuración**: Variables `DB_*`

### Base de Datos SATURNO13 (TheEliteGroup)
- **Propósito**: Datos existentes de TheEliteGroup
- **Tablas**: Companies (en esquema TheEliteGroup_Parameters)
- **Configuración**: Variables `SATURNO13_*`

## Configuración del Archivo .env

### Estructura Recomendada
```env
# =============================================================================
# CONFIGURACIÓN DE ENTORNO
# =============================================================================
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=true

# =============================================================================
# BASE DE DATOS PRINCIPAL (OneSite)
# =============================================================================
DB_SERVER=localhost
DB_NAME=onesite_db
DB_USER=sa
DB_PASSWORD=tu_contraseña_local

# =============================================================================
# BASE DE DATOS SATURNO13 (TheEliteGroup)
# =============================================================================
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
SATURNO13_USER=tu_usuario_saturno13
SATURNO13_PASSWORD=tu_contraseña_saturno13
SATURNO13_SCHEMA=TheEliteGroup_Parameters
```

### Variables de Configuración

#### Entorno
- `ENVIRONMENT`: development, staging, production
- `USE_SATURNO13_COMPANIES`: true/false para usar tabla de empresas de SATURNO13

#### Base Principal (OneSite)
- `DB_SERVER`: Servidor de la base de datos principal
- `DB_NAME`: Nombre de la base de datos principal
- `DB_USER`: Usuario de la base de datos principal
- `DB_PASSWORD`: Contraseña de la base de datos principal

#### Base SATURNO13 (TheEliteGroup)
- `SATURNO13_SERVER`: Servidor SATURNO13
- `SATURNO13_DB`: Base de datos AnalysisDW
- `SATURNO13_USER`: Usuario de SATURNO13
- `SATURNO13_PASSWORD`: Contraseña de SATURNO13
- `SATURNO13_SCHEMA`: Esquema TheEliteGroup_Parameters

## Métodos de Configuración

### 1. Configuración Automática (Recomendada)
```bash
python setup_multiple_databases.py
```
- Configuración interactiva
- Prueba automática de conexiones
- Crea archivo .env automáticamente

### 2. Configuración Manual
1. Copiar `backend/env.example` a `backend/.env`
2. Editar las variables según tu entorno
3. Ejecutar pruebas de conexión

### 3. Configuración Solo SATURNO13
```bash
python setup_saturno13_connection.py
```
- Para casos donde solo necesitas SATURNO13
- Configuración simplificada

## Gestión de Conexiones

### DatabaseManager
La aplicación usa un `DatabaseManager` que maneja múltiples conexiones:

```python
from app.db.databases import db_manager

# Obtener engine específico
engine = db_manager.get_engine('main')  # Base principal
engine = db_manager.get_engine('saturno13')  # SATURNO13

# Obtener sesión específica
session = db_manager.get_session('main')
session = db_manager.get_session('saturno13')
```

### Dependencies de FastAPI
```python
from app.db.databases import get_main_db, get_saturno13_db, get_companies_db

# Para base principal
def endpoint(db: Session = Depends(get_main_db)):
    pass

# Para SATURNO13
def endpoint(db: Session = Depends(get_saturno13_db)):
    pass

# Para empresas (automático según configuración)
def endpoint(db: Session = Depends(get_companies_db)):
    pass
```

## Casos de Uso

### Desarrollo Local
```env
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=true
DB_SERVER=localhost
DB_NAME=onesite_dev
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
```

### Staging
```env
ENVIRONMENT=staging
USE_SATURNO13_COMPANIES=true
DB_SERVER=staging-server
DB_NAME=onesite_staging
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
```

### Producción
```env
ENVIRONMENT=production
USE_SATURNO13_COMPANIES=true
DB_SERVER=prod-server
DB_NAME=onesite_prod
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
```

### Sin SATURNO13
```env
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=false
DB_SERVER=localhost
DB_NAME=onesite_db
# Variables SATURNO13_* no necesarias
```

## Verificación de Configuración

### Prueba de Conexiones
```bash
python test_companies_connection.py
```

### Verificación Manual
```python
from app.db.databases import db_manager

# Probar todas las conexiones
results = db_manager.test_connections()
print(results)
```

## Troubleshooting

### Error: Base de datos no configurada
- Verificar que todas las variables estén definidas en `.env`
- Comprobar credenciales de acceso

### Error: Conexión a SATURNO13 fallida
- Verificar conectividad de red
- Comprobar credenciales de SATURNO13
- Verificar que el esquema existe

### Error: Tabla Companies no encontrada
- Verificar que `SATURNO13_SCHEMA` sea correcto
- Comprobar que la tabla existe en el esquema

### Error: Múltiples conexiones
- Verificar que no haya conflictos de puertos
- Comprobar configuración de pool de conexiones

## Mejores Prácticas

### Seguridad
- Nunca committear archivos `.env` al repositorio
- Usar credenciales específicas por entorno
- Rotar contraseñas regularmente

### Rendimiento
- Configurar pool de conexiones apropiado
- Monitorear uso de conexiones
- Cerrar conexiones no utilizadas

### Mantenimiento
- Documentar cambios en configuración
- Probar conexiones después de cambios
- Mantener backups de configuración

## Próximas Mejoras
- [ ] Configuración por archivos separados (.env.development, .env.production)
- [ ] Encriptación de credenciales
- [ ] Configuración dinámica de conexiones
- [ ] Monitoreo automático de conexiones
- [ ] Failover automático entre bases de datos 