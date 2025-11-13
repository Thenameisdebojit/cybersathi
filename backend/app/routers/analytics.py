# backend/app/routers/analytics.py
"""Analytics router for dashboard statistics and insights."""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime, timedelta

from app.models.user import UserDocument
from app.models.complaint import ComplaintDocument, ComplaintStatus, IncidentType
from app.models.analytics import AnalyticsSummary
from app.services.auth import get_current_admin_user

router = APIRouter()


@router.get("/dashboard", response_model=AnalyticsSummary)
async def get_dashboard_stats(
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Get dashboard summary statistics (Admin only).
    
    Returns:
    - Total complaints
    - Complaints registered today
    - Resolved complaints
    - Average resolution time
    - Language distribution
    - Incident type distribution
    - District-wise distribution
    """
    # Total complaints
    total_complaints = await ComplaintDocument.count()
    
    # Complaints today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    complaints_today = await ComplaintDocument.find(
        ComplaintDocument.created_at >= today_start
    ).count()
    
    # Resolved complaints
    resolved_complaints = await ComplaintDocument.find(
        ComplaintDocument.status == ComplaintStatus.RESOLVED
    ).count()
    
    # Language distribution
    language_dist = {}
    all_complaints = await ComplaintDocument.find_all().to_list()
    for complaint in all_complaints:
        lang = complaint.language or "en"
        language_dist[lang] = language_dist.get(lang, 0) + 1
    
    # Incident type distribution
    incident_dist = {}
    for complaint in all_complaints:
        incident = complaint.incident_type.value
        incident_dist[incident] = incident_dist.get(incident, 0) + 1
    
    # District distribution
    district_dist = {}
    for complaint in all_complaints:
        if complaint.location and complaint.location.district:
            district = complaint.location.district
            district_dist[district] = district_dist.get(district, 0) + 1
    
    # Average resolution time (simplified - calculate from status history)
    avg_resolution_time = 0.0
    resolved = await ComplaintDocument.find(
        ComplaintDocument.status == ComplaintStatus.RESOLVED
    ).to_list()
    
    if resolved:
        total_hours = 0
        for complaint in resolved:
            # Calculate time from created_at to last status change
            time_diff = (complaint.updated_at - complaint.created_at).total_seconds() / 3600
            total_hours += time_diff
        avg_resolution_time = total_hours / len(resolved)
    
    # Trend data (last 7 days)
    trend_data = []
    for i in range(7):
        day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = await ComplaintDocument.find(
            ComplaintDocument.created_at >= day_start,
            ComplaintDocument.created_at < day_end
        ).count()
        
        trend_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count
        })
    
    trend_data.reverse()  # Chronological order
    
    return AnalyticsSummary(
        total_complaints=total_complaints,
        complaints_today=complaints_today,
        resolved_complaints=resolved_complaints,
        avg_resolution_time=round(avg_resolution_time, 2),
        language_distribution=language_dist,
        incident_type_distribution=incident_dist,
        district_distribution=district_dist,
        trend_data=trend_data
    )


@router.get("/trends")
async def get_trends(
    days: int = Query(30, le=365),
    group_by: str = Query("day", regex="^(day|week|month)$"),
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Get complaint trends over time (Admin only).
    
    - **days**: Number of days to analyze (max 365)
    - **group_by**: Grouping interval (day, week, month)
    """
    # TODO: Implement aggregation pipeline for MongoDB
    # For now, return simple daily counts
    
    trend_data = []
    for i in range(days):
        day_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = await ComplaintDocument.find(
            ComplaintDocument.created_at >= day_start,
            ComplaintDocument.created_at < day_end
        ).count()
        
        trend_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count
        })
    
    trend_data.reverse()
    
    return {"trends": trend_data, "group_by": group_by}


@router.get("/districts")
async def get_district_stats(
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Get district-wise complaint statistics (Admin only).
    
    Returns complaint counts by district for heatmap visualization.
    """
    district_stats = {}
    
    complaints = await ComplaintDocument.find_all().to_list()
    
    for complaint in complaints:
        if complaint.location and complaint.location.district:
            district = complaint.location.district
            state = complaint.location.state or "Odisha"
            
            key = f"{district}, {state}"
            
            if key not in district_stats:
                district_stats[key] = {
                    "district": district,
                    "state": state,
                    "total_complaints": 0,
                    "total_amount": 0.0,
                    "incident_types": {}
                }
            
            district_stats[key]["total_complaints"] += 1
            
            if complaint.amount:
                district_stats[key]["total_amount"] += complaint.amount
            
            incident_type = complaint.incident_type.value
            district_stats[key]["incident_types"][incident_type] = \
                district_stats[key]["incident_types"].get(incident_type, 0) + 1
    
    return {"districts": list(district_stats.values())}


@router.get("/export")
async def export_complaints(
    format: str = Query("csv", regex="^(csv|pdf|json)$"),
    status_filter: Optional[ComplaintStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Export complaints data (Admin only).
    
    - **format**: Export format (csv, pdf, json)
    - **status_filter**: Filter by status
    - **start_date**: Start date for filtering
    - **end_date**: End date for filtering
    """
    # TODO: Implement actual export logic with pandas/reportlab
    
    query = {}
    if status_filter:
        query["status"] = status_filter
    if start_date:
        query["created_at"] = {"$gte": start_date}
    if end_date:
        query.setdefault("created_at", {})["$lte"] = end_date
    
    complaints = await ComplaintDocument.find(query).to_list()
    
    # For now, return JSON
    data = [c.to_dict() for c in complaints]
    
    return {
        "format": format,
        "count": len(data),
        "data": data if format == "json" else None,
        "message": f"Export ready: {len(data)} complaints" if format != "json" else None
    }


@router.get("/incident-types")
async def get_incident_type_stats(
    current_user: UserDocument = Depends(get_current_admin_user)
):
    """
    Get statistics by incident type (Admin only).
    
    Returns complaint counts and total amounts for each incident type.
    """
    incident_stats = {}
    
    complaints = await ComplaintDocument.find_all().to_list()
    
    for complaint in complaints:
        incident_type = complaint.incident_type.value
        
        if incident_type not in incident_stats:
            incident_stats[incident_type] = {
                "incident_type": incident_type,
                "count": 0,
                "total_amount": 0.0,
                "resolved": 0
            }
        
        incident_stats[incident_type]["count"] += 1
        
        if complaint.amount:
            incident_stats[incident_type]["total_amount"] += complaint.amount
        
        if complaint.status == ComplaintStatus.RESOLVED:
            incident_stats[incident_type]["resolved"] += 1
    
    return {"incident_types": list(incident_stats.values())}
