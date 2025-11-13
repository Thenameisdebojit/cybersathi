# backend/app/models/complaint.py
"""Complaint models for MongoDB using Beanie ODM."""
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

from beanie import Document
from pydantic import BaseModel, Field, field_validator


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
    file_size: int
    url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class StatusHistory(BaseModel):
    """Status change tracking."""
    status: ComplaintStatus
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    changed_by: Optional[str] = None
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
    platform: Optional[str] = None
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
            v = '+91' + v
        return v


class ComplaintUpdate(BaseModel):
    """Schema for updating complaint."""
    status: Optional[ComplaintStatus] = None
    portal_case_id: Optional[str] = None
    assignee: Optional[str] = None
    notes: Optional[str] = None


class ComplaintDocument(Document):
    """MongoDB document model for complaints."""
    
    reference_id: str = Field(default_factory=lambda: f"CYB{uuid.uuid4().hex[:10].upper()}")
    
    name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    language: str = "en"
    
    incident_type: IncidentType
    description: str
    date_of_incident: Optional[datetime] = None
    amount: Optional[float] = None
    platform: Optional[str] = None
    txn_id: Optional[str] = None
    bank_account: Optional[str] = None
    suspect_info: Optional[str] = None
    location: Optional[Location] = None
    
    attachments: List[Attachment] = Field(default_factory=list)
    
    status: ComplaintStatus = Field(default=ComplaintStatus.REGISTERED)
    status_history: List[StatusHistory] = Field(default_factory=list)
    
    portal_case_id: Optional[str] = None
    ncrp_submitted_at: Optional[datetime] = None
    
    assignee: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    source: str = "whatsapp"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    class Settings:
        name = "complaints"
        indexes = [
            "reference_id",
            "phone",
            "status",
            "created_at",
            [("phone", 1), ("created_at", -1)],
            [("status", 1), ("created_at", -1)],
        ]
    
    async def update_status(self, new_status: ComplaintStatus, changed_by: Optional[str] = None, notes: Optional[str] = None):
        """Update complaint status and track history."""
        self.status = new_status
        self.status_history.append(
            StatusHistory(
                status=new_status,
                changed_by=changed_by,
                notes=notes
            )
        )
        self.updated_at = datetime.utcnow()
        await self.save()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "reference_id": self.reference_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "language": self.language,
            "incident_type": self.incident_type,
            "description": self.description,
            "date_of_incident": self.date_of_incident,
            "amount": self.amount,
            "platform": self.platform,
            "txn_id": self.txn_id,
            "status": self.status,
            "portal_case_id": self.portal_case_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "attachments": [att.dict() for att in self.attachments],
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
