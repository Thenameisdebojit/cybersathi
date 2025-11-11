import logging
from typing import Dict, List
from app.config import settings

logger = logging.getLogger(__name__)


class ConversationState:
    def __init__(self):
        self.sessions = {}
    
    def get_state(self, user_id: str) -> Dict:
        return self.sessions.get(user_id, {"stage": "initial", "data": {}})
    
    def update_state(self, user_id: str, stage: str, data: Dict = None):
        if user_id not in self.sessions:
            self.sessions[user_id] = {"stage": stage, "data": data or {}}
        else:
            self.sessions[user_id]["stage"] = stage
            if data:
                self.sessions[user_id]["data"].update(data)
    
    def clear_state(self, user_id: str):
        if user_id in self.sessions:
            del self.sessions[user_id]


class NLPService:
    def __init__(self):
        self.conversation_state = ConversationState()
        self.language_keywords = {
            "english": ["hello", "hi", "help", "report", "complaint", "fraud", "scam", "track", "status"],
            "odia": ["ନମସ୍କାର", "ସାହାଯ୍ୟ", "ରିପୋର୍ଟ", "ଅଭିଯୋଗ"]
        }
    
    def detect_language(self, text: str) -> str:
        text_lower = text.lower()
        for lang, keywords in self.language_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return lang
        return "english"
    
    async def process_message(self, user_id: str, text: str) -> Dict:
        state = self.conversation_state.get_state(user_id)
        language = self.detect_language(text)
        
        text_lower = text.lower()
        
        if state["stage"] == "initial" or any(word in text_lower for word in ["hi", "hello", "start", "help"]):
            return self._get_welcome_message(user_id, language)
        
        elif any(word in text_lower for word in ["report", "complaint", "fraud", "scam"]):
            return self._start_complaint_flow(user_id, language)
        
        elif any(word in text_lower for word in ["track", "status", "check"]):
            return self._start_tracking_flow(user_id, language)
        
        elif any(word in text_lower for word in ["awareness", "tips", "safety", "help"]):
            return self._get_awareness_content(user_id, language)
        
        elif state["stage"] == "collecting_complaint":
            return await self._handle_complaint_collection(user_id, text, state, language)
        
        elif state["stage"] == "tracking":
            return await self._handle_tracking(user_id, text, language)
        
        else:
            return self._get_default_response(user_id, language)
    
    async def process_button_click(self, user_id: str, button_id: str) -> Dict:
        state = self.conversation_state.get_state(user_id)
        
        if button_id == "report_fraud":
            return self._start_complaint_flow(user_id, "english")
        elif button_id == "track_case":
            return self._start_tracking_flow(user_id, "english")
        elif button_id == "awareness":
            return self._get_awareness_content(user_id, "english")
        elif button_id == "helpline":
            return {
                "text": f"📞 For immediate assistance, call the National Cybercrime Helpline:\n\n{settings.HELPLINE_NUMBER}\n\nAvailable 24x7"
            }
        else:
            return self._get_default_response(user_id, "english")
    
    def _get_welcome_message(self, user_id: str, language: str) -> Dict:
        self.conversation_state.update_state(user_id, "initial")
        
        if language == "odia":
            text = "🛡️ ସାଇବରସାଥୀରେ ସ୍ୱାଗତ!\n\nମୁଁ ଆପଣଙ୍କୁ ସାଇବର ଅପରାଧ ରିପୋର୍ଟ କରିବାରେ ସାହାଯ୍ୟ କରିପାରିବି।"
        else:
            text = "🛡️ Welcome to CyberSathi!\n\nI'm your AI assistant for reporting cybercrimes and getting help with the National Cybercrime Helpline (1930).\n\nHow can I help you today?"
        
        buttons = [
            {"id": "report_fraud", "title": "Report Fraud"},
            {"id": "track_case", "title": "Track My Case"},
            {"id": "awareness", "title": "Safety Tips"}
        ]
        
        return {"text": text, "buttons": buttons}
    
    def _start_complaint_flow(self, user_id: str, language: str) -> Dict:
        self.conversation_state.update_state(user_id, "collecting_complaint", {"step": "type"})
        
        text = "I'll help you file a complaint. What type of fraud did you experience?"
        buttons = [
            {"id": "upi_fraud", "title": "UPI/Payment Fraud"},
            {"id": "social_media", "title": "Social Media Scam"},
            {"id": "phishing", "title": "Phishing/Email Scam"},
            {"id": "online_shopping", "title": "Online Shopping Fraud"},
            {"id": "job_fraud", "title": "Job/Investment Scam"},
            {"id": "other", "title": "Other"}
        ]
        
        return {"text": text, "buttons": buttons}
    
    def _start_tracking_flow(self, user_id: str, language: str) -> Dict:
        self.conversation_state.update_state(user_id, "tracking")
        
        text = "Please provide your complaint reference ID (e.g., NCRP-12345678) to check the status."
        
        return {"text": text}
    
    def _get_awareness_content(self, user_id: str, language: str) -> Dict:
        text = """🔒 Cyber Safety Tips:

1️⃣ Never share OTP, CVV, or card PIN with anyone
2️⃣ Verify URLs before entering sensitive information
3️⃣ Don't click on suspicious links or attachments
4️⃣ Enable 2-factor authentication on all accounts
5️⃣ Regularly update passwords
6️⃣ Be cautious of "too good to be true" offers
7️⃣ Report suspicious activities immediately

Stay safe online! 🛡️"""
        
        return {"text": text}
    
    async def _handle_complaint_collection(self, user_id: str, text: str, state: Dict, language: str) -> Dict:
        step = state["data"].get("step", "type")
        
        if step == "type":
            state["data"]["incident_type"] = text
            state["data"]["step"] = "description"
            self.conversation_state.update_state(user_id, "collecting_complaint", state["data"])
            return {"text": "Please describe what happened in detail:"}
        
        elif step == "description":
            state["data"]["description"] = text
            state["data"]["step"] = "amount"
            self.conversation_state.update_state(user_id, "collecting_complaint", state["data"])
            return {"text": "How much money was lost (if any)? Enter 0 if not applicable:"}
        
        elif step == "amount":
            try:
                amount = float(text.replace("₹", "").replace(",", "").strip())
                state["data"]["amount"] = amount
                state["data"]["step"] = "complete"
                self.conversation_state.update_state(user_id, "collecting_complaint", state["data"])
                
                import uuid
                reference_id = f"CS-{uuid.uuid4().hex[:8].upper()}"
                
                self.conversation_state.clear_state(user_id)
                
                return {
                    "text": f"✅ Your complaint has been registered!\n\nReference ID: {reference_id}\n\nYou can track your complaint status using this ID.\n\nOur team will review and forward it to the appropriate authorities.",
                    "buttons": [
                        {"id": "track_case", "title": "Track Status"},
                        {"id": "report_fraud", "title": "Report Another"}
                    ]
                }
            except:
                return {"text": "Please enter a valid number (e.g., 5000 or 0):"}
        
        return self._get_default_response(user_id, language)
    
    async def _handle_tracking(self, user_id: str, text: str, language: str) -> Dict:
        reference_id = text.strip().upper()
        
        if reference_id.startswith("CS-") or reference_id.startswith("NCRP-"):
            self.conversation_state.clear_state(user_id)
            return {
                "text": f"📋 Status for {reference_id}:\n\n✅ Status: Under Review\n📅 Last Updated: Today\n👮 Assigned to: Cyber Cell District Unit\n\nYour case is being reviewed by the authorities. You will be notified of any updates."
            }
        else:
            return {"text": "Please provide a valid reference ID (e.g., CS-12345678 or NCRP-12345678):"}
    
    def _get_default_response(self, user_id: str, language: str) -> Dict:
        return {
            "text": "I didn't quite understand that. You can:\n\n• Report a fraud\n• Track your case\n• Get safety tips\n• Call helpline 1930",
            "buttons": [
                {"id": "report_fraud", "title": "Report Fraud"},
                {"id": "track_case", "title": "Track Case"},
                {"id": "awareness", "title": "Safety Tips"}
            ]
        }


nlp_service = NLPService()


def parse_message(text: str, language: str = "en") -> Dict:
    """
    Legacy shim for backward compatibility with REST endpoints.
    Returns: { "intent": str, "confidence": float, "entities": {}, "suggested_incident_type": str|None }
    """
    text_lower = text.lower()
    
    if "upi" in text_lower or "payment" in text_lower or "transaction" in text_lower:
        return {
            "intent": "report_fraud",
            "confidence": 0.7,
            "entities": {},
            "suggested_incident_type": "upi_fraud"
        }
    elif "phishing" in text_lower or "email" in text_lower or "link" in text_lower:
        return {
            "intent": "report_fraud",
            "confidence": 0.7,
            "entities": {},
            "suggested_incident_type": "phishing"
        }
    elif "social media" in text_lower or "facebook" in text_lower or "instagram" in text_lower:
        return {
            "intent": "report_fraud",
            "confidence": 0.7,
            "entities": {},
            "suggested_incident_type": "social_media"
        }
    elif "shopping" in text_lower or "product" in text_lower or "delivery" in text_lower:
        return {
            "intent": "report_fraud",
            "confidence": 0.7,
            "entities": {},
            "suggested_incident_type": "online_shopping"
        }
    elif "job" in text_lower or "investment" in text_lower or "scheme" in text_lower:
        return {
            "intent": "report_fraud",
            "confidence": 0.7,
            "entities": {},
            "suggested_incident_type": "job_fraud"
        }
    elif "status" in text_lower or "track" in text_lower or "check" in text_lower:
        return {
            "intent": "track_case",
            "confidence": 0.75,
            "entities": {},
            "suggested_incident_type": None
        }
    elif "help" in text_lower or "tip" in text_lower or "safety" in text_lower:
        return {
            "intent": "awareness",
            "confidence": 0.75,
            "entities": {},
            "suggested_incident_type": None
        }
    
    return {
        "intent": "unknown",
        "confidence": 0.3,
        "entities": {},
        "suggested_incident_type": "other"
    }
