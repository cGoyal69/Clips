import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    PROJECT_NAME: str = "Sound Clip API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "A FastAPI backend for streaming sound clips"

    # Use environment variable or fallback for local dev
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgresql:1l8TBIbausK6TwyOBP1jfGOZT4EXHjTI@dpg-cvp8u3i4d50c73bq8akg-a.oregon-postgres.render.com/dbname_cekt?sslmode=require"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()