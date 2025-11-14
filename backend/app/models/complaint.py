# backend/app/models/complaint.py
"""Complaint models for MongoDB using Beanie ODM (PS-2 compliant)."""
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

from beanie import Document
from pydantic import BaseModel, EmailStr, Field, field_validator


class Gender(str, Enum):
    """Gender options (PS-2)."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class IncidentType(str, Enum):
    """Types of cyber incidents (Legacy - kept for backward compatibility)."""
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


class FraudCategory(str, Enum):
    """Main fraud categories (PS-2)."""
    FINANCIAL_FRAUD = "financial_fraud"
    SOCIAL_MEDIA_FRAUD = "social_media_fraud"
    OTHER = "other"


class FinancialFraudType(str, Enum):
    """23 Financial fraud subtypes from PS-2."""
    INVESTMENT_TRADING_IPO = "investment_trading_ipo"
    CUSTOMER_CARE_FRAUD = "customer_care_fraud"
    UPI_FRAUD = "upi_fraud"
    APK_FRAUD = "apk_fraud"
    FAKE_FRANCHISEE_DEALERSHIP = "fake_franchisee_dealership"
    ONLINE_JOB_FRAUD = "online_job_fraud"
    DEBIT_CARD_FRAUD = "debit_card_fraud"
    CREDIT_CARD_FRAUD = "credit_card_fraud"
    ECOMMERCE_FRAUD = "ecommerce_fraud"
    LOAN_APP_FRAUD = "loan_app_fraud"
    SEXTORTION_FRAUD = "sextortion_fraud"
    OLX_FRAUD = "olx_fraud"
    LOTTERY_FRAUD = "lottery_fraud"
    HOTEL_BOOKING_FRAUD = "hotel_booking_fraud"
    GAMING_APP_FRAUD = "gaming_app_fraud"
    AEPS_FRAUD = "aeps_fraud"
    TOWER_INSTALLATION_FRAUD = "tower_installation_fraud"
    EWALLET_FRAUD = "ewallet_fraud"
    DIGITAL_ARREST_FRAUD = "digital_arrest_fraud"
    FAKE_WEBSITE_SCAM = "fake_website_scam"
    TICKET_BOOKING_FRAUD = "ticket_booking_fraud"
    INSURANCE_MATURITY_FRAUD = "insurance_maturity_fraud"
    OTHERS = "others"


class SocialMediaPlatform(str, Enum):
    """Social media platforms (PS-2)."""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    X_TWITTER = "x_twitter"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    GMAIL = "gmail"
    FRAUD_CALL = "fraud_call"
    OTHER = "other"


class SocialMediaFraudType(str, Enum):
    """Social media fraud types (PS-2)."""
    IMPERSONATION_ACCOUNT = "impersonation_account"
    FAKE_ACCOUNT = "fake_account"
    HACKED_ACCOUNT = "hacked_account"
    OBSCENE_CONTENT = "obscene_content"
    SPAM = "spam"


class EvidenceType(str, Enum):
    """Types of evidence/attachments (PS-2)."""
    IDENTITY_PROOF = "identity_proof"
    BANK_STATEMENT = "bank_statement"
    TRANSACTION_SCREENSHOT = "transaction_screenshot"
    REQUEST_LETTER = "request_letter"
    URL_PROOF = "url_proof"
    DEBIT_CARD_PHOTO = "debit_card_photo"
    CREDIT_CARD_PHOTO = "credit_card_photo"
    DISPUTED_SCREENSHOT = "disputed_screenshot"
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


class ReporterInfo(BaseModel):
    """Reporter/complainant information (PS-2 13 required fields)."""
    name: str
    guardian_name: str  # Father/Spouse/Guardian name
    date_of_birth: datetime
    phone: str  # E.164 format
    email: Optional[EmailStr] = None
    gender: Gender
    village: str
    post_office: str
    police_station: str
    district: str
    pin_code: str  # 6 digits
    
    @field_validator('pin_code')
    @classmethod
    def validate_pin_code(cls, v: str) -> str:
        """Validate PIN code is 6 digits."""
        if not v.isdigit() or len(v) != 6:
            raise ValueError("PIN code must be exactly 6 digits")
        return v


class IncidentDetails(BaseModel):
    """Structured incident information (PS-2)."""
    description: str = Field(..., min_length=10)
    incident_date: Optional[datetime] = None
    amount_lost: Optional[float] = Field(None, ge=0)
    account_number: Optional[str] = None
    transaction_reference: Optional[str] = None
    beneficiary_account: Optional[str] = None
    beneficiary_name: Optional[str] = None
    transaction_date: Optional[datetime] = None
    fraud_url: Optional[str] = None
    suspect_info: Optional[str] = None


class Attachment(BaseModel):
    """File attachment metadata (Enhanced for PS-2)."""
    filename: str
    file_type: str
    file_size: int
    url: str
    evidence_type: Optional[EvidenceType] = EvidenceType.OTHER
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
    """MongoDB document model for complaints (PS-2 Enhanced)."""
    
    # Legacy reference ID (kept for backward compatibility)
    reference_id: str = Field(default_factory=lambda: f"CYB{uuid.uuid4().hex[:10].upper()}")
    
    # PS-2 Acknowledgement Number (CS-YYYY-XXX format)
    ps2_acknowledgement: Optional[str] = None
    
    # PS-2 Reporter Information (13 required fields)
    reporter_info: Optional[ReporterInfo] = None
    
    # Legacy fields (kept for backward compatibility)
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    language: str = "en"
    
    # PS-2 Fraud Classification
    fraud_category: Optional[FraudCategory] = None
    financial_fraud_type: Optional[FinancialFraudType] = None
    social_media_platform: Optional[SocialMediaPlatform] = None
    social_media_fraud_type: Optional[SocialMediaFraudType] = None
    
    # PS-2 Incident Details
    incident_details: Optional[IncidentDetails] = None
    
    # Legacy incident fields (kept for backward compatibility)
    incident_type: Optional[IncidentType] = None
    description: Optional[str] = None
    date_of_incident: Optional[datetime] = None
    amount: Optional[float] = None
    platform: Optional[str] = None
    txn_id: Optional[str] = None
    bank_account: Optional[str] = None
    suspect_info: Optional[str] = None
    location: Optional[Location] = None
    
    # Attachments/Evidence
    attachments: List[Attachment] = Field(default_factory=list)
    
    # Status management
    status: ComplaintStatus = Field(default=ComplaintStatus.REGISTERED)
    status_history: List[StatusHistory] = Field(default_factory=list)
    
    # Portal integration
    portal_case_id: Optional[str] = None
    ncrp_submitted_at: Optional[datetime] = None
    
    # Assignment and follow-up
    assignee: Optional[str] = None
    follow_up_required: bool = False
    follow_up_due_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Source/Channel
    source: str = "whatsapp"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # WhatsApp specific
    wa_conversation_id: Optional[str] = None
    wa_phone_number: Optional[str] = None
    
    class Settings:
        name = "complaints"
        indexes = [
            "reference_id",
            "ps2_acknowledgement",
            "phone",
            "reporter_info.phone",
            "reporter_info.email",
            "status",
            "fraud_category",
            "source",
            "created_at",
            "assignee",
            [("phone", 1), ("created_at", -1)],
            [("status", 1), ("created_at", -1)],
            [("fraud_category", 1), ("created_at", -1)],
        ]
    
    @staticmethod
    def generate_ps2_acknowledgement() -> str:
        """Generate PS-2 format acknowledgement number: CS-YYYY-XXX."""
        from datetime import datetime
        import random
        year = datetime.utcnow().year
        sequence = random.randint(100, 999)
        return f"CS-{year}-{sequence}"
    
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
