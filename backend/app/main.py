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
    try:
        # Try to connect to MongoDB Atlas
        await db.connect_db()
        logger.info("✅ MongoDB Atlas connected successfully")
        db_connected = True
        
        # Create default admin user if not exists
        await create_default_admin()
        
    except Exception as e:
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
            # bcrypt only supports passwords up to 72 bytes
            admin_password = settings.ADMIN_PASSWORD.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            
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
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
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
