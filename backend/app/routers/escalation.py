# backend/app/routers/escalation.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.cyberportal_adapter import escalate_to_1930
from app.services.db_service import get_complaint_by_reference

router = APIRouter()

class EscalationRequest(BaseModel):
    reference_id: str
    reason: str
    contact_phone: str = None

@router.post("/to-1930")
def escalate(req: EscalationRequest):
    rec = get_complaint_by_reference(req.reference_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Reference ID not found")
    # build escalation payload
    payload = {
        "local_ref": rec.get("reference_id"),
        "portal_case_id": rec.get("portal_case_id"),
        "reason": req.reason,
        "contact_phone": req.contact_phone or rec.get("phone"),
        "details": rec.get("description"),
    }
    resp = escalate_to_1930(payload)
    return {"escalation_result": resp}
