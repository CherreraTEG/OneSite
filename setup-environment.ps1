# =============================================================================
# Script de Gestión de Entornos - OneSite (PowerShell)
# =============================================================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("development", "staging", "production", "show")]
    [string]$Environment = "show"
)

# Configuración de colores
$Host.UI.RawUI.ForegroundColor = "Cyan"
Write-Host "🔧 Gestor de Entornos - OneSite (PowerShell)" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Función para mostrar el entorno actual
function Show-CurrentEnvironment {
    Write-Host "🌍 ENTORNO ACTUAL" -ForegroundColor Yellow
    Write-Host "==============================" -ForegroundColor Yellow
    
    try {
        # Cargar variables de entorno del archivo .env
        if (Test-Path "backend\.env") {
            $envContent = Get-Content "backend\.env" | Where-Object { $_ -match "^[^#]" -and $_ -match "=" }
            
            $environment = ($envContent | Where-Object { $_ -match "ENVIRONMENT=" } | ForEach-Object { $_.Split("=")[1] }) -replace '"', ''
            $dbServer = ($envContent | Where-Object { $_ -match "DB_SERVER=" } | ForEach-Object { $_.Split("=")[1] }) -replace '"', ''
            $dbName = ($envContent | Where-Object { $_ -match "DB_NAME=" } | ForEach-Object { $_.Split("=")[1] }) -replace '"', ''
            
            Write-Host "📋 Entorno: $environment" -ForegroundColor White
            Write-Host "📡 Servidor: $dbServer" -ForegroundColor White
            Write-Host "🗄️  Base de datos: $dbName" -ForegroundColor White
        } else {
            Write-Host "❌ No se encontró archivo backend\.env" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error al leer configuración: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Función para configurar entorno
function Set-Environment {
    param([string]$EnvType)
    
    Write-Host "🔧 Configurando entorno: $($EnvType.ToUpper())" -ForegroundColor Yellow
    Write-Host "==================================================" -ForegroundColor Yellow
    
    $configs = @{
        "development" = @{
            "env_file" = "backend\.env"
            "description" = "Desarrollo local"
            "features" = @("Logging detallado", "CORS amplio", "Rate limiting bajo", "Debug habilitado")
        }
        "staging" = @{
            "env_file" = "backend\.env.staging"
            "description" = "Pre-producción"
            "features" = @("Logging moderado", "CORS restringido", "Rate limiting medio", "Debug limitado")
        }
        "production" = @{
            "env_file" = "backend\.env.production"
            "description" = "Producción"
            "features" = @("Logging mínimo", "CORS estricto", "Rate limiting alto", "Debug deshabilitado")
        }
    }
    
    if (-not $configs.ContainsKey($EnvType)) {
        Write-Host "❌ Entorno '$EnvType' no válido" -ForegroundColor Red
        Write-Host "Entornos disponibles: development, staging, production" -ForegroundColor Yellow
        return $false
    }
    
    $config = $configs[$EnvType]
    
    Write-Host "📋 Descripción: $($config.description)" -ForegroundColor White
    Write-Host "📁 Archivo: $($config.env_file)" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Características:" -ForegroundColor White
    foreach ($feature in $config.features) {
        Write-Host "   ✅ $feature" -ForegroundColor Green
    }
    
    # Verificar si existe el archivo de configuración
    if (-not (Test-Path $config.env_file)) {
        Write-Host ""
        Write-Host "⚠️  El archivo $($config.env_file) no existe" -ForegroundColor Yellow
        $response = Read-Host "¿Quieres crear la configuración para este entorno? (y/n)"
        
        if ($response -match "^[yY]") {
            return New-EnvironmentConfig -Environment $EnvType
        } else {
            Write-Host "❌ Configuración cancelada" -ForegroundColor Red
            return $false
        }
    }
    
    # Copiar configuración al .env principal
    try {
        Copy-Item $config.env_file "backend\.env" -Force
        Write-Host ""
        Write-Host "✅ Configuración de $EnvType aplicada" -ForegroundColor Green
        Write-Host "📁 Copiado: $($config.env_file) → backend\.env" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error al copiar configuración: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Función para crear nueva configuración
function New-EnvironmentConfig {
    param([string]$Environment)
    
    Write-Host ""
    Write-Host "🔧 Creando configuración para $Environment..." -ForegroundColor Yellow
    
    if ($Environment -eq "development") {
        return New-DevelopmentConfig
    } elseif ($Environment -eq "staging") {
        return New-StagingConfig
    } elseif ($Environment -eq "production") {
        return New-ProductionConfig
    } else {
        Write-Host "❌ Entorno '$Environment' no soportado" -ForegroundColor Red
        return $false
    }
}

# Función para crear configuración de desarrollo
function New-DevelopmentConfig {
    Write-Host "📝 Configurando entorno de DESARROLLO..." -ForegroundColor Yellow
    
    Write-Host ""
    Write-Host "🏠 BASE DE DATOS PRINCIPAL (OneSite):" -ForegroundColor Cyan
    $dbServer = Read-Host "Servidor [SATURNO13]"
    if (-not $dbServer) { $dbServer = "SATURNO13" }
    
    $dbName = Read-Host "Base de datos [OnesiteDW]"
    if (-not $dbName) { $dbName = "OnesiteDW" }
    
    $dbUser = Read-Host "Usuario [data_analysis_admin]"
    if (-not $dbUser) { $dbUser = "data_analysis_admin" }
    
    $dbPassword = Read-Host "Contraseña" -AsSecureString
    $dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))
    
    if (-not $dbPasswordPlain) {
        Write-Host "❌ La contraseña es obligatoria" -ForegroundColor Red
        return $false
    }
    
    # Crear contenido del archivo
    $envContent = @"
# =============================================================================
# CONFIGURACIÓN DE DESARROLLO - OneSite
# =============================================================================

# =============================================================================
# CONFIGURACIÓN DE ENTORNO
# =============================================================================
ENVIRONMENT=development
USE_SATURNO13_COMPANIES=true

# =============================================================================
# BASE DE DATOS PRINCIPAL (OneSite)
# =============================================================================
DB_SERVER=$dbServer
DB_NAME=$dbName
DB_USER=$dbUser
DB_PASSWORD=$dbPasswordPlain

# =============================================================================
# BASE DE DATOS SATURNO13 (TheEliteGroup)
# =============================================================================
SATURNO13_SERVER=SATURNO13
SATURNO13_DB=AnalysisDW
SATURNO13_USER=data_analysis_admin
SATURNO13_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc
SATURNO13_SCHEMA=TheEliteGroup_Parameters

# =============================================================================
# BASE DE DATOS JUPITER12MIA (EFLOWER_Reports)
# =============================================================================
JUPITER12MIA_SERVER=JUPITER12MIA
JUPITER12MIA_DB=EFLOWER_Reports
JUPITER12MIA_USER=data_analysis_admin
JUPITER12MIA_PASSWORD=Hg1y3m9VFJsNrzjw8brjbc

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD JWT
# =============================================================================
SECRET_KEY=dev-super-secret-key-2024-elite-group-development
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# =============================================================================
# CONFIGURACIÓN DE ACTIVE DIRECTORY
# =============================================================================
AD_SERVER=10.50.5.200
AD_PORT=636
AD_USE_SSL=true
AD_BASE_DN=DC=ELITE,DC=local
AD_DOMAIN=elite.local

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================
RATE_LIMIT_PER_MINUTE=5
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15

# =============================================================================
# CONFIGURACIÓN CORS
# =============================================================================
CORS_ORIGINS=["https://teg.1sitesoft.com", "http://localhost:4200", "http://127.0.0.1:4200"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["Authorization", "Content-Type", "X-Requested-With"]

# =============================================================================
# CONFIGURACIÓN DE REDIS
# =============================================================================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================
LOG_LEVEL=DEBUG
LOG_FILE=onesite.log
"@
    
    # Guardar archivo
    try {
        $envContent | Out-File -FilePath "backend\.env" -Encoding UTF8
        Write-Host "✅ Configuración de desarrollo creada" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Error al crear archivo: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Función para crear configuración de staging
function New-StagingConfig {
    Write-Host "📝 Configurando entorno de STAGING..." -ForegroundColor Yellow
    Write-Host "⚠️  Esta funcionalidad requiere configuración manual" -ForegroundColor Yellow
    Write-Host "   Copia backend\env.production.example a backend\.env.staging" -ForegroundColor White
    Write-Host "   y ajusta los valores según tu entorno de staging" -ForegroundColor White
    return $false
}

# Función para crear configuración de producción
function New-ProductionConfig {
    Write-Host "📝 Configurando entorno de PRODUCCIÓN..." -ForegroundColor Yellow
    Write-Host "⚠️  Esta funcionalidad requiere configuración manual" -ForegroundColor Yellow
    Write-Host "   Copia backend\env.production.example a backend\.env.production" -ForegroundColor White
    Write-Host "   y ajusta los valores según tu entorno de producción" -ForegroundColor White
    return $false
}

# Función para mostrar ayuda
function Show-Help {
    Write-Host "Uso: .\setup-environment.ps1 [development|staging|production|show]" -ForegroundColor White
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor White
    Write-Host "  development  - Entorno de desarrollo local" -ForegroundColor Cyan
    Write-Host "  staging      - Entorno de pre-producción" -ForegroundColor Cyan
    Write-Host "  production   - Entorno de producción" -ForegroundColor Cyan
    Write-Host "  show         - Mostrar entorno actual (por defecto)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ejemplo: .\setup-environment.ps1 development" -ForegroundColor White
}

# Lógica principal
if ($Environment -eq "show") {
    Show-CurrentEnvironment
} elseif ($Environment -in @("development", "staging", "production")) {
    Set-Environment -EnvType $Environment
} else {
    Show-Help
    Write-Host ""
    Show-CurrentEnvironment
}

Write-Host ""
Write-Host "✅ Script completado" -ForegroundColor Green 