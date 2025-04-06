
import os
import sys
from sqlalchemy.orm import Session

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.db.models import Clip

# Sample royalty-free audio clips from Pixabay
sample_clips = [
    {
        "title": "Ambient Nature",
        "description": "Relaxing ambient sounds from the forest",
        "genre": "Ambient",
        "duration": 32.5,
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c2c74d8db1.mp3"
    },
    {
        "title": "Electronic Beat",
        "description": "Upbeat electronic music with synthesizers",
        "genre": "Electronic",
        "duration": 27.8,
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6ff1bab.mp3"
    },
    {
        "title": "Jazz Lounge",
        "description": "Smooth jazz for relaxation",
        "genre": "Jazz",
        "duration": 45.2,
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/02/22/audio_d20eb7f347.mp3"
    },
    {
        "title": "Lo-Fi Study",
        "description": "Lo-fi beats for studying or working",
        "genre": "Lo-Fi",
        "duration": 38.7,
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
    },
    {
        "title": "Cinematic Trailer",
        "description": "Epic orchestral music for trailers",
        "genre": "Cinematic",
        "duration": 52.3,
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/04/27/audio_861a30d565.mp3"
    },
    {
        "title": "Acoustic Folk",
        "description": "Gentle acoustic guitar folk melody",
        "genre": "Folk",
        "duration": 41.6,
        "audio_url": "https://cdn.pixabay.com/download/audio/2021/11/25/audio_a4223d47d9.mp3"
    }
]

def seed_database():
    db = SessionLocal()
    try:
        # Check if database already has clips
        existing_clips = db.query(Clip).count()
        if existing_clips > 0:
            print(f"Database already has {existing_clips} clips. Skipping seed.")
            return
        
        # Add sample clips
        for clip_data in sample_clips:
            clip = Clip(**clip_data)
            db.add(clip)
        
        db.commit()
        print(f"Added {len(sample_clips)} sample clips to the database.")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()