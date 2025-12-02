from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from models.vlog import VlogCreate, VlogResponse
from database import get_database
from bson import ObjectId

router = APIRouter()


@router.post("/api/vlogs", response_model=VlogResponse, status_code=201)
async def create_vlog(vlog: VlogCreate):
    db = get_database()
    vlog_dict = vlog.model_dump()
    vlog_dict["created_at"] = datetime.utcnow()
    vlog_dict["updated_at"] = datetime.utcnow()

    result = await db.vlogs.insert_one(vlog_dict)
    created_vlog = await db.vlogs.find_one({"_id": result.inserted_id})
    created_vlog["_id"] = str(created_vlog["_id"])

    return created_vlog


@router.get("/api/vlogs", response_model=List[VlogResponse])
async def get_vlogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    db = get_database()
    vlogs = []
    cursor = db.vlogs.find().skip(skip).limit(limit).sort("created_at", -1)

    async for vlog in cursor:
        vlog["_id"] = str(vlog["_id"])
        vlogs.append(vlog)

    return vlogs


@router.get("/api/vlogs/{vlog_id}", response_model=VlogResponse)
async def get_vlog(vlog_id: str):
    db = get_database()

    if not ObjectId.is_valid(vlog_id):
        raise HTTPException(status_code=400, detail="Invalid vlog ID format")

    vlog = await db.vlogs.find_one({"_id": ObjectId(vlog_id)})

    if not vlog:
        raise HTTPException(status_code=404, detail="Vlog not found")

    vlog["_id"] = str(vlog["_id"])
    return vlog
