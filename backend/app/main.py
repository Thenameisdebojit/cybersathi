# backend/app/main.py
"""FastAPI application with MongoDB, authentication, and WhatsApp integration."""
import uvicorn
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.database import db
from app.routers import auth, complaints, tracking, escalation, whatsapp_webhook, analytics
from app.services.auth import AuthService
from app.models.user import UserDocument, UserRole, UserStatus

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    # Startup
    logger.info("🚀 Starting CyberSathi Backend...")
    
    db_connected = False
    import json
    from datetime import datetime
    
    # #region agent log
    try:
        with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:31","message":"lifespan startup - before db.connect_db","data":{},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
    except: pass
    # #endregion
    
    try:
        # Try to connect to MongoDB Atlas
        await db.connect_db()
        logger.info("✅ MongoDB Atlas connected successfully")
        db_connected = True
        
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:36","message":"db.connect_db successful","data":{"using_mock":db.using_mock if hasattr(db,'using_mock') else None},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        # Create default admin user if not exists
        await create_default_admin()
        
    except Exception as e:
        # #region agent log
        try:
            with open(r'd:\cybersathi\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:41","message":"db.connect_db failed","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
        except: pass
        # #endregion
        
        logger.warning(f"⚠️  MongoDB connection failed: {e}")
        logger.warning("⚠️  Starting in limited mode - database features unavailable")
        logger.warning("ℹ️  Please configure MONGODB_URL in backend/.env with your MongoDB Atlas connection string")
        logger.warning("ℹ️  Get free MongoDB Atlas at: https://www.mongodb.com/cloud/atlas")
    
    logger.info(f"🌟 CyberSathi v{settings.APP_VERSION} is ready!")
    logger.info(f"📊 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    if not db_connected:
        logger.info("⚠️  Database: DISCONNECTED (configure MongoDB Atlas to enable)")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down CyberSathi Backend...")
    if db_connected:
        await db.close_db()
    logger.info("✅ Cleanup completed")


async def create_default_admin():
    """Create default admin user from environment variables."""
    try:
        # Check if admin exists
        admin = await UserDocument.find_one(UserDocument.email == settings.ADMIN_EMAIL)
        
        if not admin:
            # Truncate password to 72 bytes for bcrypt compatibility
            admin_password = settings.ADMIN_PASSWORD[:72]
            
            # Create admin user
            admin = await AuthService.create_user(
                email=settings.ADMIN_EMAIL,
                password=admin_password,
                full_name="System Administrator",
                phone=settings.ADMIN_PHONE,
                role=UserRole.SUPER_ADMIN,
                department="IT & Security",
            )
            logger.info(f"✅ Default admin created: {settings.ADMIN_EMAIL}")
        else:
            logger.info(f"ℹ️  Admin user already exists: {settings.ADMIN_EMAIL}")
            
    except Exception as e:
        logger.warning(f"⚠️  Could not create default admin: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready WhatsApp chatbot for India's Cybercrime Helpline (1930)",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaints"])
app.include_router(tracking.router, prefix="/api/v1/tracking", tags=["Tracking"])
app.include_router(escalation.router, prefix="/api/v1/escalation", tags=["Escalation"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(whatsapp_webhook.router, prefix="", tags=["WhatsApp"])

# Import and include new routers
try:
    from app.api import uploads, chatbot_ai
    app.include_router(uploads.router, prefix="/api/v1/files", tags=["File Upload"])
    app.include_router(chatbot_ai.router, prefix="/api/v1/ai", tags=["AI Chatbot"])
except Exception as e:
    logger.warning(f"Could not load optional routers: {e}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    import json
    import os
    from datetime import datetime
    
    # #region agent log
    try:
        log_path = r'd:\cybersathi\.cursor\debug.log'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:148","message":"health check called","data":{},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
    except Exception as log_err:
        logger.error(f"Failed to write debug log: {log_err}")
    # #endregion
    
    # Check database connection status
    db_status = "disconnected"
    db_using_mock = False
    mongodb_url_info = "not_set"
    try:
        from app.database import db
        from app.config import settings
        import os
        
        mongodb_url = os.getenv("MONGODB_URL") or settings.MONGODB_URL
        mongodb_url_info = "set" if mongodb_url and mongodb_url != "mongodb://localhost:27017" else "default_localhost"
        
        if db.client:
            # Try to ping the database
            await db.client.admin.command('ping')
            db_status = "connected"
            db_using_mock = getattr(db, 'using_mock', False)
        else:
            db_status = "not_initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # #region agent log
    try:
        log_path = r'd:\cybersathi\.cursor\debug.log'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"main.py:149","message":"health check response","data":{"db_status":db_status,"db_using_mock":db_using_mock,"mongodb_url_info":mongodb_url_info},"timestamp":int(datetime.now().timestamp()*1000)}) + '\n')
    except Exception as log_err:
        logger.error(f"Failed to write debug log: {log_err}")
    # #endregion
    
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "using_mock": db_using_mock,
            "persistent": not db_using_mock,
            "mongodb_url_configured": mongodb_url_info
        }
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic info."""
    return {
        "message": "Welcome to CyberSathi API",
        "version": settings.APP_VERSION,
        "docs": f"http://{settings.HOST}:{settings.PORT}/docs" if settings.DEBUG else "Contact admin",
    }


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
