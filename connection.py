from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# Connecting Database
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")

# Database
client = AsyncIOMotorClient(MONGO_URI)
db = client["hospital"]

# Collections
users_collection = db["users"]
doctors_collection = db["doctors"]
appoiments_collection = db["appoiments"]

# Dependecy
def get_db():
    return db