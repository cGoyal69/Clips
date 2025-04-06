# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.db.models import Clip

# Use your PostgreSQL Render database here (ideally a test DB)
POSTGRES_TEST_DATABASE_URL = (
    "postgresql://postgresql:1l8TBIbausK6TwyOBP1jfGOZT4EXHjTI@dpg-cvp8u3i4d50c73bq8akg-a.oregon-postgres.render.com/dbname_cekt?sslmode=require"
)

engine = create_engine(POSTGRES_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    """Create and seed the test DB"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Clean previous test data
    db.query(Clip).delete()
    db.commit()

    test_clips = [
        Clip(
            title="Test Clip 1",
            description="This is a test clip",
            genre="Test",
            duration=10.5,
            audio_url="https://example.com/test1.mp3",
            play_count=0
        ),
        Clip(
            title="Test Clip 2",
            description="Another test clip",
            genre="Sample",
            duration=20.0,
            audio_url="https://example.com/test2.mp3",
            play_count=5
        )
    ]

    db.add_all(test_clips)
    db.commit()
    yield db

    db.close()
    # Optionally clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module", autouse=True)
def override_dependency(test_db):
    """Override FastAPI's get_db dependency to use our test session."""
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
    """Return a FastAPI test client."""
    with TestClient(app) as c:
        yield c


def test_read_clips(client):
    response = client.get("/api/clips")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_read_clip(client):
    response = client.get("/api/clips/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Clip 1"


def test_clip_not_found(client):
    response = client.get("/api/clips/999")
    assert response.status_code == 404


def test_get_clip_stats(client):
    response = client.get("/api/clips/2/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["play_count"] == 5


def test_create_clip(client):
    new_clip = {
        "title": "New Test Clip",
        "description": "A newly created clip",
        "genre": "New",
        "duration": 15.5,
        "audio_url": "https://example.com/new.mp3"
    }
    response = client.post("/api/clips/", json=new_clip)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Test Clip"

    # Confirm new clip is added
    response = client.get(f"/api/clips/{data['id']}")
    assert response.status_code == 200