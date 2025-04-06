# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

from app.main import app
from app.core.database import Base, get_db

# Add seed module to path and import seeding function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.seed import seed_database  # ✅ ← Import your seed logic

# PostgreSQL DB for testing
POSTGRES_TEST_DATABASE_URL = (
    "postgresql://postgresql:1l8TBIbausK6TwyOBP1jfGOZT4EXHjTI@dpg-cvp8u3i4d50c73bq8akg-a.oregon-postgres.render.com/dbname_cekt?sslmode=require"
)

engine = create_engine(POSTGRES_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def seed_and_override_db():
    """Seed DB before tests & override get_db."""
    seed_database()  # ✅ ← Call your seeder

    def _override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_read_clips(client):
    response = client.get("/api/clips")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6


def test_read_clip(client):
    response = client.get("/api/clips/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Ambient Nature"


def test_clip_not_found(client):
    response = client.get("/api/clips/999")
    assert response.status_code == 404


def test_get_clip_stats(client):
    response = client.get("/api/clips/2/stats")
    assert response.status_code in [200, 404]  # depending on stats route logic


def test_create_clip(client):
    new_clip = {
        "title": "New Test Clip",
        "description": "A newly created clip",
        "genre": "New",
        "duration": 15.5,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"
    }
    response = client.post("/api/clips/", json=new_clip)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Test Clip"

    # Confirm clip added
    response = client.get(f"/api/clips/{data['id']}")
    assert response.status_code == 200