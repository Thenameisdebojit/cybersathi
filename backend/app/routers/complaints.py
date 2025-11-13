# backend/app/routers/complaints.py
"""Complaint management router with MongoDB integration."""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime

from app.models.complaint import (
    ComplaintCreate, ComplaintUpdate, ComplaintResponse,
    ComplaintDocument, ComplaintStatus, IncidentType
)
from app.models.analytics import AnalyticsEventDocument, EventType
from app.models.audit_log import AuditLogDocument, AuditAction
from app.models.user import UserDocument
from app.services.auth import get_current_user, get_current_admin_user
from app.services.nlp_service import parse_message
from app.services.cyberportal_adapter import submit_complaint

router = APIRouter()


@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def register_complaint(
    payload: ComplaintCreate,
    current_user: Optional[UserDocument] = None
):
    """
    Register a new cybercrime complaint.
    
    - **phone**: Contact number (required)
    - **incident_type**: Type of cybercrime
    - **description**: Detailed description (min 10 chars)
    - **amount**: Financial loss amount (optional)
    - **date_of_incident**: When incident occurred (optional)
    - **attachments**: Supporting documents/images (optional)
    
    Returns complaint with unique reference ID.
    """
    try:
        # Create complaint document
        complaint = ComplaintDocument(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            language=payload.language,
            incident_type=payload.incident_type,
            description=payload.description,
            date_of_incident=payload.date_of_incident,
            amount=payload.amount,
            platform=payload.platform,
            txn_id=payload.txn_id,
            bank_account=payload.bank_account,
            suspect_info=payload.suspect_info,
            location=payload.location,
            attachments=payload.attachments,
            status=ComplaintStatus.REGISTERED,
            source="api",  # or "whatsapp" if from webhook
        )
        
        # Save to MongoDB
        await complaint.insert()
        
        # Track analytics event
        await AnalyticsEventDocument.track(
            event_type=EventType.COMPLAINT_REGISTERED,
            complaint_id=str(complaint.id),
            language=complaint.language,
            district=complaint.location.district if complaint.location else None,
            incident_type=complaint.incident_type.value,
            value=complaint.amount,
        )
        
        # Audit log
        await AuditLogDocument.log(
            action=AuditAction.COMPLAINT_CREATED,
            resource_type="complaint",
            user_id=str(current_user.id) if current_user else None,
            resource_id=str(complaint.id),
            description=f"Complaint registered: {complaint.reference_id}",
        )
        
        # TODO: Submit to NCRP in background task
        # submit_to_ncrp_task.delay(str(complaint.id))
        
        return ComplaintResponse(
            id=str(complaint.id),
            reference_id=complaint.reference_id,
            name=complaint.name,
            phone=complaint.phone,
            language=complaint.language,
            incident_type=complaint.incident_type,
            description=complaint.description,
            status=complaint.status,
            created_at=complaint.created_at,
            updated_at=complaint.updated_at,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register complaint: {str(e)}"
        )


@router.get("/list", response_model=List[ComplaintResponse])
async def list_complaints(
    limit: int = Query(100, le=1000),
    skip: int = Query(0, ge=0),
    status_filter: Optional[ComplaintStatus] = None,
    incident_type_filter: Optional[IncidentType] = None,
    language: Optional[str] = None,
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    List all complaints (Admin only).
    
    Supports filtering and pagination.
    - **limit**: Number of results (max 1000)
    - **skip**: Number of results to skip (pagination)
    - **status_filter**: Filter by complaint status
    - **incident_type_filter**: Filter by incident type
    - **language**: Filter by language (en, od, hi)
    """
    try:
        query = {}
        
        if status_filter:
            query["status"] = status_filter
        if incident_type_filter:
            query["incident_type"] = incident_type_filter
        if language:
            query["language"] = language
        
        complaints = await ComplaintDocument.find(query)\
            .sort("-created_at")\
            .skip(skip)\
            .limit(limit)\
            .to_list()
        
        return [
            ComplaintResponse(
                id=str(c.id),
                reference_id=c.reference_id,
                name=c.name,
                phone=c.phone,
                language=c.language,
                incident_type=c.incident_type,
                description=c.description,
                status=c.status,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in complaints
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch complaints: {str(e)}"
        )


@router.get("/{reference_id}")
async def get_complaint(reference_id: str):
    """
    Get single complaint by reference ID.
    
    Public endpoint - anyone with reference ID can track their complaint.
    """
    complaint = await ComplaintDocument.find_one(
        ComplaintDocument.reference_id == reference_id
    )
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Track view event
    await AnalyticsEventDocument.track(
        event_type=EventType.USER_INTERACTION,
        complaint_id=str(complaint.id),
        metadata={"action": "view_complaint"}
    )
    
    return complaint.to_dict()


@router.put("/{reference_id}", response_model=ComplaintResponse)
async def update_complaint(
    reference_id: str,
    updates: ComplaintUpdate,
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Update complaint details (Admin only).
    
    - **status**: Update complaint status
    - **portal_case_id**: Link NCRP case ID
    - **assignee**: Assign to user
    - **notes**: Add notes
    """
    complaint = await ComplaintDocument.find_one(
        ComplaintDocument.reference_id == reference_id
    )
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Track changes for audit
    changes = {}
    
    if updates.status and updates.status != complaint.status:
        changes["status"] = {"old": complaint.status.value, "new": updates.status.value}
        await complaint.update_status(
            new_status=updates.status,
            changed_by=str(current_user.id),
            notes=updates.notes
        )
    
    if updates.portal_case_id:
        changes["portal_case_id"] = {"old": complaint.portal_case_id, "new": updates.portal_case_id}
        complaint.portal_case_id = updates.portal_case_id
    
    if updates.assignee:
        changes["assignee"] = {"old": complaint.assignee, "new": updates.assignee}
        complaint.assignee = updates.assignee
    
    complaint.updated_at = datetime.utcnow()
    await complaint.save()
    
    # Audit log
    await AuditLogDocument.log(
        action=AuditAction.COMPLAINT_UPDATED,
        resource_type="complaint",
        user_id=str(current_user.id),
        user_email=current_user.email,
        resource_id=str(complaint.id),
        changes=changes,
        description=f"Complaint {reference_id} updated",
    )
    
    return ComplaintResponse(
        id=str(complaint.id),
        reference_id=complaint.reference_id,
        name=complaint.name,
        phone=complaint.phone,
        language=complaint.language,
        incident_type=complaint.incident_type,
        description=complaint.description,
        status=complaint.status,
        created_at=complaint.created_at,
        updated_at=complaint.updated_at,
    )


@router.delete("/{reference_id}")
async def delete_complaint(
    reference_id: str,
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Delete complaint (Super Admin only).
    
    Use with caution - this is permanent.
    """
    if current_user.role.value != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can delete complaints"
        )
    
    complaint = await ComplaintDocument.find_one(
        ComplaintDocument.reference_id == reference_id
    )
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Audit log before deletion
    await AuditLogDocument.log(
        action=AuditAction.COMPLAINT_UPDATED,  # Or create COMPLAINT_DELETED action
        resource_type="complaint",
        user_id=str(current_user.id),
        user_email=current_user.email,
        resource_id=str(complaint.id),
        description=f"Complaint {reference_id} deleted",
    )
    
    await complaint.delete()
    
    return {"message": f"Complaint {reference_id} deleted successfully"}
