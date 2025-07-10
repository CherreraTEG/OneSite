#!/usr/bin/env python3
"""
Script para probar la conexión SSL/TLS con Active Directory
"""
import os
import sys
import ssl
from ldap3 import Server, Connection, ALL, Tls
from ldap3.core.exceptions import LDAPException
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ssl_connection():
    """Probar diferentes configuraciones SSL"""
    
    # Configuración del servidor AD
    ad_server = "10.50.5.200"
    ad_port = 636
    ad_domain = "elite.local"
    
    # Buscar certificado
    cert_paths = [
        'elite-clean-chain.pem',
        'elite-full-chain.pem',
        'elite-ca-cert.pem',
        'elite-ad-chain.pem',
        '/mnt/c/Cursor/OneSite/backend/elite-clean-chain.pem'
    ]
    
    cert_path = None
    for path in cert_paths:
        if os.path.exists(path):
            cert_path = path
            logger.info(f"Encontrado certificado: {cert_path}")
            break
    
    if not cert_path:
        logger.warning("No se encontró certificado, probando sin certificado específico")
    
    # Configuraciones SSL a probar
    ssl_configs = [
        {
            "name": "SSL Estricto with certificado específico",
            "tls": Tls(
                validate=ssl.CERT_REQUIRED,
                ca_certs_file=cert_path,
                version=ssl.PROTOCOL_TLS_CLIENT,
                ciphers='HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA'
            ) if cert_path else None
        },
        {
            "name": "SSL Estricto con certificados del sistema",
            "tls": Tls(
                validate=ssl.CERT_REQUIRED,
                version=ssl.PROTOCOL_TLS_CLIENT,
                ciphers='HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA'
            )
        },
        {
            "name": "SSL Estricto básico con certificado específico",
            "tls": Tls(
                validate=ssl.CERT_REQUIRED,
                ca_certs_file=cert_path
            ) if cert_path else None
        },
        {
            "name": "SSL Relajado (no recomendado para producción)",
            "tls": Tls(
                validate=ssl.CERT_NONE
            )
        }
    ]
    
    results = []
    
    for config in ssl_configs:
        if config["tls"] is None:
            logger.info(f"Saltando configuración: {config['name']} (no disponible)")
            continue
            
        logger.info(f"Probando configuración: {config['name']}")
        
        try:
            # Crear servidor
            server = Server(
                ad_server,
                get_info=ALL,
                port=ad_port,
                use_ssl=True,
                tls=config["tls"]
            )
            
            # Probar conexión básica
            test_conn = Connection(server)
            
            # Intentar bind anónimo para probar la conexión SSL
            if test_conn.bind():
                logger.info(f"✅ {config['name']}: Conexión SSL exitosa")
                results.append((config["name"], "✅ EXITOSO", "Conexión SSL establecida"))
                test_conn.unbind()
            else:
                logger.info(f"⚠️ {config['name']}: Conexión SSL establecida, pero bind falló (esperado)")
                results.append((config["name"], "⚠️ PARCIAL", "SSL OK, bind falló (esperado)"))
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ {config['name']}: Error - {error_msg}")
            results.append((config["name"], "❌ ERROR", error_msg))
    
    # Mostrar resumen
    logger.info("\n" + "="*80)
    logger.info("RESUMEN DE PRUEBAS SSL")
    logger.info("="*80)
    
    for name, status, details in results:
        logger.info(f"{status} {name}")
        logger.info(f"   Detalles: {details}")
        logger.info("")
    
    # Recomendaciones
    logger.info("RECOMENDACIONES:")
    logger.info("- Usar la primera configuración exitosa para producción")
    logger.info("- Evitar configuraciones 'SSL Relajado' en producción")
    logger.info("- Asegurar que el certificado sea válido y esté actualizado")
    
    return results

if __name__ == "__main__":
    logger.info("Iniciando pruebas de conexión SSL con Active Directory")
    logger.info("="*80)
    
    try:
        results = test_ssl_connection()
        
        # Determinar el resultado general
        successful_configs = [r for r in results if "✅" in r[1]]
        
        if successful_configs:
            logger.info(f"\n🎉 Se encontraron {len(successful_configs)} configuraciones SSL exitosas")
            sys.exit(0)
        else:
            logger.error("\n❌ No se pudo establecer conexión SSL con ninguna configuración")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error ejecutando pruebas: {e}")
        sys.exit(1)