from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from models.gps import GPSCreate, GPSResponse
from database import get_database
from bson import ObjectId

router = APIRouter()


@router.post("/api/gps", response_model=GPSResponse, status_code=201)
async def create_gps(gps: GPSCreate):
    db = get_database()
    gps_dict = gps.model_dump()
    gps_dict["created_at"] = datetime.utcnow()

    result = await db.gps_coordinates.insert_one(gps_dict)
    created_gps = await db.gps_coordinates.find_one({"_id": result.inserted_id})
    created_gps["_id"] = str(created_gps["_id"])

    return created_gps


@router.get("/api/gps", response_model=List[GPSResponse])
async def get_gps_coordinates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    db = get_database()
    gps_coords = []
    cursor = db.gps_coordinates.find().skip(skip).limit(limit).sort("created_at", -1)

    async for gps in cursor:
        gps["_id"] = str(gps["_id"])
        gps_coords.append(gps)

    return gps_coords


@router.get("/api/gps/{gps_id}", response_model=GPSResponse)
async def get_gps(gps_id: str):
    db = get_database()

    if not ObjectId.is_valid(gps_id):
        raise HTTPException(status_code=400, detail="Invalid GPS ID format")

    gps = await db.gps_coordinates.find_one({"_id": ObjectId(gps_id)})

    if not gps:
        raise HTTPException(status_code=404, detail="GPS coordinate not found")

    gps["_id"] = str(gps["_id"])
    return gps
