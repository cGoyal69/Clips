import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import requests
from app.core.database import get_db
from app.db.models import Clip
from app.schemas.clip import ClipResponse, ClipCreate, ClipStats
from app.services.clip_service import (
    get_clips, 
    get_clip, 
    create_clip, 
    increment_play_count, 
    get_clip_stats
)

router = APIRouter(
    prefix="/clips",
    tags=["clips"]
)

@router.get("/", response_model=List[ClipResponse])
def read_clips(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clips = get_clips(db, skip=skip, limit=limit)
    return clips

@router.get("/{clip_id}", response_model=ClipResponse)
def read_clip(clip_id: int, db: Session = Depends(get_db)):
    clip = get_clip(db, clip_id)
    if clip is None:
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip

@router.get("/{clip_id}/stream")
def stream_clip(clip_id: int, db: Session = Depends(get_db)):
    clip = get_clip(db, clip_id)
    if clip is None:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    # Increment play count
    increment_play_count(db, clip_id)
    
    try:
        # For hosted clips, we'll stream the MP3 file
        response = requests.get(clip.audio_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve audio file"
            )
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    tmp.write(chunk)
            tmp_path = tmp.name
        
        # Use FileResponse to stream the audio file
        return FileResponse(
            path=tmp_path,
            media_type="audio/mpeg",
            filename=f"{clip.title}.mp3",
            headers={"Content-Disposition": f"attachment; filename={clip.title}.mp3"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error streaming audio: {str(e)}"
        )

@router.get("/{clip_id}/stats", response_model=ClipStats)
def read_clip_stats(clip_id: int, db: Session = Depends(get_db)):
    return get_clip_stats(db, clip_id)

@router.post("/", response_model=ClipResponse, status_code=status.HTTP_201_CREATED)
def create_new_clip(clip: ClipCreate, db: Session = Depends(get_db)):
    return create_clip(db, clip)