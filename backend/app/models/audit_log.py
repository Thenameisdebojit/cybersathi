# backend/app/models/audit_log.py
"""Audit log models for tracking system actions."""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Enum as SQLEnum, JSON, Text
from pydantic import Field

from app.models.base import Base


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


class AuditLog(Base):
    """SQLAlchemy model for audit logs."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Who
    user_id = Column(String, index=True)
    user_email = Column(String)
    user_role = Column(String)
    
    # What
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    resource_type = Column(String, nullable=False)  # complaint, user, campaign, etc.
    resource_id = Column(String, index=True)
    
    # When
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Where
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Details
    description = Column(Text)
    changes = Column(JSON)  # Before/after values
    metadata = Column(JSON)
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(Text)


# Keep old name for backwards compatibility
AuditLogDocument = AuditLog
