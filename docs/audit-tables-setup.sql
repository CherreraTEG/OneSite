-- =====================================================
-- Scripts SQL para configuración de auditoría OneSite
-- Base de datos: OneSiteDW
-- Servidor: SATURNO13
-- Usuario: data_analysis_admin
-- =====================================================

USE OneSiteDW;
GO

-- =====================================================
-- 1. Tabla de auditoría de autenticación
-- =====================================================
CREATE TABLE audit_login_attempts (
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
CREATE INDEX idx_audit_login_username ON audit_login_attempts(username);
CREATE INDEX idx_audit_login_time ON audit_login_attempts(attempt_time);
CREATE INDEX idx_audit_login_ip ON audit_login_attempts(ip_address);

-- =====================================================
-- 2. Tabla de bloqueo de cuentas
-- =====================================================
CREATE TABLE account_lockouts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    lockout_start DATETIME2 DEFAULT GETDATE(),
    lockout_end DATETIME2 NOT NULL,
    failed_attempts INT DEFAULT 1,
    is_active BIT DEFAULT 1
);

-- Índices para bloqueo
CREATE INDEX idx_lockout_username ON account_lockouts(username);
CREATE INDEX idx_lockout_ip ON account_lockouts(ip_address);
CREATE INDEX idx_lockout_active ON account_lockouts(is_active);

-- =====================================================
-- 3. Tabla de tokens blacklist
-- =====================================================
CREATE TABLE token_blacklist (
    id INT IDENTITY(1,1) PRIMARY KEY,
    token_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL,
    blacklisted_at DATETIME2 DEFAULT GETDATE(),
    expires_at DATETIME2 NOT NULL,
    reason VARCHAR(100) DEFAULT 'logout'
);

-- Índices para blacklist
CREATE INDEX idx_blacklist_token ON token_blacklist(token_hash);
CREATE INDEX idx_blacklist_expires ON token_blacklist(expires_at);

-- =====================================================
-- 4. Tabla de métricas de seguridad
-- =====================================================
CREATE TABLE security_metrics (
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
CREATE UNIQUE INDEX idx_metrics_datetime ON security_metrics(metric_date, metric_hour);

-- =====================================================
-- 5. Tabla de configuración de seguridad
-- =====================================================
CREATE TABLE security_config (
    id INT IDENTITY(1,1) PRIMARY KEY,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value VARCHAR(255) NOT NULL,
    description TEXT,
    updated_at DATETIME2 DEFAULT GETDATE(),
    updated_by VARCHAR(100)
);

-- Insertar configuración inicial
INSERT INTO security_config (config_key, config_value, description) VALUES
('rate_limit_per_minute', '5', 'Máximo de intentos de login por minuto'),
('max_login_attempts', '5', 'Máximo de intentos fallidos antes del bloqueo'),
('lockout_duration_minutes', '15', 'Duración del bloqueo en minutos'),
('session_timeout_minutes', '60', 'Tiempo de expiración de sesión'),
('password_policy_enabled', 'true', 'Habilitar políticas de contraseña'),
('mfa_required', 'false', 'Requerir autenticación de dos factores');

-- =====================================================
-- 6. Procedimientos almacenados para auditoría
-- =====================================================

-- Procedimiento para registrar intento de login
CREATE PROCEDURE sp_log_login_attempt
    @username VARCHAR(100),
    @ip_address VARCHAR(45),
    @user_agent TEXT,
    @success BIT,
    @failure_reason VARCHAR(255) = NULL,
    @ad_domain VARCHAR(100) = NULL,
    @session_id VARCHAR(255) = NULL
AS
BEGIN
    INSERT INTO audit_login_attempts (
        username, ip_address, user_agent, success, 
        failure_reason, ad_domain, session_id
    ) VALUES (
        @username, @ip_address, @user_agent, @success,
        @failure_reason, @ad_domain, @session_id
    );
END;
GO

-- Procedimiento para verificar bloqueo de cuenta
CREATE PROCEDURE sp_check_account_lockout
    @username VARCHAR(100),
    @ip_address VARCHAR(45)
AS
BEGIN
    SELECT 
        is_active,
        lockout_end,
        failed_attempts
    FROM account_lockouts 
    WHERE username = @username 
        AND ip_address = @ip_address 
        AND is_active = 1
        AND lockout_end > GETDATE();
END;
GO

-- Procedimiento para registrar bloqueo
CREATE PROCEDURE sp_lock_account
    @username VARCHAR(100),
    @ip_address VARCHAR(45),
    @lockout_minutes INT = 15
AS
BEGIN
    DECLARE @lockout_end DATETIME2 = DATEADD(MINUTE, @lockout_minutes, GETDATE());
    
    -- Actualizar bloqueo existente o crear nuevo
    IF EXISTS (SELECT 1 FROM account_lockouts WHERE username = @username AND ip_address = @ip_address AND is_active = 1)
    BEGIN
        UPDATE account_lockouts 
        SET failed_attempts = failed_attempts + 1,
            lockout_end = @lockout_end
        WHERE username = @username AND ip_address = @ip_address AND is_active = 1;
    END
    ELSE
    BEGIN
        INSERT INTO account_lockouts (username, ip_address, lockout_end)
        VALUES (@username, @ip_address, @lockout_end);
    END
END;
GO

-- Procedimiento para limpiar registros antiguos
CREATE PROCEDURE sp_cleanup_old_records
    @days_to_keep INT = 90
AS
BEGIN
    DECLARE @cutoff_date DATETIME2 = DATEADD(DAY, -@days_to_keep, GETDATE());
    
    -- Limpiar intentos de login antiguos
    DELETE FROM audit_login_attempts WHERE attempt_time < @cutoff_date;
    
    -- Limpiar bloqueos expirados
    DELETE FROM account_lockouts WHERE lockout_end < GETDATE() AND is_active = 1;
    
    -- Limpiar tokens expirados
    DELETE FROM token_blacklist WHERE expires_at < GETDATE();
    
    PRINT 'Limpieza completada: ' + CAST(@@ROWCOUNT AS VARCHAR) + ' registros eliminados';
END;
GO

-- =====================================================
-- 7. Vistas para reportes de seguridad
-- =====================================================

-- Vista de intentos de login recientes
CREATE VIEW vw_recent_login_attempts AS
SELECT TOP 100
    username,
    ip_address,
    attempt_time,
    success,
    failure_reason,
    ad_domain
FROM audit_login_attempts
ORDER BY attempt_time DESC;

-- Vista de cuentas bloqueadas
CREATE VIEW vw_active_lockouts AS
SELECT 
    username,
    ip_address,
    lockout_start,
    lockout_end,
    failed_attempts,
    DATEDIFF(MINUTE, GETDATE(), lockout_end) as remaining_minutes
FROM account_lockouts
WHERE is_active = 1 AND lockout_end > GETDATE();

-- Vista de métricas diarias
CREATE VIEW vw_daily_security_metrics AS
SELECT 
    metric_date,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    SUM(account_lockouts) as account_lockouts,
    AVG(avg_response_time_ms) as avg_response_time
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
GROUP BY metric_date
ORDER BY metric_date DESC;

-- =====================================================
-- 8. Triggers para auditoría automática
-- =====================================================

-- Trigger para actualizar métricas automáticamente
CREATE TRIGGER tr_audit_login_metrics
ON audit_login_attempts
AFTER INSERT
AS
BEGIN
    DECLARE @current_date DATE = CAST(GETDATE() AS DATE);
    DECLARE @current_hour INT = DATEPART(HOUR, GETDATE());
    
    -- Actualizar métricas
    IF EXISTS (SELECT 1 FROM security_metrics WHERE metric_date = @current_date AND metric_hour = @current_hour)
    BEGIN
        UPDATE security_metrics 
        SET 
            total_logins = total_logins + (SELECT COUNT(*) FROM inserted),
            successful_logins = successful_logins + (SELECT COUNT(*) FROM inserted WHERE success = 1),
            failed_logins = failed_logins + (SELECT COUNT(*) FROM inserted WHERE success = 0)
        WHERE metric_date = @current_date AND metric_hour = @current_hour;
    END
    ELSE
    BEGIN
        INSERT INTO security_metrics (metric_date, metric_hour, total_logins, successful_logins, failed_logins)
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
-- 9. Permisos y roles de seguridad
-- =====================================================

-- Crear rol para auditoría
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'onesite_auditor')
BEGIN
    CREATE ROLE onesite_auditor;
END

-- Asignar permisos de solo lectura para auditoría
GRANT SELECT ON audit_login_attempts TO onesite_auditor;
GRANT SELECT ON account_lockouts TO onesite_auditor;
GRANT SELECT ON security_metrics TO onesite_auditor;
GRANT SELECT ON vw_recent_login_attempts TO onesite_auditor;
GRANT SELECT ON vw_active_lockouts TO onesite_auditor;
GRANT SELECT ON vw_daily_security_metrics TO onesite_auditor;

-- Crear rol para administración de seguridad
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'onesite_security_admin')
BEGIN
    CREATE ROLE onesite_security_admin;
END

-- Asignar permisos de administración
GRANT ALL ON audit_login_attempts TO onesite_security_admin;
GRANT ALL ON account_lockouts TO onesite_security_admin;
GRANT ALL ON token_blacklist TO onesite_security_admin;
GRANT ALL ON security_metrics TO onesite_security_admin;
GRANT ALL ON security_config TO onesite_security_admin;
GRANT EXECUTE ON sp_log_login_attempt TO onesite_security_admin;
GRANT EXECUTE ON sp_check_account_lockout TO onesite_security_admin;
GRANT EXECUTE ON sp_lock_account TO onesite_security_admin;
GRANT EXECUTE ON sp_cleanup_old_records TO onesite_security_admin;

-- Asignar permisos al usuario data_analysis_admin
GRANT onesite_security_admin TO data_analysis_admin;

PRINT '✅ Scripts de auditoría ejecutados exitosamente';
PRINT '📊 Configuración para OneSiteDW en SATURNO13:';
PRINT '   - Base de datos: OneSiteDW';
PRINT '   - Usuario: data_analysis_admin';
PRINT '   - Tablas creadas:';
PRINT '     * audit_login_attempts (auditoría de login)';
PRINT '     * account_lockouts (bloqueo de cuentas)';
PRINT '     * token_blacklist (tokens invalidados)';
PRINT '     * security_metrics (métricas de seguridad)';
PRINT '     * security_config (configuración)';
PRINT '🔧 Procedimientos almacenados creados';
PRINT '👁️ Vistas de reportes configuradas';
PRINT '🔐 Roles de seguridad establecidos';
PRINT '👤 Usuario data_analysis_admin configurado con permisos de administración'; 