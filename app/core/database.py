import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgresql:1l8TBIbausK6TwyOBP1jfGOZT4EXHjTI@localhost:5432/dbname_cektL")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()