# 📋 Guía de Permisos de Empresas - OneSite

## 🎯 Funcionalidad Implementada

El sistema ahora valida que los usuarios solo vean las empresas a las que tienen permisos específicos asignados.

### ✅ **Comportamiento Actual:**

1. **Usuario con empresas asignadas**: Ve solo las empresas activas que tienen en la tabla `user_company_permission`
2. **Usuario sin empresas asignadas**: Ve el mensaje "No tienes empresas asignadas"
3. **Usuario no autenticado**: No ve ninguna empresa

## 🗄️ Estructura de Base de Datos

### Tabla `user_company_permission`
```sql
CREATE TABLE user_company_permission (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,           -- ID del usuario (FK a tabla user)
    company_id INT NOT NULL         -- ID de la empresa (FK a Companies.id_Company)
);
```

### Relaciones:
- `user_id` → `user.id` (Base de datos principal OneSite)
- `company_id` → `Companies.id_Company` (Base de datos SATURNO13)

## 🔧 Configuración de Permisos

### 1. **Verificar usuarios disponibles:**
```sql
SELECT id, username, email FROM user;
```

### 2. **Verificar empresas activas:**
```sql
SELECT 
    id_Company, 
    Company, 
    BU, 
    Estado_Cargue 
FROM TheEliteGroup_Parameters.Companies 
WHERE Estado_Cargue = 1;
```

### 3. **Asignar permisos a un usuario:**
```sql
-- Ejemplo: Asignar empresas 1 y 2 al usuario 1
INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 1);
INSERT INTO user_company_permission (user_id, company_id) VALUES (1, 2);
```

### 4. **Ver permisos existentes:**
```sql
SELECT 
    ucp.user_id,
    u.username,
    ucp.company_id,
    c.Company,
    c.BU
FROM user_company_permission ucp
LEFT JOIN user u ON ucp.user_id = u.id  
LEFT JOIN TheEliteGroup_Parameters.Companies c ON ucp.company_id = c.id_Company;
```

## 🧪 Pruebas

### **Caso 1: Usuario con empresas asignadas**
1. Insertar permisos en `user_company_permission`
2. Hacer login con ese usuario
3. **Resultado esperado**: Ve solo las empresas asignadas en el selector

### **Caso 2: Usuario sin empresas asignadas**
1. Usuario existe en tabla `user` pero no tiene registros en `user_company_permission`
2. Hacer login con ese usuario
3. **Resultado esperado**: Ve mensaje "No tienes empresas asignadas"

### **Caso 3: Usuario no autenticado**
1. No hacer login o usar token inválido
2. **Resultado esperado**: No ve empresas, endpoint retorna 401

## 🔄 Flujo Técnico

### Backend (`/api/v1/companies/active`):
1. Verifica autenticación JWT ✅
2. Busca usuario en BD principal por `username` ✅
3. Hace JOIN entre `Company` y `UserCompanyPermission` ✅
4. Filtra solo empresas activas (`Estado_Cargue = 1`) ✅
5. Retorna lista (puede estar vacía) ✅

### Frontend (Sidebar):
1. Llama al endpoint con token JWT ✅
2. Si `companies.length > 0`: Muestra selector ✅
3. Si `companies.length === 0`: Muestra mensaje "No tienes empresas asignadas" ✅
4. Si error 401: Limpia estado sin mostrar error ✅

## 🎨 Estados del Selector

| Estado | Condición | Mostrar |
|--------|-----------|---------|
| 🔄 Cargando | `loading = true` | "Cargando empresas..." |
| ✅ Con empresas | `companies.length > 0` | Dropdown con empresas |
| ⚠️ Sin empresas | `companies.length === 0` | "No tienes empresas asignadas" |
| ❌ Error | `error !== null` | Mensaje de error específico |
| 🔒 No autenticado | `!isAuthenticated()` | Sin selector |

## 📝 Comandos Útiles

### Limpiar permisos de un usuario:
```sql
DELETE FROM user_company_permission WHERE user_id = 1;
```

### Asignar todas las empresas activas a un usuario:
```sql
INSERT INTO user_company_permission (user_id, company_id)
SELECT 1, id_Company 
FROM TheEliteGroup_Parameters.Companies 
WHERE Estado_Cargue = 1;
```

### Ver estadísticas:
```sql
SELECT 
    COUNT(*) as total_permisos,
    COUNT(DISTINCT user_id) as usuarios_con_permisos,
    COUNT(DISTINCT company_id) as empresas_asignadas
FROM user_company_permission;
```

## 🚀 URLs de Prueba

- **Frontend**: http://localhost:4200
- **API Docs**: http://localhost:8000/docs
- **Debug Endpoint**: http://localhost:8000/api/v1/companies/debug
- **Companies Endpoint**: http://localhost:8000/api/v1/companies/active

## 🔍 Debugging

Ver logs en:
- **Backend**: Terminal donde ejecutas uvicorn
- **Frontend**: Consola del navegador (F12 → Console)

Los logs muestran:
- Qué usuario está autenticado
- Cuántas empresas tiene asignadas
- Si se muestra el mensaje de "sin empresas"