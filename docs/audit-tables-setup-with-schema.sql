-- =====================================================
-- Scripts SQL para configuración de auditoría OneSite
-- Base de datos: OneSiteDW
-- Servidor: SATURNO13
-- Usuario: Mtadm
-- Esquema: security (Recomendado para mejor organización)
-- =====================================================

USE OneSiteDW;
GO

-- =====================================================
-- 1. Crear esquema de seguridad
-- =====================================================

-- Crear esquema security si no existe
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'security')
BEGIN
    EXEC('CREATE SCHEMA security');
    PRINT '✅ Esquema security creado';
END
ELSE
BEGIN
    PRINT 'ℹ️ Esquema security ya existe';
END

-- =====================================================
-- 2. Tabla de auditoría de autenticación
-- =====================================================

-- Eliminar tabla si existe (para recrear con esquema correcto)
IF OBJECT_ID('dbo.audit_login_attempts', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.audit_login_attempts;
    PRINT '🗑️ Tabla dbo.audit_login_attempts eliminada';
END

CREATE TABLE security.audit_login_attempts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    attempt_time DATETIME2 DEFAULT GETDATE(),
    success BIT NOT NULL,
    failure_reason VARCHAR(255),
    ad_domain VARCHAR(100),
    session_id VARCHAR(255)
);

-- Índices para auditoría
CREATE INDEX idx_audit_login_username ON security.audit_login_attempts(username);
CREATE INDEX idx_audit_login_time ON security.audit_login_attempts(attempt_time);
CREATE INDEX idx_audit_login_ip ON security.audit_login_attempts(ip_address);

-- =====================================================
-- 3. Tabla de bloqueo de cuentas
-- =====================================================

-- Eliminar tabla si existe
IF OBJECT_ID('dbo.account_lockouts', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.account_lockouts;
    PRINT '🗑️ Tabla dbo.account_lockouts eliminada';
END

CREATE TABLE security.account_lockouts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    lockout_start DATETIME2 DEFAULT GETDATE(),
    lockout_end DATETIME2 NOT NULL,
    failed_attempts INT DEFAULT 1,
    is_active BIT DEFAULT 1
);

-- Índices para bloqueo
CREATE INDEX idx_lockout_username ON security.account_lockouts(username);
CREATE INDEX idx_lockout_ip ON security.account_lockouts(ip_address);
CREATE INDEX idx_lockout_active ON security.account_lockouts(is_active);

-- =====================================================
-- 4. Tabla de tokens blacklist
-- =====================================================

-- Eliminar tabla si existe
IF OBJECT_ID('dbo.token_blacklist', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.token_blacklist;
    PRINT '🗑️ Tabla dbo.token_blacklist eliminada';
END

CREATE TABLE security.token_blacklist (
    id INT IDENTITY(1,1) PRIMARY KEY,
    token_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL,
    blacklisted_at DATETIME2 DEFAULT GETDATE(),
    expires_at DATETIME2 NOT NULL,
    reason VARCHAR(100) DEFAULT 'logout'
);

-- Índices para blacklist
CREATE INDEX idx_blacklist_token ON security.token_blacklist(token_hash);
CREATE INDEX idx_blacklist_expires ON security.token_blacklist(expires_at);

-- =====================================================
-- 5. Tabla de métricas de seguridad
-- =====================================================

-- Eliminar tabla si existe
IF OBJECT_ID('dbo.security_metrics', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.security_metrics;
    PRINT '🗑️ Tabla dbo.security_metrics eliminada';
END

CREATE TABLE security.security_metrics (
    id INT IDENTITY(1,1) PRIMARY KEY,
    metric_date DATE DEFAULT CAST(GETDATE() AS DATE),
    metric_hour INT DEFAULT DATEPART(HOUR, GETDATE()),
    total_logins INT DEFAULT 0,
    successful_logins INT DEFAULT 0,
    failed_logins INT DEFAULT 0,
    account_lockouts INT DEFAULT 0,
    unique_users INT DEFAULT 0,
    avg_response_time_ms INT DEFAULT 0
);

-- Índice único para métricas por fecha/hora
CREATE UNIQUE INDEX idx_metrics_datetime ON security.security_metrics(metric_date, metric_hour);

-- =====================================================
-- 6. Tabla de configuración de seguridad
-- =====================================================

-- Eliminar tabla si existe
IF OBJECT_ID('dbo.security_config', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.security_config;
    PRINT '🗑️ Tabla dbo.security_config eliminada';
END

CREATE TABLE security.security_config (
    id INT IDENTITY(1,1) PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value VARCHAR(255) NOT NULL,
    description TEXT,
    updated_at DATETIME2 DEFAULT GETDATE(),
    updated_by VARCHAR(100)
);

-- Insertar configuración inicial
INSERT INTO security.security_config (config_key, config_value, description) VALUES
('rate_limit_per_minute', '5', 'Máximo de intentos de login por minuto'),
('max_login_attempts', '5', 'Máximo de intentos fallidos antes del bloqueo'),
('lockout_duration_minutes', '15', 'Duración del bloqueo en minutos'),
('session_timeout_minutes', '60', 'Tiempo de expiración de sesión'),
('password_policy_enabled', 'true', 'Habilitar políticas de contraseña'),
('mfa_required', 'false', 'Requerir autenticación de dos factores');

-- =====================================================
-- 7. Procedimientos almacenados para auditoría
-- =====================================================

-- Eliminar procedimientos si existen
IF OBJECT_ID('dbo.sp_log_login_attempt', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_log_login_attempt;
IF OBJECT_ID('dbo.sp_check_account_lockout', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_check_account_lockout;
IF OBJECT_ID('dbo.sp_lock_account', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_lock_account;
IF OBJECT_ID('dbo.sp_cleanup_old_records', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_cleanup_old_records;

-- Procedimiento para registrar intento de login
CREATE PROCEDURE security.sp_log_login_attempt
    @username VARCHAR(100),
    @ip_address VARCHAR(45),
    @user_agent TEXT,
    @success BIT,
    @failure_reason VARCHAR(255) = NULL,
    @ad_domain VARCHAR(100) = NULL,
    @session_id VARCHAR(255) = NULL
AS
BEGIN
    INSERT INTO security.audit_login_attempts (
        username, ip_address, user_agent, success, 
        failure_reason, ad_domain, session_id
    ) VALUES (
        @username, @ip_address, @user_agent, @success,
        @failure_reason, @ad_domain, @session_id
    );
END;
GO

-- Procedimiento para verificar bloqueo de cuenta
CREATE PROCEDURE security.sp_check_account_lockout
    @username VARCHAR(100),
    @ip_address VARCHAR(45)
AS
BEGIN
    SELECT 
        is_active,
        lockout_end,
        failed_attempts
    FROM security.account_lockouts 
    WHERE username = @username 
        AND ip_address = @ip_address 
        AND is_active = 1
        AND lockout_end > GETDATE();
END;
GO

-- Procedimiento para registrar bloqueo
CREATE PROCEDURE security.sp_lock_account
    @username VARCHAR(100),
    @ip_address VARCHAR(45),
    @lockout_minutes INT = 15
AS
BEGIN
    DECLARE @lockout_end DATETIME2 = DATEADD(MINUTE, @lockout_minutes, GETDATE());
    
    -- Actualizar bloqueo existente o crear nuevo
    IF EXISTS (SELECT 1 FROM security.account_lockouts WHERE username = @username AND ip_address = @ip_address AND is_active = 1)
    BEGIN
        UPDATE security.account_lockouts 
        SET failed_attempts = failed_attempts + 1,
            lockout_end = @lockout_end
        WHERE username = @username AND ip_address = @ip_address AND is_active = 1;
    END
    ELSE
    BEGIN
        INSERT INTO security.account_lockouts (username, ip_address, lockout_end)
        VALUES (@username, @ip_address, @lockout_end);
    END
END;
GO

-- Procedimiento para limpiar registros antiguos
CREATE PROCEDURE security.sp_cleanup_old_records
    @days_to_keep INT = 90
AS
BEGIN
    DECLARE @cutoff_date DATETIME2 = DATEADD(DAY, -@days_to_keep, GETDATE());
    
    -- Limpiar intentos de login antiguos
    DELETE FROM security.audit_login_attempts WHERE attempt_time < @cutoff_date;
    
    -- Limpiar bloqueos expirados
    DELETE FROM security.account_lockouts WHERE lockout_end < GETDATE() AND is_active = 1;
    
    -- Limpiar tokens expirados
    DELETE FROM security.token_blacklist WHERE expires_at < GETDATE();
    
    PRINT 'Limpieza completada: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' registros eliminados';
END;
GO

-- =====================================================
-- 8. Vistas para reportes de seguridad
-- =====================================================

-- Eliminar vistas si existen
IF OBJECT_ID('dbo.vw_recent_login_attempts', 'V') IS NOT NULL
    DROP VIEW dbo.vw_recent_login_attempts;
IF OBJECT_ID('dbo.vw_active_lockouts', 'V') IS NOT NULL
    DROP VIEW dbo.vw_active_lockouts;
IF OBJECT_ID('dbo.vw_daily_security_metrics', 'V') IS NOT NULL
    DROP VIEW dbo.vw_daily_security_metrics;

-- Vista de intentos de login recientes
CREATE VIEW security.vw_recent_login_attempts AS
SELECT TOP 100
    username,
    ip_address,
    attempt_time,
    success,
    failure_reason,
    ad_domain
FROM security.audit_login_attempts
ORDER BY attempt_time DESC;

-- Vista de cuentas bloqueadas
CREATE VIEW security.vw_active_lockouts AS
SELECT 
    username,
    ip_address,
    lockout_start,
    lockout_end,
    failed_attempts,
    DATEDIFF(MINUTE, GETDATE(), lockout_end) as remaining_minutes
FROM security.account_lockouts
WHERE is_active = 1 AND lockout_end > GETDATE();

-- Vista de métricas diarias (sin ORDER BY)
CREATE VIEW security.vw_daily_security_metrics AS
SELECT 
    metric_date,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    SUM(account_lockouts) as account_lockouts,
    AVG(avg_response_time_ms) as avg_response_time
FROM security.security_metrics
WHERE metric_date >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
GROUP BY metric_date;

-- =====================================================
-- 9. Triggers para auditoría automática
-- =====================================================

-- Eliminar trigger si existe
IF OBJECT_ID('dbo.tr_audit_login_metrics', 'TR') IS NOT NULL
    DROP TRIGGER dbo.tr_audit_login_metrics;

-- Trigger para actualizar métricas automáticamente
CREATE TRIGGER security.tr_audit_login_metrics
ON security.audit_login_attempts
AFTER INSERT
AS
BEGIN
    DECLARE @current_date DATE = CAST(GETDATE() AS DATE);
    DECLARE @current_hour INT = DATEPART(HOUR, GETDATE());
    
    -- Actualizar métricas
    IF EXISTS (SELECT 1 FROM security.security_metrics WHERE metric_date = @current_date AND metric_hour = @current_hour)
    BEGIN
        UPDATE security.security_metrics 
        SET 
            total_logins = total_logins + (SELECT COUNT(*) FROM inserted),
            successful_logins = successful_logins + (SELECT COUNT(*) FROM inserted WHERE success = 1),
            failed_logins = failed_logins + (SELECT COUNT(*) FROM inserted WHERE success = 0)
        WHERE metric_date = @current_date AND metric_hour = @current_hour;
    END
    ELSE
    BEGIN
        INSERT INTO security.security_metrics (metric_date, metric_hour, total_logins, successful_logins, failed_logins)
        SELECT 
            @current_date,
            @current_hour,
            COUNT(*),
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END),
            SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END)
        FROM inserted;
    END
END;
GO

-- =====================================================
-- 10. Permisos y roles de seguridad
-- =====================================================

-- Crear rol para auditoría
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'onesite_auditor')
BEGIN
    CREATE ROLE onesite_auditor;
END

-- Asignar permisos de solo lectura para auditoría
GRANT SELECT ON security.audit_login_attempts TO onesite_auditor;
GRANT SELECT ON security.account_lockouts TO onesite_auditor;
GRANT SELECT ON security.security_metrics TO onesite_auditor;
GRANT SELECT ON security.vw_recent_login_attempts TO onesite_auditor;
GRANT SELECT ON security.vw_active_lockouts TO onesite_auditor;
GRANT SELECT ON security.vw_daily_security_metrics TO onesite_auditor;

-- Crear rol para administración de seguridad
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'onesite_security_admin')
BEGIN
    CREATE ROLE onesite_security_admin;
END

-- Asignar permisos de administración
GRANT ALL ON security.audit_login_attempts TO onesite_security_admin;
GRANT ALL ON security.account_lockouts TO onesite_security_admin;
GRANT ALL ON security.token_blacklist TO onesite_security_admin;
GRANT ALL ON security.security_metrics TO onesite_security_admin;
GRANT ALL ON security.security_config TO onesite_security_admin;
GRANT EXECUTE ON security.sp_log_login_attempt TO onesite_security_admin;
GRANT EXECUTE ON security.sp_check_account_lockout TO onesite_security_admin;
GRANT EXECUTE ON security.sp_lock_account TO onesite_security_admin;
GRANT EXECUTE ON security.sp_cleanup_old_records TO onesite_security_admin;

-- Asignar permisos al usuario Mtadm
GRANT onesite_security_admin TO Mtadm;

-- =====================================================
-- 11. Verificación final
-- =====================================================

PRINT '✅ Scripts de auditoría ejecutados exitosamente';
PRINT '📊 Configuración para OneSiteDW en SATURNO13:';
PRINT '   - Base de datos: OneSiteDW';
PRINT '   - Esquema: security';
PRINT '   - Usuario: Mtadm';
PRINT '';
PRINT '📋 Tablas creadas en esquema security:';
PRINT '   - audit_login_attempts (auditoría de login)';
PRINT '   - account_lockouts (bloqueo de cuentas)';
PRINT '   - token_blacklist (tokens invalidados)';
PRINT '   - security_metrics (métricas de seguridad)';
PRINT '   - security_config (configuración)';
PRINT '';
PRINT '🔧 Procedimientos almacenados creados:';
PRINT '   - sp_log_login_attempt';
PRINT '   - sp_check_account_lockout';
PRINT '   - sp_lock_account';
PRINT '   - sp_cleanup_old_records';
PRINT '';
PRINT '👁️ Vistas de reportes configuradas:';
PRINT '   - vw_recent_login_attempts';
PRINT '   - vw_active_lockouts';
PRINT '   - vw_daily_security_metrics';
PRINT '';
PRINT '🔐 Roles de seguridad establecidos:';
PRINT '   - onesite_auditor (solo lectura)';
PRINT '   - onesite_security_admin (administración)';
PRINT '';
PRINT '👤 Usuario Mtadm configurado con permisos de administración';
PRINT '';
PRINT '🎯 Beneficios del esquema security:';
PRINT '   - Mejor organización de datos';
PRINT '   - Permisos granulares';
PRINT '   - Fácil mantenimiento';
PRINT '   - Aislamiento de datos sensibles'; 