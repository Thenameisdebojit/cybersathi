# backend/app/routers/tracking.py
from fastapi import APIRouter, HTTPException
from app.services.db_service import get_complaint_by_reference
from app.services.cyberportal_adapter import get_case_status

router = APIRouter()

@router.get("/{reference_id}")
def track_case(reference_id: str):
    """
    Track case by reference id:
    - fetch local record
    - fetch portal status if available
    """
    rec = get_complaint_by_reference(reference_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Reference ID not found")

    response = {
        "reference_id": rec.get("reference_id"),
        "status": rec.get("status"),
        "created_at": rec.get("created_at"),
        "updated_at": rec.get("updated_at"),
        "incident_type": rec.get("incident_type"),
    }

    portal_id = rec.get("portal_case_id")
    if portal_id:
        portal_status = get_case_status(portal_id)
        response["portal_status"] = portal_status

    return response
