from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from models.doctor import DoctorCreate
from connection import db
from auth.dependecies import get_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

# EndPoint to create Doctors
@router.post("/doctors", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: DoctorCreate, admin_user: dict=  Depends(get_admin_user)):
    existing = await db["doctors"].find_one({"email": doctor.email})
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already exists with this email")

    doctor_dict = doctor.dict()
    result = await db["doctors"].insert_one(doctor_dict)
    doctor_dict["_id"] = str(result.inserted_id)
    return doctor_dict