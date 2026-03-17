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
    using_mock: bool = False
    
    @classmethod
    async def connect_db(cls):
        """Initialize MongoDB connection and Beanie ODM with fallback to in-memory database."""
        import json
        from datetime import datetime
        
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:26","message":"connect_db entry","data":{},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        try:
            # Get MongoDB URL from environment (Replit secret)
            mongodb_url = os.getenv("MONGODB_URL") or settings.MONGODB_URL
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:30","message":"MongoDB URL retrieved","data":{"has_env_url":bool(os.getenv("MONGODB_URL")),"mongodb_url_set":bool(mongodb_url),"is_localhost":"localhost" in mongodb_url if mongodb_url else False},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            logger.info(f"Connecting to MongoDB...")
            
            # Try to connect to MongoDB
            try:
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:36","message":"before AsyncIOMotorClient creation","data":{},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                cls.client = AsyncIOMotorClient(
                    mongodb_url,
                    minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                    maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                )
                
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:45","message":"before ping test","data":{},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                # Test the connection
                await cls.client.admin.command('ping')
                cls.using_mock = False
                
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:46","message":"MongoDB ping successful","data":{"using_mock":False},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                logger.info("✅ MongoDB connection established successfully")
                
            except Exception as conn_error:
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:49","message":"MongoDB connection failed, using mock","data":{"error_type":type(conn_error).__name__,"error_msg":str(conn_error)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                # Fallback to in-memory mock database
                logger.warning(f"⚠️  Could not connect to MongoDB: {conn_error}")
                logger.info("🔄 Falling back to in-memory database (mongomock)...")
                
                from mongomock_motor import AsyncMongoMockClient
                cls.client = AsyncMongoMockClient()
                cls.using_mock = True
                
                # #region agent log
                try:
                    with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:56","message":"Mock database initialized","data":{"using_mock":True},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
                except: pass
                # #endregion
                
                logger.info("✅ In-memory database initialized successfully")
                logger.info("ℹ️  Note: Data will not persist after restart")
            
            # Initialize Beanie with document models
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:61","message":"before init_beanie","data":{"db_name":settings.MONGODB_DB_NAME},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
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
            
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:72","message":"init_beanie completed","data":{"using_mock":cls.using_mock},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            logger.info("ℹ️  Indexes are managed by Beanie via model Settings")
            
        except Exception as e:
            # #region agent log
            try:
                with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"database.py:74","message":"database initialization error","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
            except: pass
            # #endregion
            
            logger.error(f"❌ Failed to initialize database: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")


# Singleton instance
db = Database()
