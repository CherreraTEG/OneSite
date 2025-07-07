from sqlalchemy.ext.declarative import declarative_base
from app.db.databases import get_main_db, get_saturno13_db, get_companies_db

# Base declarativa para los modelos
Base = declarative_base()

# Dependencies para compatibilidad
def get_db():
    """Dependency para la base de datos principal (compatibilidad)"""
    return get_main_db()

# Exportar las nuevas dependencies
__all__ = ['Base', 'get_db', 'get_main_db', 'get_saturno13_db', 'get_companies_db'] 