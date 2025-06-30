@echo off
echo ====================================================
echo    Ejecutando Scripts de Auditoria OneSite
echo    Base de datos: OneSiteDW
echo    Servidor: SATURNO13
echo ====================================================
echo.

REM Configurar variables de entorno
set DB_SERVER=SATURNO13
set DB_NAME=OneSiteDW
set DB_USER=Mtadm
set DB_PASSWORD=CIOelite0630!!

echo 🔧 Conectando a la base de datos...
echo    Servidor: %DB_SERVER%
echo    Base de datos: %DB_NAME%
echo    Usuario: %DB_USER%
echo.

REM Ejecutar script SQL usando sqlcmd
sqlcmd -S %DB_SERVER% -d %DB_NAME% -U %DB_USER% -P %DB_PASSWORD% -i audit-tables-setup.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Scripts ejecutados exitosamente
    echo 📊 Tablas de auditoria creadas en OneSiteDW
    echo 🔐 Roles de seguridad configurados
    echo 👤 Usuario Mtadm con permisos asignados
) else (
    echo.
    echo ❌ Error al ejecutar los scripts
    echo 🔍 Verificar conexion a la base de datos
)

echo.
echo ====================================================
echo    Proceso completado
echo ====================================================
pause 