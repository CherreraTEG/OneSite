from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ldap_connection():
    try:
        # Configuración del servidor LDAP
        server = Server(
            "10.50.5.200",  # Servidor LDAP de Elite
            get_info=ALL,
            port=389,
            use_ssl=False
        )
        logger.info("Servidor LDAP configurado")

        # Intentar conexión con credenciales de prueba
        user_dn = "cherrera@elite.local"  # Formato UPN (User Principal Name)
        password = "Mi@mi.2024*"
        
        logger.info(f"Intentando conexión LDAP con: {user_dn}")
        
        # Crear conexión LDAP
        conn = Connection(
            server,
            user=user_dn,
            password=password,
            authentication=SIMPLE,
            auto_bind=True,
            receive_timeout=10,
            read_only=True
        )
        
        if conn.bound:
            logger.info("✅ Conexión LDAP exitosa")
            
            # Buscar información del usuario
            search_filter = '(&(objectClass=user)(sAMAccountName=cherrera))'
            search_base = 'DC=ELITE,DC=local'
            
            logger.info(f"Buscando usuario con filtro: {search_filter}")
            logger.info(f"Base de búsqueda: {search_base}")
            
            conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['cn', 'mail', 'memberOf']
            )
            
            if conn.entries:
                logger.info("✅ Usuario encontrado en el Directorio Activo")
                for entry in conn.entries:
                    logger.info(f"Nombre: {entry.cn}")
                    logger.info(f"Email: {entry.mail}")
                    logger.info(f"Grupos: {entry.memberOf}")
            else:
                logger.warning("⚠️ Usuario no encontrado en el Directorio Activo")
            
            conn.unbind()
            return True
        else:
            logger.error("❌ La conexión LDAP no se pudo establecer")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error de conexión LDAP: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n=== Prueba de Conexión al Directorio Activo ===\n")
    if test_ldap_connection():
        print("\n✅ La conexión al Directorio Activo fue exitosa")
    else:
        print("\n❌ La conexión al Directorio Activo falló") 