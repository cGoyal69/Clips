# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.db.models import Clip

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database and seed with test data
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    
    # Create test data
    db = TestingSessionLocal()
    test_clips = [
        {
            "title": "Test Clip 1",
            "description": "This is a test clip",
            "genre": "Test",
            "duration": 10.5,
            "audio_url": "https://example.com/test1.mp3",
            "play_count": 0
        },
        {
            "title": "Test Clip 2",
            "description": "Another test clip",
            "genre": "Sample",
            "duration": 20.0,
            "audio_url": "https://example.com/test2.mp3",
            "play_count": 5
        }
    ]
    
    for clip_data in test_clips:
        clip = Clip(**clip_data)
        db.add(clip)
    
    db.commit()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Override dependency to use test database
@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

def test_read_clips(client):
    """Test getting all clips"""
    response = client.get("/api/clips")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Clip 1"
    assert data[1]["title"] == "Test Clip 2"

def test_read_clip(client):
    """Test getting a single clip"""
    response = client.get("/api/clips/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Clip 1"
    assert data["genre"] == "Test"

def test_clip_not_found(client):
    """Test getting a non-existent clip"""
    response = client.get("/api/clips/999")
    assert response.status_code == 404

def test_get_clip_stats(client):
    """Test getting clip stats"""
    response = client.get("/api/clips/2/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Clip 2"
    assert data["play_count"] == 5

def test_create_clip(client):
    """Test creating a new clip"""
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
    assert data["play_count"] == 0
    
    # Verify it's in the database
    response = client.get("/api/clips/3")
    assert response.status_code == 200