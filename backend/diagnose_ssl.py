#!/usr/bin/env python3
"""
Script de diagnóstico SSL para OneSite LDAP
Ayuda a identificar problemas de certificados y conectividad
"""

import ssl
import socket
import sys
import os
from ldap3 import Server, Connection, Tls, ALL
from app.core.config import settings

def test_ssl_connection():
    """Prueba la conectividad SSL con el servidor LDAP"""
    print("🔍 Diagnostico SSL para OneSite LDAP")
    print("=" * 50)
    
    # Información del servidor
    print(f"Servidor: {settings.AD_SERVER}")
    print(f"Puerto: {settings.AD_PORT}")
    print(f"SSL Habilitado: {settings.AD_USE_SSL}")
    print(f"Dominio: {settings.AD_DOMAIN}")
    print()
    
    if not settings.AD_USE_SSL:
        print("⚠️ SSL no está habilitado en la configuración")
        return False
    
    # Prueba 1: Conectividad básica de red
    print("1. Probando conectividad de red...")
    try:
        sock = socket.create_connection((settings.AD_SERVER, settings.AD_PORT), timeout=10)
        print("✅ Conectividad de red exitosa")
        sock.close()
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False
    
    # Prueba 2: Certificado SSL
    print("\n2. Verificando certificado SSL...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((settings.AD_SERVER, settings.AD_PORT), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=settings.AD_SERVER) as ssock:
                cert = ssock.getpeercert()
                print(f"✅ Certificado SSL válido")
                print(f"   Sujeto: {cert.get('subject', 'N/A')}")
                print(f"   Emisor: {cert.get('issuer', 'N/A')}")
                print(f"   Válido hasta: {cert.get('notAfter', 'N/A')}")
    except ssl.SSLCertVerificationError as e:
        print(f"⚠️ Error de verificación de certificado: {e}")
        print("   El certificado no es válido o no coincide con el servidor")
    except Exception as e:
        print(f"❌ Error SSL: {e}")
    
    # Prueba 3: Conexión LDAP con SSL estricto
    print("\n3. Probando conexión LDAP con SSL estricto...")
    try:
        tls_configuration = Tls(validate=ssl.CERT_REQUIRED)
        server = Server(
            settings.AD_SERVER,
            get_info=ALL,
            port=settings.AD_PORT,
            use_ssl=True,
            tls=tls_configuration
        )
        
        conn = Connection(server)
        conn.bind()
        
        if conn.bound:
            print("✅ Conexión LDAP con SSL estricto exitosa")
            conn.unbind()
            return True
        else:
            print("❌ Conexión LDAP con SSL estricto falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en conexión SSL estricta: {e}")
        
        # Prueba 4: Conexión LDAP con SSL relajado
        print("\n4. Probando conexión LDAP con SSL relajado...")
        try:
            tls_configuration = Tls(validate=ssl.CERT_NONE)
            server = Server(
                settings.AD_SERVER,
                get_info=ALL,
                port=settings.AD_PORT,
                use_ssl=True,
                tls=tls_configuration
            )
            
            conn = Connection(server)
            conn.bind()
            
            if conn.bound:
                print("⚠️ Conexión LDAP con SSL relajado exitosa")
                print("   RECOMENDACIÓN: Configurar certificados SSL válidos")
                conn.unbind()
                return True
            else:
                print("❌ Conexión LDAP con SSL relajado también falló")
                return False
                
        except Exception as e2:
            print(f"❌ Error en conexión SSL relajada: {e2}")
            return False
    
    return False

def generate_recommendations():
    """Genera recomendaciones basadas en el diagnóstico"""
    print("\n📋 RECOMENDACIONES:")
    print("=" * 30)
    
    print("1. Para desarrollo:")
    print("   - Usar SSL relajado temporalmente")
    print("   - Configurar ENVIRONMENT=development")
    
    print("\n2. Para producción:")
    print("   - Obtener certificados SSL válidos del servidor LDAP")
    print("   - Usar nombre DNS en lugar de IP para AD_SERVER")
    print("   - Configurar ENVIRONMENT=production")
    
    print("\n3. Configuración de certificados:")
    print("   - Contactar al administrador de AD")
    print("   - Verificar que el certificado incluya el nombre del servidor")
    print("   - Asegurar que la CA esté en el almacén de certificados")

def main():
    """Función principal del diagnóstico"""
    try:
        success = test_ssl_connection()
        generate_recommendations()
        
        if success:
            print("\n✅ Diagnóstico completado - Conexión SSL funcional")
            sys.exit(0)
        else:
            print("\n❌ Diagnóstico completado - Problemas detectados")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error en diagnóstico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 