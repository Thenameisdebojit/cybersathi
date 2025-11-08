# backend/app/services/nlp_service.py
"""
Lightweight NLP service adapter.
- Uses Rasa HTTP API if available (settings.RASA_URL)
- Falls back to naive rule-based parse when Rasa not available.
"""
import requests
from typing import Dict
from app.config import Settings

settings = Settings()

def parse_message(text: str, language: str = "en") -> Dict:
    """
    Returns:
      { "intent": str, "confidence": float, "entities": {...}, "suggested_incident_type": str|None }
    """
    # Try calling Rasa if configured
    try:
        url = f"{settings.RASA_URL}/model/parse"
        resp = requests.post(url, json={"text": text}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            intent = data.get("intent", {}).get("name")
            confidence = data.get("intent", {}).get("confidence", 0.0)
            entities = {e.get("entity"): e.get("value") for e in data.get("entities", [])}
            suggested = None
            if intent == "report_fraud":
                # try to map to a standard incident_type
                if "upi" in text.lower():
                    suggested = "upi_scam"
            return {"intent": intent, "confidence": confidence, "entities": entities, "suggested_incident_type": suggested}
    except Exception:
        # fallback to rule-based
        l = text.lower()
        if "upi" in l or "transaction" in l:
            return {"intent": "report_fraud", "confidence": 0.6, "entities": {}, "suggested_incident_type": "upi_scam"}
        if "status" in l or "track" in l:
            return {"intent": "track_case", "confidence": 0.7, "entities": {}, "suggested_incident_type": None}
        if "help" in l or "tip" in l:
            return {"intent": "awareness_tip", "confidence": 0.7, "entities": {}, "suggested_incident_type": None}
    return {"intent": "unknown", "confidence": 0.0, "entities": {}, "suggested_incident_type": None}
