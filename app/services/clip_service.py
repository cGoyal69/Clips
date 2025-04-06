
from sqlalchemy.orm import Session
from typing import List, Optional
import requests
from fastapi import HTTPException, status
from app.db.models import Clip
from app.schemas.clip import ClipCreate

# app/services/clip_service.py

def get_clips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Clip).order_by(Clip.id.asc()).offset(skip).limit(limit).all()

def get_clip(db: Session, clip_id: int) -> Optional[Clip]:
    return db.query(Clip).filter(Clip.id == clip_id).first()

def create_clip(db: Session, clip: ClipCreate) -> Clip:
    db_clip = Clip(
        title=clip.title,
        description=clip.description,
        genre=clip.genre,
        duration=clip.duration,
        audio_url=clip.audio_url
    )
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    return db_clip

def increment_play_count(db: Session, clip_id: int) -> Clip:
    db_clip = get_clip(db, clip_id)
    if not db_clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with id {clip_id} not found"
        )
    
    db_clip.play_count += 1
    db.commit()
    db.refresh(db_clip)
    return db_clip

def get_clip_stats(db: Session, clip_id: int) -> Clip:
    db_clip = get_clip(db, clip_id)
    if not db_clip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Clip with id {clip_id} not found"
        )
    return db_clip