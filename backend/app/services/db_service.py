# backend/app/services/db_service.py
"""Database service for MongoDB operations using Beanie."""
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.complaint import ComplaintDocument, ComplaintCreate, ComplaintStatus
from app.models.user import UserDocument
from app.models.analytics import AnalyticsEventDocument, EventType


async def create_complaint(payload: Dict[str, Any]) -> Optional[ComplaintDocument]:
    """Create a new complaint in MongoDB."""
    try:
        complaint = ComplaintDocument(**payload)
        await complaint.insert()
        return complaint
    except Exception as e:
        print(f"Error creating complaint: {e}")
        return None


async def get_complaint_by_reference(ref: str) -> Optional[ComplaintDocument]:
    """Get complaint by reference ID."""
    try:
        complaint = await ComplaintDocument.find_one(ComplaintDocument.reference_id == ref)
        return complaint
    except Exception as e:
        print(f"Error fetching complaint: {e}")
        return None


async def get_all_complaints(limit: int = 100, skip: int = 0) -> List[ComplaintDocument]:
    """Get all complaints with pagination."""
    try:
        complaints = await ComplaintDocument.find_all().sort("-created_at").skip(skip).limit(limit).to_list()
        return complaints
    except Exception as e:
        print(f"Error fetching complaints: {e}")
        return []


async def update_complaint_status(reference_id: str, status: ComplaintStatus, notes: Optional[str] = None, changed_by: Optional[str] = None) -> bool:
    """Update complaint status."""
    try:
        complaint = await get_complaint_by_reference(reference_id)
        if complaint:
            await complaint.update_status(status, changed_by=changed_by, notes=notes)
            return True
        return False
    except Exception as e:
        print(f"Error updating complaint status: {e}")
        return False


async def link_portal_case(reference_id: str, portal_case_id: str) -> bool:
    """Link complaint to NCRP portal case."""
    try:
        complaint = await get_complaint_by_reference(reference_id)
        if complaint:
            complaint.portal_case_id = portal_case_id
            complaint.ncrp_submitted_at = datetime.utcnow()
            complaint.updated_at = datetime.utcnow()
            await complaint.save()
            return True
        return False
    except Exception as e:
        print(f"Error linking portal case: {e}")
        return False


async def search_complaints(
    status: Optional[str] = None,
    incident_type: Optional[str] = None,
    phone: Optional[str] = None,
    limit: int = 100
) -> List[ComplaintDocument]:
    """Search complaints with filters."""
    try:
        query = {}
        if status:
            query["status"] = status
        if incident_type:
            query["incident_type"] = incident_type
        if phone:
            query["phone"] = phone
        
        complaints = await ComplaintDocument.find(query).sort("-created_at").limit(limit).to_list()
        return complaints
    except Exception as e:
        print(f"Error searching complaints: {e}")
        return []


async def get_user_by_email(email: str) -> Optional[UserDocument]:
    """Get user by email."""
    try:
        user = await UserDocument.find_one(UserDocument.email == email)
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None


async def track_analytics_event(
    event_type: EventType,
    user_id: Optional[str] = None,
    complaint_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Track an analytics event."""
    try:
        await AnalyticsEventDocument.track(
            event_type=event_type,
            user_id=user_id,
            complaint_id=complaint_id,
            metadata=metadata
        )
    except Exception as e:
        print(f"Error tracking analytics: {e}")
