# OneSite

## Descripción
Sistema OneSite desarrollado con Angular (Frontend) y FastAPI (Backend).

## Estructura del Proyecto
```
OneSite/
├── backend/           # Backend en FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints de la API
│   │   ├── core/     # Configuración central
│   │   ├── db/       # Configuración de base de datos
│   │   ├── models/   # Modelos SQLAlchemy
│   │   └── schemas/  # Esquemas Pydantic
│   ├── main.py
│   └── requirements.txt
│
└── frontend/         # Frontend en Angular
    ├── src/
    │   ├── app/
    │   │   ├── modules/           # Módulos de la aplicación
    │   │   │   ├── permisos/
    │   │   │   ├── costos/
    │   │   │   ├── camiones/
    │   │   │   └── auditoria/
    │   │   ├── shared/           # Componentes compartidos
    │   │   │   └── components/
    │   │   │       ├── button/
    │   │   │       ├── card/
    │   │   │       └── input/
    │   │   ├── app.module.ts
    │   │   └── app-routing.module.ts
    │   ├── assets/
    │   │   └── i18n/            # Archivos de traducción
    │   │       ├── es.json
    │   │       └── en.json
    │   └── styles.scss
    ├── angular.json
    └── package.json
```

## Requisitos
- Python 3.8+
- Node.js 16+
- SQL Server
- Git

## Instalación

### Backend
1. Navegar al directorio del backend
```bash
cd backend
```

2. Crear y activar entorno virtual
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
Crear un archivo `.env` en la carpeta backend con las siguientes variables:
```env
# Configuración de la base de datos
DB_SERVER=tu_servidor
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

# Configuración de seguridad
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de CORS
CORS_ORIGINS=https://teg.1sitesoft.com
CORS_CREDENTIALS=True
CORS_METHODS=*
CORS_HEADERS=*
```

### Frontend
1. Navegar al directorio del frontend
```bash
cd frontend
```

2. Instalar dependencias
```bash
npm install
```

## Ejecución

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
ng serve
```

## Documentación

### API
La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Módulos
1. **Permisos**
   - Gestión de permisos del sistema
   - Endpoints:
     - GET /api/v1/permisos
     - POST /api/v1/permisos
     - GET /api/v1/permisos/{id}
     - PUT /api/v1/permisos/{id}
     - DELETE /api/v1/permisos/{id}

2. **Costos** (En desarrollo)
3. **Camiones** (En desarrollo)
4. **Auditoría** (En desarrollo)

### Base de Datos
Ver [documentación de la base de datos](docs/database.md)

## Seguridad
- Autenticación mediante JWT
- CORS configurado para dominio específico
- Variables de entorno para datos sensibles
- HTTPS en producción

## Despliegue
El sistema será desplegado en AWS bajo el dominio teg.1sitesoft.com

## Contribución
1. Crear una rama para la nueva funcionalidad
2. Realizar los cambios necesarios
3. Crear un Pull Request
4. Esperar la revisión y aprobación

## Licencia
[Incluir información de licencia] 