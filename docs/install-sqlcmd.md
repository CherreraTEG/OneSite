# 🔧 Instalación de SQL Server Command Line Utilities

## 📋 **Requisitos**
- Windows 10/11 o Windows Server
- Acceso a internet para descarga

## 🚀 **Instalación de sqlcmd**

### **Método 1: Usando Microsoft SQL Server Command Line Utilities**

1. **Descargar desde Microsoft:**
   - Visitar: https://docs.microsoft.com/en-us/sql/tools/sqlcmd-utility
   - Descargar "Microsoft ODBC Driver for SQL Server"
   - Descargar "Microsoft Command Line Utilities for SQL Server"

2. **Instalar componentes:**
   ```powershell
   # Descargar e instalar ODBC Driver
   # Descargar e instalar Command Line Utilities
   ```

### **Método 2: Usando Chocolatey (Recomendado)**

```powershell
# Instalar Chocolatey si no está instalado
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar SQL Server Command Line Utilities
choco install sqlcmd
```

### **Método 3: Instalación Manual**

1. **Descargar desde Microsoft:**
   - https://go.microsoft.com/fwlink/?linkid=2142258
   - Seleccionar versión x64 para Windows

2. **Ejecutar instalador:**
   ```powershell
   # Ejecutar el archivo .msi descargado
   msiexec /i MicrosoftCommandLineUtilities.msi /quiet
   ```

## ✅ **Verificar Instalación**

```powershell
# Verificar que sqlcmd está disponible
sqlcmd -?

# Probar conexión
sqlcmd -S SATURNO13 -U Mtadm -P "CIOelite0630!!" -Q "SELECT @@VERSION"
```

## 🔧 **Configurar PATH (si es necesario)**

Si sqlcmd no se encuentra automáticamente:

```powershell
# Agregar al PATH
$env:PATH += ";C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn"

# O instalar en ubicación específica
```

## 🚀 **Ejecutar Scripts Después de la Instalación**

```powershell
# Navegar a la carpeta docs
cd C:\Cursor\OneSite\docs

# Ejecutar script de auditoría
.\execute-audit-scripts.bat
```

---

**Nota:** Una vez instalado sqlcmd, podrás ejecutar el script de auditoría sin problemas. 