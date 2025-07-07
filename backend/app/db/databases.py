from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# =============================================================================
# CONFIGURACIÓN DE MÚLTIPLES BASES DE DATOS
# =============================================================================

class DatabaseManager:
    """Gestor de múltiples conexiones de bases de datos"""
    
    def __init__(self):
        self._engines = {}
        self._sessions = {}
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Inicializa las conexiones a las bases de datos"""
        
        # Base de datos principal (OneSite)
        if all([settings.DB_SERVER, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD]):
            self._engines['main'] = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300
            )
            self._sessions['main'] = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self._engines['main']
            )
            print(f"✅ Conexión a base de datos principal: {settings.DB_SERVER}/{settings.DB_NAME}")
        
        # Base de datos SATURNO13 (TheEliteGroup)
        if all([settings.SATURNO13_SERVER, settings.SATURNO13_DB, settings.SATURNO13_USER, settings.SATURNO13_PASSWORD]):
            self._engines['saturno13'] = create_engine(
                settings.SATURNO13_DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300
            )
            self._sessions['saturno13'] = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self._engines['saturno13']
            )
            print(f"✅ Conexión a SATURNO13: {settings.SATURNO13_SERVER}/{settings.SATURNO13_DB}")
        
        # Base de datos JUPITER12MIA (EFLOWER_Reports)
        if all([settings.JUPITER12MIA_SERVER, settings.JUPITER12MIA_DB, settings.JUPITER12MIA_USER, settings.JUPITER12MIA_PASSWORD]):
            self._engines['jupiter12mia'] = create_engine(
                settings.JUPITER12MIA_DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300
            )
            self._sessions['jupiter12mia'] = sessionmaker(
                autocommit=False, 
                autoflush=False, 
                bind=self._engines['jupiter12mia']
            )
            print(f"✅ Conexión a JUPITER12MIA: {settings.JUPITER12MIA_SERVER}/{settings.JUPITER12MIA_DB}")
    
    def get_engine(self, database_name: str = 'main'):
        """Obtiene el engine de una base de datos específica"""
        if database_name not in self._engines:
            raise ValueError(f"Base de datos '{database_name}' no configurada")
        return self._engines[database_name]
    
    def get_session(self, database_name: str = 'main'):
        """Obtiene una sesión de una base de datos específica"""
        if database_name not in self._sessions:
            raise ValueError(f"Base de datos '{database_name}' no configurada")
        return self._sessions[database_name]()
    
    def test_connections(self):
        """Prueba todas las conexiones configuradas"""
        results = {}
        
        for db_name, engine in self._engines.items():
            try:
                with engine.connect() as connection:
                    connection.execute("SELECT 1")
                    results[db_name] = {"status": "success", "message": "Conexión exitosa"}
                    print(f"✅ {db_name}: Conexión exitosa")
            except Exception as e:
                results[db_name] = {"status": "error", "message": str(e)}
                print(f"❌ {db_name}: Error de conexión - {str(e)}")
        
        return results
    
    def close_all(self):
        """Cierra todas las conexiones"""
        for engine in self._engines.values():
            engine.dispose()
        print("🔒 Todas las conexiones cerradas")

# Instancia global del gestor de bases de datos
db_manager = DatabaseManager()

# =============================================================================
# FUNCIONES DE DEPENDENCIA PARA FASTAPI
# =============================================================================

def get_db(database_name: str = 'main'):
    """
    Dependency para obtener una sesión de base de datos.
    
    Args:
        database_name: Nombre de la base de datos ('main' o 'saturno13')
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = db_manager.get_session(database_name)
    try:
        yield db
    finally:
        db.close()

def get_main_db():
    """Dependency para la base de datos principal (OneSite)"""
    return get_db('main')

def get_saturno13_db():
    """Dependency para la base de datos SATURNO13 (TheEliteGroup)"""
    return get_db('saturno13')

def get_jupiter12mia_db():
    """Dependency para la base de datos JUPITER12MIA (EFLOWER_Reports)"""
    return get_db('jupiter12mia')

# =============================================================================
# CONFIGURACIÓN ESPECÍFICA PARA COMPANIES
# =============================================================================

def get_companies_db():
    """
    Dependency específica para el módulo de empresas.
    Usa SATURNO13 si está configurado, sino usa la base principal.
    """
    if settings.USE_SATURNO13_COMPANIES and 'saturno13' in db_manager._engines:
        return get_db('saturno13')
    else:
        return get_db('main') 