# backend/app/routers/complaints.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.complaint import ComplaintCreate, Complaint
from app.services.db_service import create_complaint, get_all_complaints, get_complaint_by_reference
from app.services.nlp_service import parse_message
from app.services.cyberportal_adapter import submit_complaint

router = APIRouter()

@router.post("/", response_model=Complaint, status_code=status.HTTP_201_CREATED)
def register_complaint(payload: ComplaintCreate):
    """
    Register a new complaint. Steps:
    - optional lightweight NLP parsing of description
    - persist locally
    - submit to cyberportal (mock or live)
    - return stored record
    """
    # NLP suggestion
    if payload.description and (not payload.incident_type or payload.incident_type == ""):
        parsed = parse_message(payload.description, language=payload.language or "en")
        suggested = parsed.get("suggested_incident_type")
        if suggested:
            payload.incident_type = suggested

    record = create_complaint(payload.dict())
    if not record:
        raise HTTPException(status_code=500, detail="Failed to create complaint locally")

    # attempt to submit to CyberPortal (mock or live)
    portal_resp = submit_complaint(record)
    if portal_resp:
        # if portal returned id, update local record with portal_case_id via db_service
        if portal_resp.get("portal_case_id"):
            from app.services.db_service import link_portal_case
            try:
                link_portal_case(record.get("reference_id"), portal_resp.get("portal_case_id"))
                record = get_complaint_by_reference(record.get("reference_id"))
            except Exception:
                # non-fatal
                pass

    return record

@router.get("/list", response_model=List[Complaint])
def list_complaints(limit: int = 100):
    rows = get_all_complaints(limit=limit)
    return rows

@router.get("/{reference_id}", response_model=Complaint)
def get_complaint(reference_id: str):
    rec = get_complaint_by_reference(reference_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Reference ID not found")
    return rec
