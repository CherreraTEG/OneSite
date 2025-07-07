# 🌍 Gestión de Entornos - OneSite

## 📋 Resumen

OneSite soporta múltiples entornos (desarrollo, staging, producción) con configuraciones específicas para cada uno. Este documento explica cómo gestionar las configuraciones de entorno de forma segura y eficiente.

## 🏗️ Arquitectura de Entornos

### **Entornos Soportados**

| Entorno | Descripción | Archivo de Configuración |
|---------|-------------|-------------------------|
| **Development** | Desarrollo local | `backend/.env` |
| **Staging** | Pre-producción | `backend/.env.staging` |
| **Production** | Producción | `backend/.env.production` |

### **Diferencias por Entorno**

| Característica | Development | Staging | Production |
|----------------|-------------|---------|------------|
| **Logging** | DEBUG | INFO | WARNING |
| **CORS** | Amplio | Restringido | Estricto |
| **Rate Limiting** | Bajo (5/min) | Medio (10/min) | Alto (10/min) |
| **Debug** | Habilitado | Limitado | Deshabilitado |
| **Token Expiry** | 60 min | 30 min | 30 min |

## 🔧 Configuración Automática

### **Script de Gestión de Entornos**

Usa el script `setup_environment.py` para cambiar entre entornos:

```bash
# Ver entorno actual
python setup_environment.py

# Cambiar a desarrollo
python setup_environment.py development

# Cambiar a staging
python setup_environment.py staging

# Cambiar a producción
python setup_environment.py production
```

### **Ejemplo de Uso**

```bash
# Ver configuración actual
python setup_environment.py

# Cambiar a desarrollo
python setup_environment.py development

# El script copiará la configuración correspondiente a backend/.env
```

## 📁 Estructura de Archivos

```
OneSite/
├── backend/
│   ├── .env                    # Configuración activa
│   ├── .env.staging           # Configuración de staging
│   ├── .env.production        # Configuración de producción
│   └── env.production.example # Plantilla de producción
├── setup_environment.py       # Script de gestión
└── docs/
    └── environment-management.md
```

## 🔐 Seguridad por Entorno

### **Development**
- Contraseñas simples para desarrollo
- CORS amplio para testing
- Logging detallado
- Debug habilitado

### **Staging**
- Contraseñas intermedias
- CORS restringido a dominios específicos
- Logging moderado
- Debug limitado

### **Production**
- Contraseñas complejas y seguras
- CORS estricto solo a dominios de producción
- Logging mínimo
- Debug completamente deshabilitado

## 🚀 Despliegue en Producción

### **Opción 1: Variables de Entorno del Sistema (Recomendada)**

En el servidor de producción, configura las variables de entorno del sistema:

```bash
# Windows (PowerShell)
$env:ENVIRONMENT="production"
$env:DB_SERVER="prod-saturno13"
$env:DB_NAME="OnesiteDW_Prod"
$env:DB_USER="prod_onesite_user"
$env:DB_PASSWORD="prod_password_muy_segura"

# Linux/Mac
export ENVIRONMENT=production
export DB_SERVER=prod-saturno13
export DB_NAME=OnesiteDW_Prod
export DB_USER=prod_onesite_user
export DB_PASSWORD=prod_password_muy_segura
```

### **Opción 2: Archivo de Configuración**

1. Copia la plantilla de producción:
   ```bash
   cp backend/env.production.example backend/.env.production
   ```

2. Edita `backend/.env.production` con los valores reales de producción

3. Usa el script para aplicar la configuración:
   ```bash
   python setup_environment.py production
   ```

## 🔄 Migración entre Entornos

### **De Development a Staging**

1. Crear configuración de staging:
   ```bash
   cp backend/env.production.example backend/.env.staging
   ```

2. Editar `backend/.env.staging` con valores de staging

3. Aplicar configuración:
   ```bash
   python setup_environment.py staging
   ```

### **De Staging a Production**

1. Verificar configuración de staging
2. Crear configuración de producción:
   ```bash
   cp backend/env.production.example backend/.env.production
   ```

3. Editar con valores de producción
4. Aplicar configuración:
   ```bash
   python setup_environment.py production
   ```

## 🛡️ Mejores Prácticas

### **Seguridad**

1. **Nunca** commits archivos `.env` con contraseñas reales
2. Usa variables de entorno del sistema en producción
3. Rota las contraseñas regularmente
4. Usa diferentes usuarios de base de datos por entorno

### **Configuración**

1. Mantén plantillas actualizadas
2. Documenta cambios en configuración
3. Prueba configuraciones antes de aplicar
4. Usa el script de gestión para cambios

### **Monitoreo**

1. Verifica logs por entorno
2. Monitorea conexiones a bases de datos
3. Revisa rate limiting y seguridad
4. Valida CORS y acceso

## 🔍 Verificación de Configuración

### **Verificar Entorno Actual**

```bash
python setup_environment.py
```

### **Verificar Conexiones**

```bash
# Probar conexión a base principal
python test_companies_connection.py

# Probar múltiples bases
python test_three_databases_corrected.py
```

### **Verificar Variables de Entorno**

```python
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

print(f"Entorno: {os.getenv('ENVIRONMENT')}")
print(f"Servidor: {os.getenv('DB_SERVER')}")
print(f"Base de datos: {os.getenv('DB_NAME')}")
```

## 🚨 Troubleshooting

### **Problema: Configuración no se aplica**

**Solución:**
1. Verificar que el archivo existe
2. Verificar permisos de archivo
3. Reiniciar la aplicación

### **Problema: Conexión a base de datos falla**

**Solución:**
1. Verificar credenciales
2. Verificar conectividad de red
3. Verificar firewall
4. Probar con script de conexión

### **Problema: CORS errors**

**Solución:**
1. Verificar configuración CORS_ORIGINS
2. Verificar que el dominio esté incluido
3. Verificar configuración del frontend

## 📞 Soporte

Para problemas con configuración de entornos:

1. Revisar logs de la aplicación
2. Verificar archivos de configuración
3. Probar conexiones con scripts de test
4. Consultar este documento
5. Contactar al equipo de desarrollo

---

**Última actualización:** Diciembre 2024  
**Versión:** 1.0  
**Autor:** Equipo OneSite 