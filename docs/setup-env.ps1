# Script para configurar variables de entorno de OneSite
# Ejecutar desde el directorio docs

Write-Host "Configurando variables de entorno para OneSite..." -ForegroundColor Green

# Solicitar contraseña de base de datos
$dbPassword = Read-Host "Ingresa la contraseña de la base de datos (Mtadm)" -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

# Crear contenido del archivo .env
$envContent = @"
# Configuracion de la base de datos SQL Server
DB_SERVER=SATURNO13
DB_NAME=OneSiteDW
DB_USER=Mtadm
DB_PASSWORD=$dbPasswordPlain

# Configuracion de seguridad JWT
SECRET_KEY=OneSite2024-Super-Secret-Key-Elite-Flower-32-Chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Configuracion de Active Directory
AD_SERVER=10.50.5.200
AD_PORT=636
AD_USE_SSL=true
AD_BASE_DN=DC=ELITE,DC=local
AD_DOMAIN=elite.local

# Configuracion de seguridad
RATE_LIMIT_PER_MINUTE=5
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15

# Configuracion CORS
CORS_ORIGINS=["https://teg.1sitesoft.com", "http://localhost:4200"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["Authorization", "Content-Type", "X-Requested-With"]

# Configuracion de Redis para rate limiting
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=OneSiteRedis2024!

# Configuracion de logging
LOG_LEVEL=INFO
LOG_FILE=onesite.log

# Configuracion del entorno
ENVIRONMENT=development
"@

# Guardar archivo .env
$envPath = "..\backend\.env"
try {
    Set-Content -Path $envPath -Value $envContent -Encoding UTF8
    Write-Host "Archivo .env creado exitosamente en backend/.env" -ForegroundColor Green
} catch {
    Write-Host "Error al crear archivo .env: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Configuracion completada!" -ForegroundColor Green
Write-Host "Archivo .env creado con la siguiente configuracion:" -ForegroundColor Cyan
Write-Host "   - Servidor BD: SATURNO13" -ForegroundColor White
Write-Host "   - Base de datos: OneSiteDW" -ForegroundColor White
Write-Host "   - Usuario: Mtadm" -ForegroundColor White
Write-Host "   - Servidor AD: 10.50.5.200" -ForegroundColor White
Write-Host "   - Dominio: elite.local" -ForegroundColor White
Write-Host "   - Redis: localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host "Ahora puedes iniciar el backend con: python -m uvicorn app.main:app --reload" -ForegroundColor Yellow 