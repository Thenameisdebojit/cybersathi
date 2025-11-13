# backend/app/models/complaint.py
"""Complaint models for PostgreSQL using SQLAlchemy ORM."""
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

from sqlalchemy import Column, String, DateTime, Integer, Float, Enum as SQLEnum, JSON, Text
from pydantic import BaseModel, Field, field_validator

from app.models.base import Base


class IncidentType(str, Enum):
    """Types of cyber incidents."""
    UPI_FRAUD = "upi_fraud"
    PHISHING = "phishing"
    IDENTITY_THEFT = "identity_theft"
    ONLINE_JOB_FRAUD = "online_job_fraud"
    LOTTERY_FRAUD = "lottery_fraud"
    DATING_APP_FRAUD = "dating_app_fraud"
    INVESTMENT_FRAUD = "investment_fraud"
    SOCIAL_MEDIA_HACK = "social_media_hack"
    RANSOMWARE = "ransomware"
    OTHER = "other"


class ComplaintStatus(str, Enum):
    """Complaint processing status."""
    DRAFT = "draft"
    REGISTERED = "registered"
    SUBMITTED_TO_NCRP = "submitted_to_ncrp"
    UNDER_INVESTIGATION = "under_investigation"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"


class Attachment(BaseModel):
    """File attachment metadata."""
    filename: str
    file_type: str
    file_size: int  # in bytes
    url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class StatusHistory(BaseModel):
    """Status change tracking."""
    status: ComplaintStatus
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    changed_by: Optional[str] = None  # user_id
    notes: Optional[str] = None


class Location(BaseModel):
    """Geographic location information."""
    district: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ComplaintCreate(BaseModel):
    """Schema for creating a new complaint."""
    name: Optional[str] = None
    phone: str = Field(..., description="Phone number with country code")
    email: Optional[str] = None
    language: str = Field(default="en", description="Language code: en, od (Odia), hi")
    incident_type: IncidentType
    description: str = Field(..., min_length=10, max_length=2000)
    date_of_incident: Optional[datetime] = None
    amount: Optional[float] = Field(None, ge=0)
    platform: Optional[str] = None  # UPI app, website, social media platform
    txn_id: Optional[str] = None
    bank_account: Optional[str] = None
    suspect_info: Optional[str] = None
    location: Optional[Location] = None
    attachments: List[Attachment] = Field(default_factory=list)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format."""
        if not v.startswith('+'):
            v = '+91' + v  # Default to India
        return v


class ComplaintUpdate(BaseModel):
    """Schema for updating complaint."""
    status: Optional[ComplaintStatus] = None
    portal_case_id: Optional[str] = None
    assignee: Optional[str] = None
    notes: Optional[str] = None


class Complaint(Base):
    """SQLAlchemy model for complaints."""
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String, unique=True, index=True, default=lambda: f"CYB{uuid.uuid4().hex[:10].upper()}")
    
    # Complainant Info (encrypted in production)
    name = Column(String)
    phone = Column(String, nullable=False, index=True)
    email = Column(String)
    language = Column(String, default="en")
    
    # Incident Details
    incident_type = Column(SQLEnum(IncidentType), nullable=False)
    description = Column(Text, nullable=False)
    date_of_incident = Column(DateTime)
    amount = Column(Float)
    platform = Column(String)
    txn_id = Column(String)
    bank_account = Column(String)
    suspect_info = Column(Text)
    location = Column(JSON)  # Stored as JSONB
    
    # Attachments (stored as JSONB array)
    attachments = Column(JSON, default=list)
    
    # Status Tracking
    status = Column(SQLEnum(ComplaintStatus), default=ComplaintStatus.REGISTERED, index=True)
    status_history = Column(JSON, default=list)  # Stored as JSONB array
    
    # Integration
    portal_case_id = Column(String)  # NCRP case ID
    ncrp_submitted_at = Column(DateTime)
    
    # Assignment
    assignee = Column(String)  # User ID of assigned admin
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    source = Column(String, default="whatsapp")  # whatsapp, web, api
    ip_address = Column(String)
    user_agent = Column(String)
    
    def update_status_sync(self, new_status: ComplaintStatus, changed_by: Optional[str] = None, notes: Optional[str] = None):
        """Update complaint status and track history (sync method for use within session)."""
        self.status = new_status
        history = self.status_history or []
        history.append({
            "status": new_status.value,
            "changed_at": datetime.utcnow().isoformat(),
            "changed_by": changed_by,
            "notes": notes
        })
        self.status_history = history
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "reference_id": self.reference_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "language": self.language,
            "incident_type": self.incident_type.value if isinstance(self.incident_type, IncidentType) else self.incident_type,
            "description": self.description,
            "date_of_incident": self.date_of_incident,
            "amount": self.amount,
            "platform": self.platform,
            "txn_id": self.txn_id,
            "status": self.status.value if isinstance(self.status, ComplaintStatus) else self.status,
            "portal_case_id": self.portal_case_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "attachments": self.attachments or [],
        }


class ComplaintResponse(BaseModel):
    """API response schema for complaint."""
    id: str
    reference_id: str
    name: Optional[str] = None
    phone: str
    language: str
    incident_type: IncidentType
    description: str
    status: ComplaintStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


# Keep old name for backwards compatibility
ComplaintDocument = Complaint
