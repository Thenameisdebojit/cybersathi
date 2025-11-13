# backend/app/models/analytics.py
"""Analytics models for tracking events and metrics."""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from sqlalchemy import Column, String, DateTime, Integer, Float, Enum as SQLEnum, JSON
from pydantic import BaseModel, Field

from app.models.base import Base


class EventType(str, Enum):
    """Types of analytics events."""
    COMPLAINT_REGISTERED = "complaint_registered"
    COMPLAINT_RESOLVED = "complaint_resolved"
    USER_INTERACTION = "user_interaction"
    WHATSAPP_MESSAGE = "whatsapp_message"
    CAMPAIGN_SENT = "campaign_sent"
    PAGE_VIEW = "page_view"
    API_CALL = "api_call"


class AnalyticsEvent(Base):
    """SQLAlchemy model for analytics events."""
    __tablename__ = "analytics_events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    event_type = Column(SQLEnum(EventType), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Context
    user_id = Column(String)
    complaint_id = Column(String)
    campaign_id = Column(String)
    
    # Dimensions
    language = Column(String)
    district = Column(String, index=True)
    state = Column(String)
    incident_type = Column(String, index=True)
    source = Column(String)  # whatsapp, web, api
    
    # Metrics
    value = Column(Float)  # For numerical metrics like amount
    duration = Column(Integer)  # Duration in seconds
    
    # Additional data (stored as JSONB)
    metadata = Column(JSON)


class AnalyticsSummary(BaseModel):
    """Summary analytics for dashboard."""
    total_complaints: int = 0
    complaints_today: int = 0
    resolved_complaints: int = 0
    avg_resolution_time: float = 0.0  # in hours
    language_distribution: Dict[str, int] = Field(default_factory=dict)
    incident_type_distribution: Dict[str, int] = Field(default_factory=dict)
    district_distribution: Dict[str, int] = Field(default_factory=dict)
    trend_data: list = Field(default_factory=list)  # Time series data


# Keep old name for backwards compatibility
AnalyticsEventDocument = AnalyticsEvent
