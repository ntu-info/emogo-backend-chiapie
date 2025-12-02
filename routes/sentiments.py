from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from models.sentiment import SentimentCreate, SentimentResponse
from database import get_database
from bson import ObjectId

router = APIRouter()


@router.post("/api/sentiments", response_model=SentimentResponse, status_code=201)
async def create_sentiment(sentiment: SentimentCreate):
    db = get_database()
    sentiment_dict = sentiment.model_dump()
    sentiment_dict["created_at"] = datetime.utcnow()

    result = await db.sentiments.insert_one(sentiment_dict)
    created_sentiment = await db.sentiments.find_one({"_id": result.inserted_id})
    created_sentiment["_id"] = str(created_sentiment["_id"])

    return created_sentiment


@router.get("/api/sentiments", response_model=List[SentimentResponse])
async def get_sentiments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    db = get_database()
    sentiments = []
    cursor = db.sentiments.find().skip(skip).limit(limit).sort("created_at", -1)

    async for sentiment in cursor:
        sentiment["_id"] = str(sentiment["_id"])
        sentiments.append(sentiment)

    return sentiments


@router.get("/api/sentiments/{sentiment_id}", response_model=SentimentResponse)
async def get_sentiment(sentiment_id: str):
    db = get_database()

    if not ObjectId.is_valid(sentiment_id):
        raise HTTPException(status_code=400, detail="Invalid sentiment ID format")

    sentiment = await db.sentiments.find_one({"_id": ObjectId(sentiment_id)})

    if not sentiment:
        raise HTTPException(status_code=404, detail="Sentiment not found")

    sentiment["_id"] = str(sentiment["_id"])
    return sentiment
