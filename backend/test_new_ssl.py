#!/usr/bin/env python3
"""
Script para probar la nueva configuración SSL
"""
import os
import sys
from dotenv import load_dotenv

# Cargar configuración SSL
load_dotenv('.env.ssl')

# Agregar el directorio app al path
sys.path.append('app')

from app.core.security import LDAPAuth
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_new_ssl_config():
    """Probar la nueva configuración SSL"""
    logger.info("Iniciando prueba de nueva configuración SSL")
    logger.info("="*60)
    
    try:
        # Crear instancia de LDAPAuth
        logger.info("Creando instancia de LDAPAuth...")
        ldap_auth = LDAPAuth()
        
        logger.info("✅ Configuración SSL exitosa")
        logger.info(f"Servidor configurado: {ldap_auth.server}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en configuración SSL: {e}")
        return False

if __name__ == "__main__":
    success = test_new_ssl_config()
    sys.exit(0 if success else 1)