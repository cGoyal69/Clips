
import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    PROJECT_NAME: str = "Sound Clip API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A FastAPI backend for streaming sound clips"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/soundclip"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()