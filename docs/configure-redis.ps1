# Script para configurar Redis para OneSite
# Ejecutar como Administrador

Write-Host "Configurando Redis para OneSite..." -ForegroundColor Green

# Verificar que estamos ejecutando como administrador
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Este script debe ejecutarse como Administrador" -ForegroundColor Red
    exit 1
}

# Detener el servicio de Redis
Write-Host "Deteniendo servicio de Redis..." -ForegroundColor Yellow
Stop-Service Redis -Force -ErrorAction SilentlyContinue

# Crear configuración optimizada para OneSite
$redisConfig = @"
# Configuracion Redis para OneSite
# Archivo: C:\Program Files\Redis\redis.windows.conf

# Configuracion de red
port 6379
bind 127.0.0.1
timeout 300
tcp-keepalive 60

# Configuracion de memoria
maxmemory 256mb
maxmemory-policy allkeys-lru

# Configuracion de persistencia
save 900 1
save 300 10
save 60 10000

# Configuracion de seguridad
requirepass OneSiteRedis2024!

# Configuracion de logging
loglevel notice
logfile "C:\Program Files\Redis\redis.log"

# Configuracion de base de datos
databases 16

# Configuracion de rendimiento
tcp-backlog 511
always-show-logo no

# Configuracion de snapshots
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./

# Configuracion de replicacion
replica-serve-stale-data yes
replica-read-only yes

# Configuracion de seguridad adicional
protected-mode yes

# Configuracion de clientes
maxclients 10000

# Configuracion de timeout
timeout 0

# Configuracion de logging
loglevel notice
logfile "C:\Program Files\Redis\redis.log"
syslog-enabled no
syslog-ident redis
syslog-facility local0

# Configuracion de notificaciones
notify-keyspace-events ""

# Configuracion de hash
hash-max-ziplist-entries 512
hash-max-ziplist-value 64

# Configuracion de listas
list-max-ziplist-size -2
list-compress-depth 0

# Configuracion de sets
set-max-intset-entries 512

# Configuracion de sorted sets
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Configuracion de hiperloglog
hll-sparse-max-bytes 3000

# Configuracion de streams
stream-node-max-bytes 4096
stream-node-max-entries 100

# Configuracion de activerehashing
activerehashing yes

# Configuracion de client-output-buffer-limit
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# Configuracion de hz
hz 10

# Configuracion de aof-rewrite-incremental-fsync
aof-rewrite-incremental-fsync yes

# Configuracion de rdb-save-incremental-fsync
rdb-save-incremental-fsync yes
"@

# Guardar configuración
$configPath = "C:\Program Files\Redis\redis.windows.conf"
try {
    Set-Content -Path $configPath -Value $redisConfig -Encoding UTF8 -Force
    Write-Host "Configuracion guardada exitosamente" -ForegroundColor Green
} catch {
    Write-Host "Error al guardar configuracion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Reiniciar el servicio de Redis
Write-Host "Reiniciando servicio de Redis..." -ForegroundColor Yellow
try {
    Start-Service Redis
    Write-Host "Servicio de Redis reiniciado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "Error al reiniciar servicio: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Configurar firewall
Write-Host "Configurando firewall..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Redis OneSite" -Direction Inbound -Protocol TCP -LocalPort 6379 -Action Allow -Profile Private -ErrorAction SilentlyContinue
    Write-Host "Firewall configurado" -ForegroundColor Green
} catch {
    Write-Host "Advertencia: No se pudo configurar firewall automaticamente" -ForegroundColor Yellow
}

# Verificar configuración
Write-Host "Verificando configuracion..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

$service = Get-Service Redis
if ($service.Status -eq "Running") {
    Write-Host "Redis esta ejecutandose correctamente" -ForegroundColor Green
} else {
    Write-Host "Error: Redis no esta ejecutandose" -ForegroundColor Red
    exit 1
}

# Probar conexión
Write-Host "Probando conexion Redis..." -ForegroundColor Yellow
try {
    $result = & "C:\Program Files\Redis\redis-cli.exe" -a "OneSiteRedis2024!" PING
    if ($result -eq "PONG") {
        Write-Host "Conexion Redis exitosa" -ForegroundColor Green
    } else {
        Write-Host "Error en conexion Redis" -ForegroundColor Red
    }
} catch {
    Write-Host "Error al probar conexion: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Configuracion de Redis completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Configuracion para OneSite:" -ForegroundColor Cyan
Write-Host "   Host: localhost" -ForegroundColor White
Write-Host "   Puerto: 6379" -ForegroundColor White
Write-Host "   Contrasena: OneSiteRedis2024!" -ForegroundColor White
Write-Host ""
Write-Host "Comandos utiles:" -ForegroundColor Cyan
Write-Host "   Iniciar: Start-Service Redis" -ForegroundColor White
Write-Host "   Detener: Stop-Service Redis" -ForegroundColor White
Write-Host "   Estado: Get-Service Redis" -ForegroundColor White
Write-Host "   CLI: redis-cli -a OneSiteRedis2024!" -ForegroundColor White
Write-Host ""
Write-Host "Recuerda actualizar el archivo .env del backend con:" -ForegroundColor Yellow
Write-Host "   REDIS_HOST=localhost" -ForegroundColor White
Write-Host "   REDIS_PORT=6379" -ForegroundColor White
Write-Host "   REDIS_PASSWORD=OneSiteRedis2024!" -ForegroundColor White 