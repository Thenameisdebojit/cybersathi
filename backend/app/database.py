# backend/app/database.py
"""MongoDB database connection and initialization."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging
import os

from app.config import settings
from app.models.complaint import ComplaintDocument
from app.models.user import UserDocument
from app.models.audit_log import AuditLogDocument
from app.models.campaign import CampaignDocument
from app.models.analytics import AnalyticsEventDocument

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize MongoDB connection and Beanie ODM."""
        try:
            # Get MongoDB URL from environment (Replit secret)
            mongodb_url = os.getenv("MONGODB_URL") or settings.MONGODB_URL
            
            logger.info(f"Connecting to MongoDB Atlas...")
            
            cls.client = AsyncIOMotorClient(
                mongodb_url,
                minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            )
            
            # Initialize Beanie with document models
            await init_beanie(
                database=cls.client[settings.MONGODB_DB_NAME],
                document_models=[
                    ComplaintDocument,
                    UserDocument,
                    AuditLogDocument,
                    CampaignDocument,
                    AnalyticsEventDocument,
                ]
            )
            
            logger.info("✅ MongoDB connection established successfully")
            logger.info("ℹ️  Indexes are managed by Beanie via model Settings")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")


# Singleton instance
db = Database()
