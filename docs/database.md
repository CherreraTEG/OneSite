# Documentación de la Base de Datos

## Estructura de la Base de Datos

### Tabla: permisos
Tabla para almacenar los permisos del sistema.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | Integer | Identificador único del permiso (PK) |
| nombre | String(100) | Nombre del permiso |
| descripcion | String(255) | Descripción detallada del permiso |
| activo | Boolean | Estado del permiso |
| fecha_creacion | DateTime | Fecha de creación del registro |
| fecha_actualizacion | DateTime | Fecha de última actualización |

### Índices
- PK_permisos (id)
- IX_permisos_nombre (nombre)

### Restricciones
- nombre: NOT NULL
- activo: DEFAULT TRUE

## Conexión
La conexión a la base de datos se realiza mediante SQLAlchemy con el driver pymssql para SQL Server.

### Configuración
Las variables de conexión se configuran en el archivo `.env` del backend:
```env
DB_SERVER=tu_servidor
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
```

### URL de Conexión
```
mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}
```

## Migraciones
Las migraciones de base de datos se manejarán con Alembic (pendiente de implementar).

## Backup
Se recomienda realizar backups diarios de la base de datos.

## Mantenimiento
- Revisión periódica de índices
- Limpieza de registros obsoletos
- Monitoreo de rendimiento

## Diagrama ER
[Pendiente de agregar diagrama ER]

## Scripts de Base de Datos
Los scripts de creación y modificación de la base de datos se encuentran en:
- `backend/db/scripts/` (pendiente de crear) 