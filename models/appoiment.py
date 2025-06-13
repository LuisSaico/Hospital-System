from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

# Appoiment Entity
class AppoimentCreate(BaseModel):
    doctor_id: str
    date_time: datetime
    reason: Optional[str]
    status: Literal["pending", "confirmed", "canceled"] = "pending"

class AppoimentResponse(BaseModel):
    id: str = Field(..., alias="_id")
    patient_id: str
    doctor_id: str
    date_time: datetime
    reason: Optional[str]
    status: str

    class Config:
            allow_population_by_field_name = True
            arbitrary_types_allowed = True
            json_encoders = {ObjectId: str}