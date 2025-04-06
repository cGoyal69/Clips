import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from sqlalchemy import create_engine

engine = create_engine("postgresql://postgresql:1l8TBIbausK6TwyOBP1jfGOZT4EXHjTI@dpg-cvp8u3i4d50c73bq8akg-a.oregon-postgres.render.com/dbname_cekt?sslmode=require")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()