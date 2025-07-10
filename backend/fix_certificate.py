#!/usr/bin/env python3
"""
Script para validar y limpiar certificados SSL
"""
import os
import sys
import logging
import tempfile
import subprocess

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_certificates(cert_file):
    """Extrae certificados individuales de un archivo PEM"""
    try:
        with open(cert_file, 'r') as f:
            content = f.read()
        
        # Dividir por certificados
        certificates = []
        current_cert = ""
        in_cert = False
        
        for line in content.split('\n'):
            if line.strip() == "-----BEGIN CERTIFICATE-----":
                in_cert = True
                current_cert = line + '\n'
            elif line.strip() == "-----END CERTIFICATE-----":
                current_cert += line + '\n'
                certificates.append(current_cert)
                current_cert = ""
                in_cert = False
            elif in_cert:
                current_cert += line + '\n'
        
        return certificates
    except Exception as e:
        logger.error(f"Error extrayendo certificados: {e}")
        return []

def validate_certificate(cert_content):
    """Valida un certificado individual"""
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as temp_file:
            temp_file.write(cert_content)
            temp_file_path = temp_file.name
        
        # Validar con openssl
        result = subprocess.run([
            'openssl', 'x509', '-in', temp_file_path, '-text', '-noout'
        ], capture_output=True, text=True)
        
        # Limpiar archivo temporal
        os.unlink(temp_file_path)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        logger.error(f"Error validando certificado: {e}")
        return False, "", str(e)

def create_clean_certificate_chain():
    """Crea una cadena de certificados limpia"""
    cert_files = [
        'elite-full-chain.pem',
        'elite-ca-cert.pem',
        'elite-ad-chain.pem'
    ]
    
    all_certificates = []
    
    for cert_file in cert_files:
        if os.path.exists(cert_file):
            logger.info(f"Procesando archivo: {cert_file}")
            certificates = extract_certificates(cert_file)
            
            for i, cert in enumerate(certificates):
                is_valid, stdout, stderr = validate_certificate(cert)
                if is_valid:
                    logger.info(f"Certificado {i+1} en {cert_file} es válido")
                    all_certificates.append(cert)
                else:
                    logger.warning(f"Certificado {i+1} en {cert_file} no es válido: {stderr}")
    
    if all_certificates:
        # Crear cadena de certificados limpia
        clean_chain = ''.join(all_certificates)
        
        # Guardar cadena limpia
        with open('elite-clean-chain.pem', 'w') as f:
            f.write(clean_chain)
        
        logger.info("Cadena de certificados limpia creada: elite-clean-chain.pem")
        
        # Validar la cadena final
        is_valid, stdout, stderr = validate_certificate(clean_chain)
        if is_valid:
            logger.info("✅ Cadena de certificados final es válida")
        else:
            logger.warning(f"⚠️ Cadena de certificados final tiene problemas: {stderr}")
            
        return 'elite-clean-chain.pem'
    else:
        logger.error("No se encontraron certificados válidos")
        return None

def main():
    logger.info("Iniciando validación y limpieza de certificados SSL")
    logger.info("="*60)
    
    # Listar archivos de certificados disponibles
    cert_files = [f for f in os.listdir('.') if f.endswith('.pem')]
    logger.info(f"Archivos de certificados encontrados: {cert_files}")
    
    if not cert_files:
        logger.error("No se encontraron archivos de certificados (.pem)")
        return 1
    
    # Crear cadena limpia
    clean_cert_file = create_clean_certificate_chain()
    
    if clean_cert_file:
        logger.info(f"\n✅ Certificado limpio creado: {clean_cert_file}")
        logger.info("Para usar este certificado, configura:")
        logger.info(f"AD_SSL_CERT_PATH={os.path.abspath(clean_cert_file)}")
        return 0
    else:
        logger.error("\n❌ No se pudo crear certificado limpio")
        return 1

if __name__ == "__main__":
    sys.exit(main())