#!/usr/bin/env python3
"""
Script para verificar y limpiar el estado de bloqueo en Redis
"""

import redis
import sys
import os
from datetime import datetime

# Configuración de Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

def connect_redis():
    """Conectar a Redis"""
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        r.ping()
        return r
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")
        return None

def check_user_status(username):
    """Verificar el estado de un usuario específico"""
    r = connect_redis()
    if not r:
        return
    
    lock_key = f"lockout:{username}"
    attempt_key = f"attempts:{username}"
    
    print(f"\n🔍 Verificando estado del usuario: {username}")
    print("=" * 50)
    
    # Verificar si está bloqueado
    is_locked = r.exists(lock_key)
    lock_ttl = r.ttl(lock_key) if is_locked else -1
    
    # Verificar intentos fallidos
    attempts = r.get(attempt_key)
    attempt_ttl = r.ttl(attempt_key) if attempts else -1
    
    print(f"🔒 Estado de bloqueo: {'BLOQUEADO' if is_locked else 'NO BLOQUEADO'}")
    if is_locked:
        print(f"⏰ Tiempo restante de bloqueo: {lock_ttl} segundos ({lock_ttl//60} minutos)")
    
    print(f"❌ Intentos fallidos: {attempts if attempts else 0}")
    if attempts:
        print(f"⏰ TTL de intentos: {attempt_ttl} segundos")
    
    return {
        'is_locked': is_locked,
        'lock_ttl': lock_ttl,
        'attempts': int(attempts) if attempts else 0,
        'attempt_ttl': attempt_ttl
    }

def list_all_locked_users():
    """Listar todos los usuarios bloqueados"""
    r = connect_redis()
    if not r:
        return
    
    print("\n🔍 Usuarios bloqueados actualmente:")
    print("=" * 50)
    
    # Buscar todas las claves de bloqueo
    lock_keys = r.keys("lockout:*")
    
    if not lock_keys:
        print("✅ No hay usuarios bloqueados")
        return
    
    for key in lock_keys:
        username = key.replace("lockout:", "")
        ttl = r.ttl(key)
        print(f"👤 {username}: {ttl} segundos restantes ({ttl//60} minutos)")

def clear_user_lockout(username):
    """Limpiar el bloqueo de un usuario específico"""
    r = connect_redis()
    if not r:
        return
    
    lock_key = f"lockout:{username}"
    attempt_key = f"attempts:{username}"
    
    print(f"\n🧹 Limpiando bloqueo del usuario: {username}")
    print("=" * 50)
    
    # Eliminar bloqueo
    deleted_lock = r.delete(lock_key)
    deleted_attempts = r.delete(attempt_key)
    
    print(f"🔒 Bloqueo eliminado: {'✅' if deleted_lock else '❌'}")
    print(f"❌ Intentos eliminados: {'✅' if deleted_attempts else '❌'}")
    
    if deleted_lock or deleted_attempts:
        print(f"✅ Usuario {username} desbloqueado exitosamente")
    else:
        print(f"ℹ️  El usuario {username} no estaba bloqueado")

def clear_all_lockouts():
    """Limpiar todos los bloqueos"""
    r = connect_redis()
    if not r:
        return
    
    print("\n🧹 Limpiando todos los bloqueos")
    print("=" * 50)
    
    # Buscar todas las claves de bloqueo e intentos
    lock_keys = r.keys("lockout:*")
    attempt_keys = r.keys("attempts:*")
    
    deleted_locks = 0
    deleted_attempts = 0
    
    for key in lock_keys:
        if r.delete(key):
            deleted_locks += 1
    
    for key in attempt_keys:
        if r.delete(key):
            deleted_attempts += 1
    
    print(f"🔒 Bloqueos eliminados: {deleted_locks}")
    print(f"❌ Intentos eliminados: {deleted_attempts}")
    print("✅ Todos los bloqueos han sido limpiados")

def main():
    """Función principal"""
    print("🔧 Herramienta de gestión de bloqueos de OneSite")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\n📋 Uso:")
        print("  python check_redis_status.py check <username>     - Verificar estado de usuario")
        print("  python check_redis_status.py list                 - Listar usuarios bloqueados")
        print("  python check_redis_status.py clear <username>     - Desbloquear usuario específico")
        print("  python check_redis_status.py clear-all            - Desbloquear todos los usuarios")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check" and len(sys.argv) >= 3:
        username = sys.argv[2]
        check_user_status(username)
    
    elif command == "list":
        list_all_locked_users()
    
    elif command == "clear" and len(sys.argv) >= 3:
        username = sys.argv[2]
        clear_user_lockout(username)
    
    elif command == "clear-all":
        clear_all_lockouts()
    
    else:
        print("❌ Comando no válido. Usa 'python check_redis_status.py' para ver la ayuda.")

if __name__ == "__main__":
    main() 