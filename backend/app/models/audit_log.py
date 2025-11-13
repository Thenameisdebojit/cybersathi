# backend/app/models/audit_log.py
"""Audit log models for tracking system actions."""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from beanie import Document, Indexed
from pydantic import Field


class AuditAction(str, Enum):
    """Types of auditable actions."""
    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    
    # Complaint actions
    COMPLAINT_CREATED = "complaint_created"
    COMPLAINT_VIEWED = "complaint_viewed"
    COMPLAINT_UPDATED = "complaint_updated"
    COMPLAINT_STATUS_CHANGED = "complaint_status_changed"
    COMPLAINT_ASSIGNED = "complaint_assigned"
    COMPLAINT_ESCALATED = "complaint_escalated"
    
    # System actions
    NCRP_SUBMISSION = "ncrp_submission"
    WHATSAPP_MESSAGE_SENT = "whatsapp_message_sent"
    WHATSAPP_MESSAGE_RECEIVED = "whatsapp_message_received"
    FILE_UPLOADED = "file_uploaded"
    CAMPAIGN_SENT = "campaign_sent"
    
    # Security events
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGED = "password_changed"
    UNAUTHORIZED_ACCESS = "unauthorized_access"


class AuditLogDocument(Document):
    """MongoDB document model for audit logs."""
    
    # Who
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    
    # What
    action: AuditAction
    resource_type: str  # complaint, user, campaign, etc.
    resource_id: Optional[str] = None
    
    # When
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Where
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Details
    description: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None  # Before/after values
    metadata: Optional[Dict[str, Any]] = None
    
    # Status
    success: bool = True
    error_message: Optional[str] = None
    
    class Settings:
        name = "audit_logs"
        indexes = [
            "user_id",
            "action",
            "timestamp",
            "resource_id",
            [("user_id", 1), ("timestamp", -1)],
            [("action", 1), ("timestamp", -1)],
        ]
    
    @classmethod
    async def log(
        cls,
        action: AuditAction,
        resource_type: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        resource_id: Optional[str] = None,
        description: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Create an audit log entry."""
        log_entry = cls(
            user_id=user_id,
            user_email=user_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            changes=changes,
            ip_address=ip_address,
            success=success,
            error_message=error_message,
        )
        await log_entry.insert()
        return log_entry
