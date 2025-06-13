from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

# Doctor Entity
class DoctorCreate(BaseModel):
    full_name: str
    email: EmailStr
    speciality: str
    available: Optional[bool] = True

class DoctorResponse(BaseModel):
    id : str = Field(..., alias="_id")
    full_name: str
    email: EmailStr
    speciality: str
    available: Optional[bool]

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}
