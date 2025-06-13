from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .jwt_handler import verify_access_token
from connection import db
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Invalid Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    if not user_id:
        raise credentials_exception

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise credentials_exception

    return user

def get_admin_user(current_user: dict= Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can perfom this action")

    return current_user
