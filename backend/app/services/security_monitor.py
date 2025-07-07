"""
Servicio de monitoreo de métricas de seguridad para OneSite
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import redis
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.db.base import get_db

logger = logging.getLogger(__name__)

class SecurityMonitor:
    """Monitor de seguridad para OneSite"""
    
    def __init__(self):
        self.redis_client = None
        self._init_redis()
    
    def _init_redis(self):
        """Inicializar conexión Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info("Conexion Redis establecida para monitoreo")
        except Exception as e:
            logger.error(f"Error conectando a Redis: {e}")
            self.redis_client = None
    
    async def collect_security_metrics(self) -> Dict:
        """Recopilar métricas de seguridad"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "redis_connected": self.redis_client is not None,
            "login_attempts": await self._get_login_attempts_metrics(),
            "rate_limiting": await self._get_rate_limiting_metrics(),
            "account_lockouts": await self._get_lockout_metrics(),
            "token_blacklist": await self._get_blacklist_metrics(),
            "system_health": await self._get_system_health()
        }
        
        # Guardar métricas en base de datos
        await self._save_metrics_to_db(metrics)
        
        return metrics
    
    async def _get_login_attempts_metrics(self) -> Dict:
        """Obtener métricas de intentos de login"""
        try:
            db = next(get_db())
            
            # Métricas de la última hora
            one_hour_ago = datetime.now() - timedelta(hours=1)
            
            # Total de intentos
            total_attempts = db.execute(text("""
                SELECT COUNT(*) FROM security.audit_login_attempts 
                WHERE attempt_time >= :one_hour_ago
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            # Intentos exitosos
            successful_attempts = db.execute(text("""
                SELECT COUNT(*) FROM security.audit_login_attempts 
                WHERE attempt_time >= :one_hour_ago AND success = 1
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            # Intentos fallidos
            failed_attempts = db.execute(text("""
                SELECT COUNT(*) FROM security.audit_login_attempts 
                WHERE attempt_time >= :one_hour_ago AND success = 0
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            # Usuarios únicos
            unique_users = db.execute(text("""
                SELECT COUNT(DISTINCT username) FROM security.audit_login_attempts 
                WHERE attempt_time >= :one_hour_ago
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            # IPs únicas
            unique_ips = db.execute(text("""
                SELECT COUNT(DISTINCT ip_address) FROM security.audit_login_attempts 
                WHERE attempt_time >= :one_hour_ago
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            return {
                "total_attempts": total_attempts or 0,
                "successful_attempts": successful_attempts or 0,
                "failed_attempts": failed_attempts or 0,
                "success_rate": (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
                "unique_users": unique_users or 0,
                "unique_ips": unique_ips or 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de login: {e}")
            return {
                "total_attempts": 0,
                "successful_attempts": 0,
                "failed_attempts": 0,
                "success_rate": 0,
                "unique_users": 0,
                "unique_ips": 0
            }
    
    async def _get_rate_limiting_metrics(self) -> Dict:
        """Obtener métricas de rate limiting"""
        if not self.redis_client:
            return {"active_limits": 0, "blocked_ips": 0, "blocked_users": 0}
        
        try:
            # Contar claves de rate limiting activas
            rate_limit_keys = self.redis_client.keys("rate_limit:*")
            active_limits = len(rate_limit_keys)
            
            # Contar IPs bloqueadas
            blocked_ip_keys = self.redis_client.keys("rate_limit:ip:*")
            blocked_ips = len(blocked_ip_keys)
            
            # Contar usuarios bloqueados
            blocked_user_keys = self.redis_client.keys("rate_limit:user:*")
            blocked_users = len(blocked_user_keys)
            
            return {
                "active_limits": active_limits,
                "blocked_ips": blocked_ips,
                "blocked_users": blocked_users
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de rate limiting: {e}")
            return {"active_limits": 0, "blocked_ips": 0, "blocked_users": 0}
    
    async def _get_lockout_metrics(self) -> Dict:
        """Obtener métricas de bloqueo de cuentas"""
        try:
            db = next(get_db())
            
            # Cuentas bloqueadas activas
            active_lockouts = db.execute(text("""
                SELECT COUNT(*) FROM security.account_lockouts 
                WHERE is_active = 1 AND lockout_end > GETDATE()
            """)).scalar()
            
            # Bloqueos en la última hora
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_lockouts = db.execute(text("""
                SELECT COUNT(*) FROM security.account_lockouts 
                WHERE lockout_start >= :one_hour_ago
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            return {
                "active_lockouts": active_lockouts or 0,
                "recent_lockouts": recent_lockouts or 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de bloqueo: {e}")
            return {"active_lockouts": 0, "recent_lockouts": 0}
    
    async def _get_blacklist_metrics(self) -> Dict:
        """Obtener métricas de blacklist de tokens"""
        try:
            db = next(get_db())
            
            # Tokens en blacklist activos
            active_blacklist = db.execute(text("""
                SELECT COUNT(*) FROM security.token_blacklist 
                WHERE expires_at > GETDATE()
            """)).scalar()
            
            # Tokens agregados en la última hora
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_blacklist = db.execute(text("""
                SELECT COUNT(*) FROM security.token_blacklist 
                WHERE blacklisted_at >= :one_hour_ago
            """), {"one_hour_ago": one_hour_ago}).scalar()
            
            return {
                "active_blacklist": active_blacklist or 0,
                "recent_blacklist": recent_blacklist or 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de blacklist: {e}")
            return {"active_blacklist": 0, "recent_blacklist": 0}
    
    async def _get_system_health(self) -> Dict:
        """Obtener métricas de salud del sistema"""
        try:
            # Verificar Redis
            redis_health = False
            if self.redis_client:
                try:
                    self.redis_client.ping()
                    redis_health = True
                except:
                    redis_health = False
            
            # Verificar base de datos
            db_health = False
            try:
                db = next(get_db())
                db.execute(text("SELECT 1"))
                db_health = True
            except:
                db_health = False
            
            return {
                "redis_healthy": redis_health,
                "database_healthy": db_health,
                "overall_health": redis_health and db_health
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo salud del sistema: {e}")
            return {
                "redis_healthy": False,
                "database_healthy": False,
                "overall_health": False
            }
    
    async def _save_metrics_to_db(self, metrics: Dict):
        """Guardar métricas en base de datos"""
        try:
            db = next(get_db())
            
            # Insertar métricas en la tabla security_metrics
            current_date = datetime.now().date()
            current_hour = datetime.now().hour
            
            # Verificar si ya existe registro para esta hora
            existing = db.execute(text("""
                SELECT id FROM security.security_metrics 
                WHERE metric_date = :current_date AND metric_hour = :current_hour
            """), {
                "current_date": current_date,
                "current_hour": current_hour
            }).fetchone()
            
            if existing:
                # Actualizar registro existente
                db.execute(text("""
                    UPDATE security.security_metrics 
                    SET 
                        total_logins = :total_logins,
                        successful_logins = :successful_logins,
                        failed_logins = :failed_logins,
                        account_lockouts = :account_lockouts,
                        unique_users = :unique_users,
                        avg_response_time_ms = :avg_response_time
                    WHERE metric_date = :current_date AND metric_hour = :current_hour
                """), {
                    "total_logins": metrics["login_attempts"]["total_attempts"],
                    "successful_logins": metrics["login_attempts"]["successful_attempts"],
                    "failed_logins": metrics["login_attempts"]["failed_attempts"],
                    "account_lockouts": metrics["account_lockouts"]["active_lockouts"],
                    "unique_users": metrics["login_attempts"]["unique_users"],
                    "avg_response_time": 0,  # TODO: Implementar medición de tiempo de respuesta
                    "current_date": current_date,
                    "current_hour": current_hour
                })
            else:
                # Crear nuevo registro
                db.execute(text("""
                    INSERT INTO security.security_metrics (
                        metric_date, metric_hour, total_logins, successful_logins,
                        failed_logins, account_lockouts, unique_users, avg_response_time_ms
                    ) VALUES (
                        :current_date, :current_hour, :total_logins, :successful_logins,
                        :failed_logins, :account_lockouts, :unique_users, :avg_response_time
                    )
                """), {
                    "current_date": current_date,
                    "current_hour": current_hour,
                    "total_logins": metrics["login_attempts"]["total_attempts"],
                    "successful_logins": metrics["login_attempts"]["successful_attempts"],
                    "failed_logins": metrics["login_attempts"]["failed_attempts"],
                    "account_lockouts": metrics["account_lockouts"]["active_lockouts"],
                    "unique_users": metrics["login_attempts"]["unique_users"],
                    "avg_response_time": 0
                })
            
            db.commit()
            logger.debug("Métricas guardadas en base de datos")
            
        except Exception as e:
            logger.error(f"Error guardando métricas en DB: {e}")
    
    async def get_security_alerts(self) -> List[Dict]:
        """Obtener alertas de seguridad"""
        alerts = []
        
        try:
            metrics = await self.collect_security_metrics()
            
            # Alerta: Tasa de éxito muy baja
            if metrics["login_attempts"]["success_rate"] < 50 and metrics["login_attempts"]["total_attempts"] > 10:
                alerts.append({
                    "type": "low_success_rate",
                    "severity": "warning",
                    "message": f"Tasa de éxito de login muy baja: {metrics['login_attempts']['success_rate']:.1f}%",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Alerta: Muchos bloqueos de cuenta
            if metrics["account_lockouts"]["active_lockouts"] > 5:
                alerts.append({
                    "type": "high_account_lockouts",
                    "severity": "warning",
                    "message": f"Muchas cuentas bloqueadas: {metrics['account_lockouts']['active_lockouts']}",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Alerta: Muchos intentos fallidos
            if metrics["login_attempts"]["failed_attempts"] > 20:
                alerts.append({
                    "type": "high_failed_attempts",
                    "severity": "warning",
                    "message": f"Muchos intentos fallidos: {metrics['login_attempts']['failed_attempts']}",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Alerta: Sistema no saludable
            if not metrics["system_health"]["overall_health"]:
                alerts.append({
                    "type": "system_unhealthy",
                    "severity": "critical",
                    "message": "Sistema de seguridad no saludable",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Alerta: Muchas IPs únicas (posible ataque)
            if metrics["login_attempts"]["unique_ips"] > 10:
                alerts.append({
                    "type": "suspicious_ips",
                    "severity": "warning",
                    "message": f"Muchas IPs únicas: {metrics['login_attempts']['unique_ips']}",
                    "timestamp": datetime.now().isoformat()
                })
            
        except Exception as e:
            logger.error(f"Error generando alertas: {e}")
            alerts.append({
                "type": "monitoring_error",
                "severity": "critical",
                "message": f"Error en monitoreo: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts
    
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """Limpiar datos antiguos"""
        try:
            db = next(get_db())
            
            # Ejecutar procedimiento de limpieza
            db.execute(text("EXEC security.sp_cleanup_old_records :days_to_keep"), {
                "days_to_keep": days_to_keep
            })
            
            db.commit()
            logger.info(f"Datos antiguos limpiados (manteniendo {days_to_keep} días)")
            
        except Exception as e:
            logger.error(f"Error limpiando datos antiguos: {e}")

# Instancia global del monitor
security_monitor = SecurityMonitor() 