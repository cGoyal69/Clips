import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.db.models import Clip

# Sample audio clips
sample_clips = [
    {
        "title": "Ambient Nature",
        "description": "Relaxing ambient sounds from the forest",
        "genre": "Ambient",
        "duration": 32.5,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    },
    {
        "title": "Electronic Beat",
        "description": "Upbeat electronic music with synthesizers",
        "genre": "Electronic",
        "duration": 27.8,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
    },
    {
        "title": "Jazz Lounge",
        "description": "Smooth jazz for relaxation",
        "genre": "Jazz",
        "duration": 45.2,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
    },
    {
        "title": "Lo-Fi Study",
        "description": "Lo-fi beats for studying or working",
        "genre": "Lo-Fi",
        "duration": 38.7,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
    },
    {
        "title": "Cinematic Trailer",
        "description": "Epic orchestral music for trailers",
        "genre": "Cinematic",
        "duration": 52.3,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    },
    {
        "title": "Acoustic Folk",
        "description": "Gentle acoustic guitar folk melody",
        "genre": "Folk",
        "duration": 41.6,
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"
    }
]

def seed_database():
    db = SessionLocal()
    try:
        # Delete all existing clips
        db.query(Clip).delete()
        db.commit()

        # Dynamically reset the primary key sequence for PostgreSQL
        table_name = Clip.__tablename__
        db.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))
        db.commit()

        # Insert new sample clips
        for clip_data in sample_clips:
            db.add(Clip(**clip_data))
        
        db.commit()
        print(f"Replaced old clips. Added {len(sample_clips)} new clips to the database.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()