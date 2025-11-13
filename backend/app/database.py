# backend/app/database.py
"""MongoDB database connection and initialization."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging

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
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
            
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
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
            
            # Create indexes
            await cls.create_indexes()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")
    
    @classmethod
    async def create_indexes(cls):
        """Create database indexes for performance."""
        try:
            db = cls.client[settings.MONGODB_DB_NAME]
            
            # Complaints indexes
            complaints = db.complaints
            await complaints.create_index("reference_id", unique=True)
            await complaints.create_index("phone")
            await complaints.create_index("status")
            await complaints.create_index("created_at")
            await complaints.create_index([("phone", 1), ("created_at", -1)])
            
            # Users indexes
            users = db.users
            await users.create_index("email", unique=True)
            await users.create_index("phone")
            await users.create_index("role")
            
            # Audit logs indexes
            audit_logs = db.audit_logs
            await audit_logs.create_index("user_id")
            await audit_logs.create_index("action")
            await audit_logs.create_index("timestamp")
            await audit_logs.create_index([("user_id", 1), ("timestamp", -1)])
            
            # Analytics indexes
            analytics = db.analytics_events
            await analytics.create_index("event_type")
            await analytics.create_index("timestamp")
            await analytics.create_index([("event_type", 1), ("timestamp", -1)])
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Index creation warning: {e}")


# Singleton instance
db = Database()
