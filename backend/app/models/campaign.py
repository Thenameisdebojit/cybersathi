# backend/app/models/campaign.py
"""Campaign models for awareness and notification campaigns."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from sqlalchemy import Column, String, DateTime, Integer, Enum as SQLEnum, JSON, Text
from pydantic import BaseModel, Field

from app.models.base import Base


class CampaignType(str, Enum):
    """Types of campaigns."""
    AWARENESS = "awareness"
    ALERT = "alert"
    SURVEY = "survey"
    ANNOUNCEMENT = "announcement"


class CampaignStatus(str, Enum):
    """Campaign status."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CampaignTarget(BaseModel):
    """Target audience for campaign."""
    all_users: bool = False
    language: Optional[str] = None  # en, od, hi
    districts: List[str] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)
    user_segments: List[str] = Field(default_factory=list)  # recent_reporters, active_users


class CampaignMessage(BaseModel):
    """Campaign message content."""
    text: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None  # image, video, document
    template_name: Optional[str] = None
    quick_replies: List[str] = Field(default_factory=list)


class CampaignStats(BaseModel):
    """Campaign delivery statistics."""
    total_targeted: int = 0
    sent: int = 0
    delivered: int = 0
    read: int = 0
    failed: int = 0
    replied: int = 0


class Campaign(Base):
    """SQLAlchemy model for campaigns."""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    title = Column(String, nullable=False)
    description = Column(Text)
    campaign_type = Column(SQLEnum(CampaignType), nullable=False)
    
    # Content (stored as JSONB)
    messages = Column(JSON, nullable=False)  # language code -> message dict
    
    # Targeting (stored as JSONB)
    target = Column(JSON, nullable=False)
    
    # Scheduling
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    scheduled_at = Column(DateTime, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Statistics (stored as JSONB)
    stats = Column(JSON, default=dict)
    
    # Metadata
    created_by = Column(String, nullable=False)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CampaignCreate(BaseModel):
    """Schema for creating a campaign."""
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType
    messages: Dict[str, CampaignMessage]
    target: CampaignTarget
    scheduled_at: Optional[datetime] = None


class CampaignResponse(BaseModel):
    """API response schema for campaign."""
    id: str
    title: str
    campaign_type: CampaignType
    status: CampaignStatus
    stats: CampaignStats
    scheduled_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


# Keep old name for backwards compatibility
CampaignDocument = Campaign
