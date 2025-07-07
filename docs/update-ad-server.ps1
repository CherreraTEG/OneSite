# Script para actualizar AD_SERVER de IP a nombre DNS
# Ejecutar desde el directorio docs

Write-Host "Actualizando AD_SERVER de IP a nombre DNS..." -ForegroundColor Green

# Ruta del archivo .env
$envPath = "..\backend\.env"

# Verificar si existe el archivo
if (!(Test-Path $envPath)) {
    Write-Host "Error: No se encontro el archivo .env en backend/" -ForegroundColor Red
    Write-Host "Ejecuta primero: powershell -ExecutionPolicy Bypass -File setup-env.ps1" -ForegroundColor Yellow
    exit 1
}

# Leer el contenido actual
$content = Get-Content $envPath -Raw

# Reemplazar la línea AD_SERVER
$oldLine = "AD_SERVER=10.50.5.200"
$newLine = "AD_SERVER=elt-dc1-mia.elite.local"

if ($content -match $oldLine) {
    $newContent = $content -replace $oldLine, $newLine
    
    # Guardar el archivo actualizado
    Set-Content -Path $envPath -Value $newContent -Encoding UTF8
    
    Write-Host "AD_SERVER actualizado exitosamente" -ForegroundColor Green
    Write-Host "   Antes: $oldLine" -ForegroundColor White
    Write-Host "   Despues: $newLine" -ForegroundColor White
    Write-Host ""
    Write-Host "Cambios realizados:" -ForegroundColor Cyan
    Write-Host "   - IP: 10.50.5.200 → DNS: elt-dc1-mia.elite.local" -ForegroundColor White
    Write-Host "   - Mejor compatibilidad con certificados SSL" -ForegroundColor White
    Write-Host "   - Preparado para validacion SSL estricta" -ForegroundColor White
    Write-Host ""
    Write-Host "Proximos pasos:" -ForegroundColor Yellow
    Write-Host "   1. Reiniciar el backend" -ForegroundColor White
    Write-Host "   2. Ejecutar: python diagnose_ssl.py" -ForegroundColor White
    Write-Host "   3. Verificar que muestre: Conexion SSL estricta exitosa" -ForegroundColor White
} else {
    Write-Host "No se encontro la linea AD_SERVER=10.50.5.200" -ForegroundColor Yellow
    Write-Host "El archivo .env ya puede estar actualizado o tener una configuracion diferente" -ForegroundColor White
} 