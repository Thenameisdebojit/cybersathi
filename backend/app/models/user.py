# backend/app/models/user.py
"""User models for authentication and authorization."""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Enum as SQLEnum, JSON
from pydantic import BaseModel, EmailStr, Field

from app.models.base import Base


class UserRole(str, Enum):
    """User roles for RBAC."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    OFFICER = "officer"
    VIEWER = "viewer"
    API_USER = "api_user"


class UserStatus(str, Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    phone: Optional[str] = None  # Optional for OAuth
    password: Optional[str] = Field(None, min_length=8)  # Optional for OAuth
    full_name: str
    role: UserRole = UserRole.VIEWER
    department: Optional[str] = None
    provider: Optional[str] = "local"  # 'local', 'google'
    provider_id: Optional[str] = None
    profile_picture: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    department: Optional[str] = None


class User(Base):
    """SQLAlchemy model for users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)
    
    # OAuth Fields
    provider = Column(String)  # 'local', 'google'
    provider_id = Column(String)
    profile_picture = Column(String)
    
    # Profile
    full_name = Column(String, nullable=False)
    department = Column(String)
    
    # Authorization
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, index=True)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, index=True)
    permissions = Column(JSON, default=list)
    
    # Session
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    created_by = Column(String)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.role == UserRole.SUPER_ADMIN:
            return True
        return permission in (self.permissions or [])
    
    def is_admin(self) -> bool:
        """Check if user is admin or super admin."""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses (exclude sensitive data)."""
        return {
            "id": str(self.id),
            "email": self.email,
            "phone": self.phone,
            "full_name": self.full_name,
            "role": self.role.value if isinstance(self.role, UserRole) else self.role,
            "status": self.status.value if isinstance(self.status, UserStatus) else self.status,
            "department": self.department,
            "last_login": self.last_login,
            "created_at": self.created_at,
            "provider": self.provider,
            "profile_picture": self.profile_picture,
        }


class UserResponse(BaseModel):
    """API response schema for user."""
    id: str
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    role: UserRole
    status: UserStatus
    department: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    provider: Optional[str] = None
    profile_picture: Optional[str] = None
    
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Keep old names for backwards compatibility
UserDocument = User
