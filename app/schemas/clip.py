
from pydantic import BaseModel, HttpUrl
from typing import Optional

class ClipBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: str
    duration: float  # Duration in seconds
    audio_url: str

class ClipCreate(ClipBase):
    pass

class ClipResponse(ClipBase):
    id: int
    play_count: int = 0
    
    class Config:
        from_attributes = True

class ClipStats(BaseModel):
    id: int
    title: str
    play_count: int
    
    class Config:
        from_attributes = True