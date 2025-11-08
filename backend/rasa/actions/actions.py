# backend/rasa/actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import sys
from pathlib import Path
import requests
import json

# Ensure backend package is importable when action server runs
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.services.db_service import create_complaint, get_complaint_by_reference
from app.services.cyberportal_adapter import submit_complaint

class ActionSubmitComplaint(Action):
    def name(self) -> Text:
        return "action_submit_complaint"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Build payload from slots and latest message
        slots = tracker.slots
        text = tracker.latest_message.get("text", "")
        payload = {
            "name": slots.get("victim_name") or None,
            "phone": slots.get("phone_number") or tracker.sender_id,
            "language": slots.get("language") or "en",
            "incident_type": slots.get("fraud_type") or "unknown",
            "description": text,
            "date_of_incident": slots.get("incident_date"),
            "amount": slots.get("amount"),
            "platform": slots.get("platform"),
            "txn_id": slots.get("transaction_id"),
            "attachments": []
        }

        # Persist locally
        try:
            local = create_complaint(payload)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't register your complaint at the moment. Please try again later.")
            return []

        # Submit to portal (mock/live)
        try:
            resp = submit_complaint(local)
            portal_id = resp.get("portal_case_id") or resp.get("portal_id") or None
            message = f"Your complaint is registered. Reference ID: {local.get('reference_id')}."
            if portal_id:
                message += f" Portal Case ID: {portal_id}."
        except Exception as e:
            message = f"Registered locally. Reference ID: {local.get('reference_id')}. (Submission to portal failed or delayed.)"

        dispatcher.utter_message(text=message)
        return []

class ActionCheckStatus(Action):
    def name(self) -> Text:
        return "action_check_status"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ref = tracker.get_slot("reference_id")
        if not ref:
            dispatcher.utter_message(text="Please provide your Reference ID.")
            return []
        rec = get_complaint_by_reference(ref)
        if not rec:
            dispatcher.utter_message(text=f"No complaint found with Reference ID {ref}.")
            return []
        status = rec.get("status", "registered")
        portal = rec.get("portal_case_id")
        msg = f"Reference {ref}: Status — {status}."
        if portal:
            msg += f" Portal ID: {portal}."
        dispatcher.utter_message(text=msg)
        return []
