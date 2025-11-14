# backend/app/models/account_unfreeze.py
"""Account unfreeze request models for PS-2 Option C."""
from datetime import datetime
from typing import Optional
from enum import Enum

from beanie import Document
from pydantic import BaseModel, EmailStr, Field

from .complaint import Gender


class UnfreezeStatus(str, Enum):
    """Account unfreeze request status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class UnfreezeRequestDocument(Document):
    """MongoDB document for account unfreeze requests (PS-2 Option C)."""
    
    # Reference number (CS-UNFREEZE-YYYY-XXX format)
    reference_number: str
    
    # Reporter Information (same 13 PS-2 fields as complaints)
    name: str
    guardian_name: str
    date_of_birth: datetime
    phone: str
    email: Optional[EmailStr] = None
    gender: Gender
    village: str
    post_office: str
    police_station: str
    district: str
    pin_code: str
    
    # Account Details
    account_number: str = Field(..., description="Bank account number to unfreeze")
    bank_name: Optional[str] = None
    ifsc_code: Optional[str] = None
    
    # Related complaint (if any)
    related_complaint_ref: Optional[str] = None
    
    # Status and assignment
    status: UnfreezeStatus = Field(default=UnfreezeStatus.PENDING)
    assignee: Optional[str] = None
    
    # Notes and follow-up
    notes: Optional[str] = None
    follow_up_required: bool = True
    follow_up_due_date: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    
    # Source
    source: str = "whatsapp"
    wa_conversation_id: Optional[str] = None
    
    class Settings:
        name = "account_unfreeze_requests"
        indexes = [
            "reference_number",
            "phone",
            "account_number",
            "status",
            "created_at",
            [("status", 1), ("created_at", -1)],
        ]
    
    @staticmethod
    def generate_reference_number() -> str:
        """Generate unfreeze request reference number."""
        import random
        year = datetime.utcnow().year
        sequence = random.randint(100, 999)
        return f"CS-UNFREEZE-{year}-{sequence}"


class QueryDocument(Document):
    """MongoDB document for other queries (PS-2 Option D)."""
    
    # Reference number
    reference_number: str
    
    # User Information
    name: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None
    
    # Query details
    query_text: str
    query_type: Optional[str] = None
    
    # Status
    status: str = Field(default="open")
    response: Optional[str] = None
    assignee: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    
    # Source
    source: str = "whatsapp"
    wa_conversation_id: Optional[str] = None
    
    class Settings:
        name = "queries"
        indexes = [
            "reference_number",
            "phone",
            "status",
            "created_at",
        ]
    
    @staticmethod
    def generate_reference_number() -> str:
        """Generate query reference number."""
        import random
        year = datetime.utcnow().year
        sequence = random.randint(100, 999)
        return f"CS-QUERY-{year}-{sequence}"
