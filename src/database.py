from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.database_name]
