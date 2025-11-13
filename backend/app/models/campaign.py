# backend/app/models/campaign.py
"""Campaign models for awareness and notification campaigns."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel, Field


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


class CampaignDocument(Document):
    """MongoDB document model for campaigns."""
    
    # Basic Info
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType
    
    # Content
    messages: Dict[str, CampaignMessage]  # language code -> message
    
    # Targeting
    target: CampaignTarget
    
    # Scheduling
    status: CampaignStatus = Field(default=CampaignStatus.DRAFT)
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Statistics
    stats: CampaignStats = Field(default_factory=CampaignStats)
    
    # Metadata
    created_by: str  # User ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "campaigns"
        indexes = [
            "status",
            "created_at",
            "scheduled_at",
            [("status", 1), ("scheduled_at", 1)],
        ]


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
