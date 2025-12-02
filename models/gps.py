from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GPSCreate(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    timestamp: datetime


class GPSResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    timestamp: datetime
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
