from ldap3 import Server, Connection, SUBTREE, ALL
from typing import Optional, Dict
import os
from app.core.config import settings

class ADAuthService:
    def __init__(self):
        self.server = Server(settings.AD_SERVER, get_info=ALL)
        self.base_dn = settings.AD_BASE_DN
        self.domain = settings.AD_DOMAIN

    async def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica un usuario contra Active Directory.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con la información del usuario si la autenticación es exitosa, None en caso contrario
        """
        try:
            # Construir el DN del usuario
            user_dn = f"{username}@{self.domain}"
            
            # Intentar conexión con las credenciales del usuario
            conn = Connection(
                self.server,
                user=user_dn,
                password=password,
                authentication='SIMPLE',
                auto_bind=True
            )
            
            # Buscar información del usuario
            search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
            conn.search(
                search_base=self.base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['cn', 'mail', 'memberOf', 'displayName']
            )
            
            if conn.entries:
                user_info = conn.entries[0]
                return {
                    'username': username,
                    'email': user_info.mail.value if hasattr(user_info, 'mail') else None,
                    'display_name': user_info.displayName.value if hasattr(user_info, 'displayName') else username,
                    'groups': [group.split(',')[0].split('=')[1] for group in user_info.memberOf.values] if hasattr(user_info, 'memberOf') else []
                }
            
            return None
            
        except Exception as e:
            print(f"Error en autenticación AD: {str(e)}")
            return None
        finally:
            if 'conn' in locals():
                conn.unbind()

# Instancia global del servicio
ad_auth_service = ADAuthService() 