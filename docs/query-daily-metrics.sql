-- =====================================================
-- Script para consultar métricas diarias con ordenamiento
-- OneSite - Auditoría de Seguridad
-- =====================================================

USE OneSiteDW;
GO

-- =====================================================
-- Consulta de métricas diarias con ordenamiento
-- =====================================================

-- Métricas diarias ordenadas por fecha (más reciente primero)
SELECT 
    metric_date,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    SUM(account_lockouts) as account_lockouts,
    AVG(avg_response_time_ms) as avg_response_time,
    CASE 
        WHEN SUM(total_logins) > 0 
        THEN CAST((SUM(successful_logins) * 100.0 / SUM(total_logins)) AS DECIMAL(5,2))
        ELSE 0 
    END as success_rate_percent
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE))
GROUP BY metric_date
ORDER BY metric_date DESC;

-- =====================================================
-- Resumen de métricas de los últimos 7 días
-- =====================================================

SELECT 
    'Últimos 7 días' as periodo,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    SUM(account_lockouts) as account_lockouts,
    AVG(avg_response_time_ms) as avg_response_time_ms,
    CASE 
        WHEN SUM(total_logins) > 0 
        THEN CAST((SUM(successful_logins) * 100.0 / SUM(total_logins)) AS DECIMAL(5,2))
        ELSE 0 
    END as success_rate_percent
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -7, CAST(GETDATE() AS DATE))

UNION ALL

-- Resumen de métricas de los últimos 30 días
SELECT 
    'Últimos 30 días' as periodo,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    SUM(account_lockouts) as account_lockouts,
    AVG(avg_response_time_ms) as avg_response_time_ms,
    CASE 
        WHEN SUM(total_logins) > 0 
        THEN CAST((SUM(successful_logins) * 100.0 / SUM(total_logins)) AS DECIMAL(5,2))
        ELSE 0 
    END as success_rate_percent
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -30, CAST(GETDATE() AS DATE));

-- =====================================================
-- Métricas por hora del día actual
-- =====================================================

SELECT 
    metric_hour,
    total_logins,
    successful_logins,
    failed_logins,
    account_lockouts,
    avg_response_time_ms,
    CASE 
        WHEN total_logins > 0 
        THEN CAST((successful_logins * 100.0 / total_logins) AS DECIMAL(5,2))
        ELSE 0 
    END as success_rate_percent
FROM security_metrics
WHERE metric_date = CAST(GETDATE() AS DATE)
ORDER BY metric_hour;

-- =====================================================
-- Top 10 días con más intentos de login
-- =====================================================

SELECT TOP 10
    metric_date,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    CASE 
        WHEN SUM(total_logins) > 0 
        THEN CAST((SUM(successful_logins) * 100.0 / SUM(total_logins)) AS DECIMAL(5,2))
        ELSE 0 
    END as success_rate_percent
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -90, CAST(GETDATE() AS DATE))
GROUP BY metric_date
ORDER BY SUM(total_logins) DESC;

-- =====================================================
-- Días con mayor tasa de fallos (posibles ataques)
-- =====================================================

SELECT TOP 10
    metric_date,
    SUM(total_logins) as total_logins,
    SUM(successful_logins) as successful_logins,
    SUM(failed_logins) as failed_logins,
    CASE 
        WHEN SUM(total_logins) > 0 
        THEN CAST((SUM(failed_logins) * 100.0 / SUM(total_logins)) AS DECIMAL(5,2))
        ELSE 0 
    END as failure_rate_percent
FROM security_metrics
WHERE metric_date >= DATEADD(DAY, -90, CAST(GETDATE() AS DATE))
    AND SUM(total_logins) > 10  -- Solo días con actividad significativa
GROUP BY metric_date
ORDER BY (SUM(failed_logins) * 100.0 / SUM(total_logins)) DESC;

PRINT '✅ Consultas de métricas ejecutadas exitosamente';
PRINT '📊 Métricas disponibles:';
PRINT '   - Métricas diarias ordenadas';
PRINT '   - Resumen de 7 y 30 días';
PRINT '   - Métricas por hora del día actual';
PRINT '   - Top 10 días con más actividad';
PRINT '   - Días con mayor tasa de fallos'; 