from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SentimentCreate(BaseModel):
    user_id: str
    vlog_id: Optional[str] = None
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    sentiment_label: str
    emotion: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class SentimentResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    vlog_id: Optional[str] = None
    sentiment_score: float
    sentiment_label: str
    emotion: str
    confidence: float
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
