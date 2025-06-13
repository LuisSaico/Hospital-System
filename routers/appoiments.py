from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
from auth.dependecies import get_current_user
from connection import db
from models.appoiment import AppoimentCreate

router = APIRouter(prefix="/appoiments", tags=["Appoiments"])

# EndPoint to get an appoiment
@router.post("/book")
async def book_appoiment(appoiment: AppoimentCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]
    doctor_id = appoiment.doctor_id
    date_time = appoiment.date_time

    # Validate don't have appoiments duplicate
    existing = await db["appoiments"].find_one({
        "user_id" : ObjectId(user_id),
        "doctor_id": ObjectId(doctor_id),
        "date_time": date_time
    })

    if existing:
        raise HTTPException(status_code=400, detail="You already have an appoiment with that doctor that date")

    # Create appoiment
    appoiment_data = {
        "user_id": ObjectId(user_id),
        "doctor_id": ObjectId(doctor_id),
        "date_time": date_time,
        "status": "pending"
    }

    result = await db["appoiments"].insert_one(appoiment_data)
    appoiment_data["_id"] = str(result.inserted_id)
    appoiment_data["user_id"] = str(appoiment_data["user_id"])
    appoiment_data["doctor_id"] = str(appoiment_data["doctor_id"])

    return appoiment_data

# EndPoint to watch your appoiments
@router.get("/my")
async def get_my_appoiments(current_user: dict = Depends(get_current_user)):
    user_id = current_user["_id"]

    cursor = db["appoiments"].find({"user_id": ObjectId(user_id)})
    appoiments = []

    async for appt in cursor:
        appt["_id"] = str(appt["_id"])
        appt["user_id"] = str(appt["user_id"])
        appt["doctor_id"] = str(appt["doctor_id"])
        appoiments.append(appt)

    return appoiments



