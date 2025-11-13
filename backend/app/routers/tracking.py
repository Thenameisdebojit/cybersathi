# backend/app/routers/tracking.py
"""Complaint tracking router for MongoDB."""
from fastapi import APIRouter, HTTPException
from app.models.complaint import ComplaintDocument
from app.models.analytics import AnalyticsEventDocument, EventType
from app.services.cyberportal_adapter import get_case_status

router = APIRouter()

@router.get("/{reference_id}")
async def track_case(reference_id: str):
    """
    Track case by reference ID.
    
    - Fetches local complaint record
    - Fetches portal status if complaint is submitted to NCRP
    - Public endpoint - anyone with reference ID can track
    """
    complaint = await ComplaintDocument.find_one(
        ComplaintDocument.reference_id == reference_id
    )
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Reference ID not found")

    # Track analytics
    await AnalyticsEventDocument.track(
        event_type=EventType.USER_INTERACTION,
        complaint_id=str(complaint.id),
        metadata={"action": "track_complaint"}
    )

    response = {
        "reference_id": complaint.reference_id,
        "status": complaint.status.value,
        "created_at": complaint.created_at.isoformat() if complaint.created_at else None,
        "updated_at": complaint.updated_at.isoformat() if complaint.updated_at else None,
        "incident_type": complaint.incident_type.value,
        "description": complaint.description,
        "language": complaint.language,
    }

    # Fetch portal status if available
    if complaint.portal_case_id:
        try:
            portal_status = get_case_status(complaint.portal_case_id)
            response["portal_status"] = portal_status
        except Exception as e:
            response["portal_status"] = {"error": f"Unable to fetch portal status: {str(e)}"}

    return response
