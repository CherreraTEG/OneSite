from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache
import os
import json
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
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = json.loads(os.getenv("CORS_ORIGINS", '["https://teg.1sitesoft.com", "http://localhost:4200"]'))
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
    CORS_METHODS: List[str] = json.loads(os.getenv("CORS_METHODS", '["GET", "POST", "PUT", "DELETE"]'))
    CORS_HEADERS: List[str] = json.loads(os.getenv("CORS_HEADERS", '["Authorization", "Content-Type", "X-Requested-With"]'))
    
    # Configuración de Active Directory
    AD_SERVER: str = os.getenv("AD_SERVER", "10.50.5.200")
    AD_PORT: int = int(os.getenv("AD_PORT", "636"))
    AD_USE_SSL: bool = os.getenv("AD_USE_SSL", "True").lower() == "true"
    AD_BASE_DN: str = os.getenv("AD_BASE_DN", "DC=ELITE,DC=local")
    AD_DOMAIN: str = os.getenv("AD_DOMAIN", "elite.local")
    
    # Configuración de seguridad
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "5"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    ACCOUNT_LOCKOUT_MINUTES: int = int(os.getenv("ACCOUNT_LOCKOUT_MINUTES", "15"))
    
    # Configuración de Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "")
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "onesite.log")
    
    # Configuración del entorno
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
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