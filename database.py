from motor.motor_asyncio import AsyncIOMotorClient
from config import get_settings
import certifi

settings = get_settings()

client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(
        settings.mongodb_uri,
        tlsCAFile=certifi.where()
    )
    db = client[settings.db_name]
    print(f"Connected to MongoDB database: {settings.db_name}")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database():
    return db
