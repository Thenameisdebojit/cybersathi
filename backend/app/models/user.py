# backend/app/models/user.py
"""User models for authentication and authorization."""
from datetime import datetime
from typing import Optional
from enum import Enum

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


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
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    full_name: str
    role: UserRole = UserRole.VIEWER
    department: Optional[str] = None
    provider: Optional[str] = "local"
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


class UserDocument(Document):
    """MongoDB document model for users."""
    
    email: EmailStr
    phone: Optional[str] = None
    hashed_password: Optional[str] = None
    
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    profile_picture: Optional[str] = None
    
    full_name: str
    department: Optional[str] = None
    
    role: UserRole = Field(default=UserRole.VIEWER)
    status: UserStatus = UserStatus.ACTIVE
    permissions: list[str] = Field(default_factory=list)
    
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    created_by: Optional[str] = None
    
    class Settings:
        name = "users"
        indexes = ["email", "phone", "role", "status"]
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.role == UserRole.SUPER_ADMIN:
            return True
        return permission in self.permissions
    
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
            "role": self.role,
            "status": self.status,
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
