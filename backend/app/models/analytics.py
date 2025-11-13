# backend/app/models/analytics.py
"""Analytics models for tracking events and metrics."""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of analytics events."""
    COMPLAINT_REGISTERED = "complaint_registered"
    COMPLAINT_RESOLVED = "complaint_resolved"
    USER_INTERACTION = "user_interaction"
    WHATSAPP_MESSAGE = "whatsapp_message"
    CAMPAIGN_SENT = "campaign_sent"
    PAGE_VIEW = "page_view"
    API_CALL = "api_call"


class AnalyticsEventDocument(Document):
    """MongoDB document model for analytics events."""
    
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Context
    user_id: Optional[str] = None
    complaint_id: Optional[str] = None
    campaign_id: Optional[str] = None
    
    # Dimensions
    language: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    incident_type: Optional[str] = None
    source: Optional[str] = None  # whatsapp, web, api
    
    # Metrics
    value: Optional[float] = None  # For numerical metrics like amount
    duration: Optional[int] = None  # Duration in seconds
    
    # Additional data
    metadata: Optional[Dict[str, Any]] = None
    
    class Settings:
        name = "analytics_events"
        indexes = [
            "event_type",
            "timestamp",
            [("event_type", 1), ("timestamp", -1)],
            [("district", 1), ("timestamp", -1)],
            [("incident_type", 1), ("timestamp", -1)],
        ]
    
    @classmethod
    async def track(
        cls,
        event_type: EventType,
        user_id: Optional[str] = None,
        complaint_id: Optional[str] = None,
        language: Optional[str] = None,
        district: Optional[str] = None,
        incident_type: Optional[str] = None,
        value: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Track an analytics event."""
        event = cls(
            event_type=event_type,
            user_id=user_id,
            complaint_id=complaint_id,
            language=language,
            district=district,
            incident_type=incident_type,
            value=value,
            metadata=metadata,
        )
        await event.insert()
        return event


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
