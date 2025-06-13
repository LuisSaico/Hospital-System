from fastapi import APIRouter
from connection import db
from bson import ObjectId

router = APIRouter(prefix="/public", tags=["Public"])

# Endpoint to list doctors
@router.get("/doctors")
async def list_dosctor():
    doctors_cursor = db["doctors"].find()
    doctors = []

    async for doctor in doctors_cursor:
        doctor["_id"] = str(doctor["_id"])
        doctors.append(doctor)
    return doctors

# EndPoint to list specialties
@router.get("/specialties")
async def list_specialties():
    specialties = await db["doctors"].distinct("specialty")
    return specialties