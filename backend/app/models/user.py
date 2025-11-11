# backend/app/models/user.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CITIZEN = "citizen"
    OFFICER = "officer"
    ADMIN = "admin"


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    roles: List[UserRole] = [UserRole.CITIZEN]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class Officer(BaseModel):
    id: int
    user_id: int
    badge_number: str
    department: str
    rank: Optional[str] = None
    assigned_district: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    
    model_config = {"from_attributes": True}


class MessageLog(BaseModel):
    id: int
    complaint_id: Optional[int] = None
    user_id: Optional[int] = None
    phone_number: str
    message_type: str  # incoming, outgoing, template
    message_content: str
    platform: str = "whatsapp"
    status: str = "sent"  # sent, delivered, read, failed
    metadata: Optional[dict] = {}
    created_at: datetime
    
    model_config = {"from_attributes": True}
