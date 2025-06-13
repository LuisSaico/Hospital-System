from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# User Entity
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    birth_date: Optional[date]

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    full_name: str
    email: EmailStr
    birth_date: Optional[date]
    role: str

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}