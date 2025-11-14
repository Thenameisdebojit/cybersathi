"""Initialize database with default admin user"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import db
from app.services.auth import AuthService
from app.models.user import UserRole
from app.config import settings


async def main():
    """Initialize database and create default admin user"""
    print("Initializing database...")
    
    try:
        await db.connect_db()
        print("✅ Database connected successfully")
        
        try:
            admin_user = await AuthService.create_user(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                full_name="System Administrator",
                phone=settings.ADMIN_PHONE,
                role=UserRole.SUPER_ADMIN,
                department="Administration"
            )
            print(f"✅ Default admin user created: {admin_user.email}")
            print(f"   Email: {settings.ADMIN_EMAIL}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
        except Exception as e:
            if "duplicate" in str(e).lower() or "exists" in str(e).lower():
                print(f"ℹ️  Admin user already exists: {settings.ADMIN_EMAIL}")
            else:
                print(f"⚠️  Error creating admin user: {e}")
        
        await db.close_db()
        print("✅ Database initialization complete")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
