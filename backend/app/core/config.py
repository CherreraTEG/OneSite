from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    # Configuración general
    PROJECT_NAME: str = "OneSite"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Configuración de la base de datos
    DB_SERVER: str = os.getenv("DB_SERVER")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    
    # Configuración de JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "https://teg.1sitesoft.com").split(",")
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
    CORS_METHODS: List[str] = os.getenv("CORS_METHODS", "*").split(",")
    CORS_HEADERS: List[str] = os.getenv("CORS_HEADERS", "*").split(",")
    
    # URL de la base de datos
    @property
    def DATABASE_URL(self) -> str:
        return f"mssql+pymssql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia cacheada de la configuración.
    Esto evita tener que leer el archivo .env múltiples veces.
    """
    return Settings()

# Instancia global de configuración
settings = get_settings() 