from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VlogCreate(BaseModel):
    user_id: str
    title: str
    content: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None


class VlogResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    title: str
    content: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
