# Script de instalacion de Redis para Windows - OneSite
# Ejecutar como Administrador

Write-Host "Instalando Redis para OneSite..." -ForegroundColor Red
Write-Host ""

# Verificar si ya esta instalado
if (Test-Path "C:\Program Files\Redis\redis-server.exe") {
    Write-Host "Redis ya esta instalado en C:\Program Files\Redis\" -ForegroundColor Green
    exit 0
}

# Crear directorio temporal
$tempDir = "C:\temp\redis-install"
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force
}

Write-Host "Descargando Redis..." -ForegroundColor Yellow

# Descargar Redis (version estable para Windows)
$redisUrl = "https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi"
$redisFile = "$tempDir\Redis-x64-3.0.504.msi"

try {
    Invoke-WebRequest -Uri $redisUrl -OutFile $redisFile -UseBasicParsing
    Write-Host "Descarga completada" -ForegroundColor Green
} catch {
    Write-Host "Error al descargar Redis: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Alternativa: Descargar manualmente desde https://github.com/microsoftarchive/redis/releases" -ForegroundColor Yellow
    exit 1
}

Write-Host "Instalando Redis..." -ForegroundColor Yellow

# Instalar Redis silenciosamente
try {
    Start-Process msiexec.exe -Wait -ArgumentList "/i `"$redisFile`" /quiet /norestart"
    Write-Host "Instalacion completada" -ForegroundColor Green
} catch {
    Write-Host "Error durante la instalacion: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Configurar Redis
Write-Host "Configurando Redis..." -ForegroundColor Yellow

$redisConfigPath = "C:\Program Files\Redis\redis.windows.conf"
$redisConfig = @"
# Configuracion Redis para OneSite
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
"@

try {
    Set-Content -Path $redisConfigPath -Value $redisConfig -Encoding UTF8
    Write-Host "Configuracion guardada" -ForegroundColor Green
} catch {
    Write-Host "Error al guardar configuracion: $($_.Exception.Message)" -ForegroundColor Red
}

# Instalar como servicio
Write-Host "Instalando servicio de Redis..." -ForegroundColor Yellow

try {
    Set-Location "C:\Program Files\Redis"
    .\redis-server.exe --service-install $redisConfigPath
    Write-Host "Servicio instalado" -ForegroundColor Green
} catch {
    Write-Host "Error al instalar servicio: $($_.Exception.Message)" -ForegroundColor Red
}

# Iniciar servicio
Write-Host "Iniciando servicio de Redis..." -ForegroundColor Yellow

try {
    Start-Service Redis
    Write-Host "Servicio iniciado" -ForegroundColor Green
} catch {
    Write-Host "Error al iniciar servicio: $($_.Exception.Message)" -ForegroundColor Red
}

# Configurar firewall
Write-Host "Configurando firewall..." -ForegroundColor Yellow

try {
    New-NetFirewallRule -DisplayName "Redis OneSite" -Direction Inbound -Protocol TCP -LocalPort 6379 -Action Allow -Profile Private -ErrorAction SilentlyContinue
    Write-Host "Firewall configurado" -ForegroundColor Green
} catch {
    Write-Host "Advertencia: No se pudo configurar firewall automaticamente" -ForegroundColor Yellow
}

# Verificar instalacion
Write-Host "Verificando instalacion..." -ForegroundColor Yellow

$service = Get-Service Redis -ErrorAction SilentlyContinue
if ($service -and $service.Status -eq "Running") {
    Write-Host "Redis esta ejecutandose correctamente" -ForegroundColor Green
} else {
    Write-Host "Redis no esta ejecutandose" -ForegroundColor Red
}

# Limpiar archivos temporales
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}

Write-Host ""
Write-Host "Instalacion de Redis completada!" -ForegroundColor Green
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