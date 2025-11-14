# backend/app/routers/whatsapp.py
"""WhatsApp webhook router for PS-2 complaint intake."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Query, UploadFile, File, Form
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, EmailStr

from backend.app.models.complaint import (
    ComplaintDocument,
    ReporterInfo,
    IncidentDetails,
    FraudCategory,
    FinancialFraudType,
    SocialMediaPlatform,
    SocialMediaFraudType,
    Gender,
    ComplaintStatus,
    Attachment,
    EvidenceType
)

router = APIRouter(prefix="/api/v1/webhook", tags=["whatsapp"])


class WhatsAppWebhookPayload(BaseModel):
    """Payload from WhatsApp webhook."""
    intent_hint: Optional[str] = None
    name: Optional[str] = None
    guardian_name: Optional[str] = None
    dob: Optional[str] = None  # ISO date string
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    village: Optional[str] = None
    post_office: Optional[str] = None
    police_station: Optional[str] = None
    district: Optional[str] = None
    pin_code: Optional[str] = None
    scam_category: Optional[str] = None
    scam_subcategory: Optional[str] = None
    account_number: Optional[str] = None
    message_text: Optional[str] = None
    amount_lost: Optional[float] = None
    transaction_reference: Optional[str] = None


@router.get("/whatsapp")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge")
):
    """Verify WhatsApp webhook (Meta verification)."""
    VERIFY_TOKEN = "cybersathi_1930_verify_token"
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def handle_whatsapp_message(payload: WhatsAppWebhookPayload):
    """Handle incoming WhatsApp messages and create/update complaints."""
    
    # Validate required fields for new complaint
    if not all([
        payload.name,
        payload.guardian_name,
        payload.dob,
        payload.phone,
        payload.gender,
        payload.village,
        payload.post_office,
        payload.police_station,
        payload.district,
        payload.pin_code
    ]):
        raise HTTPException(
            status_code=400,
            detail="Missing required reporter information fields"
        )
    
    # Parse DOB
    try:
        dob = datetime.fromisoformat(payload.dob or "")
    except:
        raise HTTPException(status_code=400, detail="Invalid date of birth format")
    
    # Create reporter info (fields are validated as non-None above)
    reporter = ReporterInfo(
        name=str(payload.name),
        guardian_name=str(payload.guardian_name),
        date_of_birth=dob,
        phone=str(payload.phone),
        email=payload.email,
        gender=Gender(str(payload.gender).lower()),
        village=str(payload.village),
        post_office=str(payload.post_office),
        police_station=str(payload.police_station),
        district=str(payload.district),
        pin_code=str(payload.pin_code)
    )
    
    # Determine fraud category
    fraud_category = None
    financial_type = None
    social_platform = None
    social_fraud_type = None
    
    if payload.scam_category:
        if payload.scam_category.lower() == "financial_fraud":
            fraud_category = FraudCategory.FINANCIAL_FRAUD
            if payload.scam_subcategory:
                financial_type = FinancialFraudType(payload.scam_subcategory)
        elif payload.scam_category.lower() == "social_media_fraud":
            fraud_category = FraudCategory.SOCIAL_MEDIA_FRAUD
            if payload.scam_subcategory:
                parts = payload.scam_subcategory.split("_")
                if len(parts) >= 2:
                    social_platform = SocialMediaPlatform(parts[0])
                    social_fraud_type = SocialMediaFraudType("_".join(parts[1:]))
    
    # Create incident details
    incident = IncidentDetails(
        description=payload.message_text or "Complaint submitted via WhatsApp",
        amount_lost=payload.amount_lost,
        account_number=payload.account_number,
        transaction_reference=payload.transaction_reference
    )
    
    # Generate PS-2 acknowledgement number
    ps2_ack = ComplaintDocument.generate_ps2_acknowledgement()
    
    # Create complaint
    complaint = ComplaintDocument(
        ps2_acknowledgement=ps2_ack,
        reporter_info=reporter,
        fraud_category=fraud_category,
        financial_fraud_type=financial_type,
        social_media_platform=social_platform,
        social_media_fraud_type=social_fraud_type,
        incident_details=incident,
        status=ComplaintStatus.REGISTERED,
        source="whatsapp",
        wa_phone_number=payload.phone
    )
    
    await complaint.insert()
    
    return {
        "reference_number": ps2_ack,
        "status": "created",
        "message": f"Complaint registered successfully. Your reference number is {ps2_ack}"
    }


@router.get("/status/{identifier}")
async def check_complaint_status(identifier: str):
    """Check complaint status by acknowledgement number or phone."""
    
    # Try to find by acknowledgement number first
    complaint = await ComplaintDocument.find_one(
        ComplaintDocument.ps2_acknowledgement == identifier
    )
    
    # If not found, try by phone
    if not complaint:
        complaint = await ComplaintDocument.find_one(
            ComplaintDocument.reporter_info.phone == identifier
        )
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Return masked information for privacy
    return {
        "acknowledgement_number": complaint.ps2_acknowledgement or complaint.reference_id,
        "status": complaint.status,
        "created_at": complaint.created_at,
        "fraud_category": complaint.fraud_category,
        "reporter_district": complaint.reporter_info.district if complaint.reporter_info else None,
        "last_updated": complaint.updated_at
    }
