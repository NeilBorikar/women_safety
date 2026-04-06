from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 🔌 CLIENT INITIALIZATION (Lazy connection)
client = AsyncIOMotorClient(
    settings.MONGO_URL,
    serverSelectionTimeoutMS=5000,
    maxPoolSize=50,
    minPoolSize=5
)

# 📦 DATABASE REFERENCE
database = client["women_safety_db"]

# 📂 EXPORTED COLLECTIONS
user_collection = database["users"]
alert_collection = database["alerts"]
location_collection = database["locations"]
evidence_collection = database["evidence"]
notification_collection = database["notifications"]


# 🚀 TEST ROOT CONNECTION ON STARTUP
async def connect_to_mongo():
    try:
        await client.admin.command("ping")
        logger.info("✅ MongoDB connected successfully")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        raise e


# 🛑 GRACEFUL SHUTDOWN
async def close_mongo_connection():
    client.close()
    logger.info("🔌 MongoDB connection closed")