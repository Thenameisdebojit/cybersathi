# backend/app/database.py
"""PostgreSQL database connection and initialization using SQLAlchemy."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import logging
import os

from app.config import settings
from app.models.base import Base

logger = logging.getLogger(__name__)


class Database:
    """PostgreSQL database connection manager."""
    
    engine = None
    async_session_maker = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize PostgreSQL connection."""
        try:
            # Get DATABASE_URL from environment
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise ValueError("DATABASE_URL environment variable not set")
            
            # Convert postgres:// to postgresql+asyncpg:// for async support
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            
            logger.info(f"Connecting to PostgreSQL database")
            
            cls.engine = create_async_engine(
                database_url,
                echo=settings.DEBUG,
                future=True,
            )
            
            cls.async_session_maker = async_sessionmaker(
                cls.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            
            # Create all tables
            async with cls.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("✅ PostgreSQL connection established successfully")
            logger.info("✅ Database tables created/verified")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close PostgreSQL connection."""
        if cls.engine:
            await cls.engine.dispose()
            logger.info("PostgreSQL connection closed")
    
    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """Get database session for dependency injection."""
        async with cls.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Singleton instance
db = Database()


# Dependency for FastAPI
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get async database session."""
    async for session in db.get_session():
        yield session
