from jose import JWTError, jwt
from datetime import datetime, timedelta
from decouple import config
import secrets
import base64

# Generate a secret key
def generate_secret_key():
    secret_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    return secret_key

SECRET_KEY = config("SECRET_KEY", default=generate_secret_key())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify Token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None

