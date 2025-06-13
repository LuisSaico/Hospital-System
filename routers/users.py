from fastapi import APIRouter, Depends
from auth.dependecies import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])

# EndPoint to get your account
@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    user = current_user.copy()
    user["_id"] = str(user["_id"])
    return user
