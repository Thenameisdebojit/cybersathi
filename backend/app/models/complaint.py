# backend/app/models/complaint.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

class Attachment(BaseModel):
    filename: str
    url: Optional[str] = None

class ComplaintCreate(BaseModel):
    name: Optional[str] = None
    phone: str
    language: Optional[str] = "en"
    incident_type: str
    description: Optional[str] = None
    date_of_incident: Optional[datetime] = None
    amount: Optional[float] = None
    platform: Optional[str] = None
    txn_id: Optional[str] = None
    attachments: Optional[List[Attachment]] = []

class Complaint(BaseModel):
    id: int
    reference_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    phone: str
    language: Optional[str] = "en"
    incident_type: str
    description: Optional[str] = None
    date_of_incident: Optional[datetime] = None
    amount: Optional[float] = None
    platform: Optional[str] = None
    txn_id: Optional[str] = None
    attachments: Optional[List[Attachment]] = []
    status: str = "registered"
    portal_case_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}
