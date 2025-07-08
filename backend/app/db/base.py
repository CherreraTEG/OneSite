from sqlalchemy.ext.declarative import declarative_base

# Base declarativa para los modelos
Base = declarative_base()

# Importar todos los modelos aquí para asegurar las relaciones
from app.models.user import User
from app.models.role import Role
from app.models.company import Company
from app.models.trucks import Truck
from app.models.permisos import Permiso
from app.models.user_company_permission import UserCompanyPermission

# Dependencies para compatibilidad
from app.db.databases import get_main_db, get_saturno13_db, get_companies_db

def get_db():
    """Dependency para la base de datos principal (compatibilidad)"""
    return get_main_db()

# Exportar las nuevas dependencies y modelos
__all__ = ['Base', 'get_db', 'get_main_db', 'get_saturno13_db', 'get_companies_db', 'User', 'Role', 'Company', 'Truck', 'Permiso', 'UserCompanyPermission'] 