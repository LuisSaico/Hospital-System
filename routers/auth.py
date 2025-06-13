from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.collection import Collection
from bson.objectid import ObjectId
from passlib.context import CryptContext
from typing_extensions import deprecated

from connection import db
from models.user import UserCreate, UserResponse
from connection import get_db, users_collection
from auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utils
def hash_paswoord(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# EndPoint to Register User
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_paswoord(user.password)

    user_dict =user.dict()
    user_dict["password"] = hashed_pw
    user_dict["role"] = "user"

    user_dict["birth_date"] = user_dict["birth_date"].isoformat()
    result = await db["users"].insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    user_dict.pop("password")

    return UserResponse(**user_dict)

# EndPoint to login user
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {"user_id": str(user["_id"])}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}





    