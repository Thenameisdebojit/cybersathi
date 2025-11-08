# backend/app/services/cyberportal_adapter.py
"""
CyberPortal Adapter
-------------------
Handles integration between CyberSathi and the National Cybercrime Reporting Portal (https://cybercrime.gov.in).

Supports two modes:
1. MOCK MODE (default for local/testing): Logs and simulates responses.
2. LIVE MODE: Sends real HTTP requests to the Cybercrime Portal API
   (requires proper API credentials and approval).

Key Responsibilities:
- Register new complaint data to the portal
- Fetch or synchronize case status updates
- Handle authentication, rate limiting, and retry logic
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional
from app.config import Settings

settings = Settings()


# ============ CONFIG ============

CYBERPORTAL_BASE = settings.CYBERPORTAL_API_URL
CYBERPORTAL_KEY = settings.CYBERPORTAL_API_KEY
MOCK_MODE = settings.DEBUG or not CYBERPORTAL_KEY  # mock if no real API key


# ============ HELPERS ============

def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {CYBERPORTAL_KEY}" if CYBERPORTAL_KEY else "",
    }


def _log(msg: str):
    print(f"[CyberPortalAdapter] {msg}")


# ============ MAIN METHODS ============

def submit_complaint(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit complaint data to the cybercrime portal.
    Returns dict with portal_case_id or error.
    """
    if MOCK_MODE:
        _log("MOCK submit_complaint called.")
        mock_id = f"MOCK-{int(time.time())}"
        return {
            "status": "mocked",
            "portal_case_id": mock_id,
            "message": "Complaint successfully simulated in mock mode."
        }

    try:
        url = f"{CYBERPORTAL_BASE}/complaints"
        resp = requests.post(url, json=data, headers=_headers(), timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"status": "error", "code": resp.status_code, "details": resp.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_case_status(portal_case_id: str) -> Dict[str, Any]:
    """
    Fetch complaint/case status from portal.
    """
    if MOCK_MODE:
        _log(f"MOCK get_case_status({portal_case_id}) called.")
        # Simulate simple status progression
        return {
            "status": "mocked",
            "portal_case_id": portal_case_id,
            "case_status": "Under Review" if int(time.time()) % 2 == 0 else "Forwarded to State Police",
            "last_update": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    try:
        url = f"{CYBERPORTAL_BASE}/complaints/{portal_case_id}/status"
        resp = requests.get(url, headers=_headers(), timeout=8)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"status": "error", "code": resp.status_code, "details": resp.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def sync_complaint_status(local_ref_id: str, portal_case_id: str) -> Dict[str, Any]:
    """
    Synchronize case status between CyberSathi DB and Cybercrime Portal.
    This function can be called by a cron or Celery worker periodically.
    """
    status_data = get_case_status(portal_case_id)
    if "case_status" in status_data:
        # Update DB record (placeholder - real DB write to be added)
        _log(f"Synced status for {local_ref_id}: {status_data['case_status']}")
    return status_data


def escalate_to_1930(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Direct escalation to 1930 helpline backend endpoint (if available).
    """
    if MOCK_MODE:
        _log("MOCK escalate_to_1930 called.")
        return {
            "status": "mocked",
            "ticket_id": f"1930-{int(time.time())}",
            "message": "Escalation simulated successfully."
        }

    try:
        url = f"{CYBERPORTAL_BASE}/escalations/1930"
        resp = requests.post(url, json=data, headers=_headers(), timeout=8)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"status": "error", "code": resp.status_code, "details": resp.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
