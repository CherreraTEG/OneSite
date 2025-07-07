# 🔴 Configuración de Redis para OneSite

## 📋 **Requisitos Previos**
- Windows 10/11 o Windows Server
- PowerShell con permisos de administrador
- Chocolatey (recomendado para instalación)

## 🚀 **Instalación de Redis en Windows**

### **Opción 1: Usando Chocolatey (Recomendado)**

```powershell
# Instalar Chocolatey si no está instalado
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Redis
choco install redis-64

# Iniciar servicio de Redis
Start-Service Redis
```

### **Opción 2: Instalación Manual**

1. **Descargar Redis para Windows:**
   - Visitar: https://github.com/microsoftarchive/redis/releases
   - Descargar la versión más reciente (Redis-x64-xxx.msi)

2. **Instalar Redis:**
   ```powershell
   # Ejecutar el instalador
   msiexec /i Redis-x64-xxx.msi /quiet
   ```

3. **Configurar como servicio:**
   ```powershell
   # Navegar al directorio de Redis
   cd "C:\Program Files\Redis"
   
   # Instalar como servicio
   redis-server --service-install redis.windows.conf
   
   # Iniciar servicio
   Start-Service Redis
   ```

## ⚙️ **Configuración de Redis**

### **Archivo de Configuración (redis.windows.conf)**

```conf
# Configuración básica
port 6379
bind 127.0.0.1
timeout 300
tcp-keepalive 60

# Configuración de memoria
maxmemory 256mb
maxmemory-policy allkeys-lru

# Configuración de persistencia
save 900 1
save 300 10
save 60 10000

# Configuración de seguridad
requirepass OneSiteRedis2024!

# Configuración de logging
loglevel notice
logfile "C:\Program Files\Redis\redis.log"

# Configuración de base de datos
databases 16
```

### **Configurar Variables de Entorno**

Actualizar el archivo `.env` del backend:

```env
# Configuración de Redis para rate limiting
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=OneSiteRedis2024!
```

## 🔧 **Verificación de Instalación**

### **Probar Conexión Redis**

```powershell
# Conectar a Redis CLI
redis-cli

# Autenticarse
AUTH OneSiteRedis2024!

# Probar comandos básicos
PING
SET test "OneSite Redis OK"
GET test
DEL test
QUIT
```

### **Verificar Servicio**

```powershell
# Verificar estado del servicio
Get-Service Redis

# Verificar puerto
netstat -an | findstr 6379
```

## 📊 **Configuración para Rate Limiting**

### **Estructura de Datos en Redis**

```
# Rate limiting por IP
rate_limit:ip:192.168.1.100 -> [timestamp1, timestamp2, ...]

# Rate limiting por usuario
rate_limit:user:admin -> [timestamp1, timestamp2, ...]

# Blacklist de tokens
blacklist:token_hash -> expiration_timestamp

# Bloqueo de cuentas
lockout:user:admin:ip:192.168.1.100 -> lockout_end_timestamp
```

### **Comandos de Mantenimiento**

```powershell
# Limpiar datos expirados
redis-cli -a OneSiteRedis2024! FLUSHDB

# Ver estadísticas
redis-cli -a OneSiteRedis2024! INFO

# Monitorear comandos en tiempo real
redis-cli -a OneSiteRedis2024! MONITOR
```

## 🔒 **Configuración de Seguridad**

### **Firewall**

```powershell
# Permitir Redis en el firewall (solo localhost)
New-NetFirewallRule -DisplayName "Redis OneSite" -Direction Inbound -Protocol TCP -LocalPort 6379 -Action Allow -Profile Private
```

### **Configuración de Red**

```conf
# En redis.windows.conf
bind 127.0.0.1
protected-mode yes
```

## 📈 **Monitoreo y Métricas**

### **Script de Monitoreo**

```powershell
# Crear script de monitoreo
@"
@echo off
echo ========================================
echo    Monitoreo Redis - OneSite
echo ========================================
echo.

redis-cli -a OneSiteRedis2024! INFO | findstr "connected_clients\|used_memory\|total_commands_processed"

echo.
echo ========================================
"@ > monitor-redis.bat
```

### **Métricas Importantes**

- `connected_clients`: Clientes conectados
- `used_memory`: Memoria utilizada
- `total_commands_processed`: Comandos procesados
- `keyspace_hits`: Aciertos en cache
- `keyspace_misses`: Fallos en cache

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

1. **Servicio no inicia:**
   ```powershell
   # Verificar logs
   Get-EventLog -LogName Application -Source Redis
   
   # Reinstalar servicio
   redis-server --service-uninstall
   redis-server --service-install redis.windows.conf
   ```

2. **Error de conexión:**
   ```powershell
   # Verificar puerto
   netstat -an | findstr 6379
   
   # Verificar firewall
   Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Redis*"}
   ```

3. **Problemas de memoria:**
   ```powershell
   # Verificar uso de memoria
   redis-cli -a OneSiteRedis2024! INFO memory
   
   # Limpiar cache
   redis-cli -a OneSiteRedis2024! FLUSHALL
   ```

## 📝 **Comandos Útiles**

```powershell
# Iniciar/Detener servicio
Start-Service Redis
Stop-Service Redis
Restart-Service Redis

# Verificar estado
Get-Service Redis

# Ver logs
Get-Content "C:\Program Files\Redis\redis.log" -Tail 50

# Backup de configuración
Copy-Item "C:\Program Files\Redis\redis.windows.conf" "C:\backup\redis.windows.conf.backup"
```

## ✅ **Verificación Final**

```powershell
# Script de verificación completa
@"
echo Verificando instalacion de Redis...
echo.

echo 1. Estado del servicio:
Get-Service Redis

echo.
echo 2. Puerto 6379:
netstat -an | findstr 6379

echo.
echo 3. Conexion Redis:
redis-cli -a OneSiteRedis2024! PING

echo.
echo 4. Configuracion:
redis-cli -a OneSiteRedis2024! CONFIG GET maxmemory

echo.
echo ✅ Verificacion completada
"@ > verify-redis.ps1
```

---

**Nota:** Esta configuración está optimizada para OneSite y incluye todas las configuraciones de seguridad necesarias para rate limiting y blacklist de tokens. 