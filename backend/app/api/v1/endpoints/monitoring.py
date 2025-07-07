"""
Endpoints para monitoreo de seguridad de OneSite
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.deps import get_current_user
from app.services.security_monitor import security_monitor
from app.db.base import get_db

router = APIRouter()

@router.get("/metrics")
async def get_security_metrics(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener métricas de seguridad en tiempo real
    """
    try:
        metrics = await security_monitor.collect_security_metrics()
        return {
            "status": "success",
            "data": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo métricas: {str(e)}"
        )

@router.get("/alerts")
async def get_security_alerts(
    current_user = Depends(get_current_user)
):
    """
    Obtener alertas de seguridad activas
    """
    try:
        alerts = await security_monitor.get_security_alerts()
        return {
            "status": "success",
            "data": alerts,
            "count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo alertas: {str(e)}"
        )

@router.get("/recent-logins")
async def get_recent_login_attempts(
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener intentos de login recientes
    """
    try:
        # Usar la vista creada en SQL con esquema security
        result = db.execute(text("""
            SELECT TOP :limit 
                username,
                ip_address,
                attempt_time,
                success,
                failure_reason,
                ad_domain
            FROM security.vw_recent_login_attempts
            ORDER BY attempt_time DESC
        """), {"limit": limit})
        
        logins = []
        for row in result:
            logins.append({
                "username": row.username,
                "ip_address": row.ip_address,
                "attempt_time": row.attempt_time.isoformat() if row.attempt_time else None,
                "success": row.success,
                "failure_reason": row.failure_reason,
                "ad_domain": row.ad_domain
            })
        
        return {
            "status": "success",
            "data": logins,
            "count": len(logins),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo intentos de login: {str(e)}"
        )

@router.get("/active-lockouts")
async def get_active_lockouts(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener cuentas bloqueadas activas
    """
    try:
        # Usar la vista creada en SQL con esquema security
        result = db.execute(text("""
            SELECT 
                username,
                ip_address,
                lockout_start,
                lockout_end,
                failed_attempts,
                remaining_minutes
            FROM security.vw_active_lockouts
            ORDER BY lockout_start DESC
        """))
        
        lockouts = []
        for row in result:
            lockouts.append({
                "username": row.username,
                "ip_address": row.ip_address,
                "lockout_start": row.lockout_start.isoformat() if row.lockout_start else None,
                "lockout_end": row.lockout_end.isoformat() if row.lockout_end else None,
                "failed_attempts": row.failed_attempts,
                "remaining_minutes": row.remaining_minutes
            })
        
        return {
            "status": "success",
            "data": lockouts,
            "count": len(lockouts),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo bloqueos: {str(e)}"
        )

@router.get("/daily-metrics")
async def get_daily_metrics(
    days: int = 7,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener métricas diarias de seguridad (CONSULTA CORREGIDA con esquema security)
    """
    try:
        # Consulta corregida con ORDER BY y esquema security
        result = db.execute(text("""
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
                END as success_rate
            FROM security.security_metrics
            WHERE metric_date >= DATEADD(DAY, -:days, CAST(GETDATE() AS DATE))
            GROUP BY metric_date
            ORDER BY metric_date DESC
        """), {"days": days})
        
        metrics = []
        for row in result:
            metrics.append({
                "date": row.metric_date.isoformat() if row.metric_date else None,
                "total_logins": row.total_logins,
                "successful_logins": row.successful_logins,
                "failed_logins": row.failed_logins,
                "account_lockouts": row.account_lockouts,
                "avg_response_time": row.avg_response_time,
                "success_rate": float(row.success_rate) if row.success_rate else 0
            })
        
        return {
            "status": "success",
            "data": metrics,
            "period_days": days,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo métricas diarias: {str(e)}"
        )

@router.post("/cleanup")
async def cleanup_old_data(
    days_to_keep: int = 90,
    current_user = Depends(get_current_user)
):
    """
    Limpiar datos antiguos de auditoría
    """
    try:
        await security_monitor.cleanup_old_data(days_to_keep)
        return {
            "status": "success",
            "message": f"Datos antiguos limpiados (manteniendo {days_to_keep} días)",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error limpiando datos: {str(e)}"
        )

@router.get("/health")
async def get_system_health(
    current_user = Depends(get_current_user)
):
    """
    Obtener estado de salud del sistema de seguridad
    """
    try:
        metrics = await security_monitor.collect_security_metrics()
        health_status = metrics["system_health"]
        
        return {
            "status": "success",
            "data": {
                "overall_health": health_status["overall_health"],
                "redis_healthy": health_status["redis_healthy"],
                "database_healthy": health_status["database_healthy"],
                "last_check": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verificando salud del sistema: {str(e)}"
        )

@router.get("/summary")
async def get_security_summary(
    current_user = Depends(get_current_user)
):
    """
    Obtener resumen de seguridad
    """
    try:
        metrics = await security_monitor.collect_security_metrics()
        alerts = await security_monitor.get_security_alerts()
        
        # Calcular resumen
        summary = {
            "login_attempts": {
                "total_last_hour": metrics["login_attempts"]["total_attempts"],
                "successful_last_hour": metrics["login_attempts"]["successful_attempts"],
                "failed_last_hour": metrics["login_attempts"]["failed_attempts"],
                "success_rate": metrics["login_attempts"]["success_rate"]
            },
            "security_status": {
                "active_lockouts": metrics["account_lockouts"]["active_lockouts"],
                "blocked_ips": metrics["rate_limiting"]["blocked_ips"],
                "blocked_users": metrics["rate_limiting"]["blocked_users"],
                "active_alerts": len(alerts)
            },
            "system_status": {
                "redis_connected": metrics["redis_connected"],
                "overall_health": metrics["system_health"]["overall_health"]
            }
        }
        
        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo resumen: {str(e)}"
        ) 