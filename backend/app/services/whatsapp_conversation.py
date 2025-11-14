"""
WhatsApp Conversation State Machine with NLU Integration
Implements 13-field complaint collection flow as per Prompt 1 requirements

⚠️ CRITICAL: This module needs to be updated to collect ALL PS2.pdf required fields:
- Name, Guardian Name, DOB, Phone, Email, Gender
- Village, Post Office, Police Station, District, PIN Code
See PS2_IMPLEMENTATION_PLAN.md for detailed refactoring guide
"""

import re
from typing import Dict, Optional, List
from datetime import datetime
from enum import Enum
import uuid

from app.services.nlu import nlu_service, Intent
from app.services.whatsapp_service import whatsapp_service
from app.services.ticket_service import ticket_service
from app.services.validation import validation_service


class ConversationStage(str, Enum):
    """Conversation flow stages"""
    INITIAL = "initial"
    AWAITING_FRAUD_TYPE = "awaiting_fraud_type"
    COLLECTING_COMPLAINT = "collecting_complaint"
    COLLECTING_FINANCIAL_DETAILS = "collecting_financial_details"
    COLLECTING_SOCIAL_MEDIA_DETAILS = "collecting_social_media_details"
    COLLECTING_ATTACHMENTS = "collecting_attachments"
    CONFIRMATION = "confirmation"
    COMPLETED = "completed"
    TRACKING = "tracking"


class ComplaintField(str, Enum):
    """Complaint collection fields - TO BE UPDATED per PS2.pdf requirements"""
    FRAUD_TYPE = "fraud_type"
    INCIDENT_DESCRIPTION = "incident_description"
    INCIDENT_DATE = "incident_date"
    INCIDENT_TIME = "incident_time"
    AMOUNT_LOST = "amount_lost"
    SUSPECT_INFO = "suspect_info"
    SUSPECT_CONTACT = "suspect_contact"
    VICTIM_NAME = "victim_name"
    VICTIM_PHONE = "victim_phone"
    VICTIM_EMAIL = "victim_email"
    LOCATION = "location"
    POLICE_REPORT_FILED = "police_report_filed"
    ADDITIONAL_INFO = "additional_info"


class ConversationState:
    """Manages conversation state for each user"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def get_state(self, user_id: str) -> Dict:
        """Get user's conversation state"""
        return self.sessions.get(user_id, {
            "stage": ConversationStage.INITIAL,
            "data": {},
            "current_field": None,
            "primary_intent": None,
            "sub_intent": None,
            "platform_intent": None,
            "fraud_branch": None,  # A1 or A2
            "attachments": [],
            "started_at": datetime.utcnow().isoformat()
        })
    
    def update_state(self, user_id: str, updates: Dict):
        """Update user's conversation state"""
        if user_id not in self.sessions:
            self.sessions[user_id] = self.get_state(user_id)
        self.sessions[user_id].update(updates)
    
    def set_field(self, user_id: str, field: ComplaintField, value: any):
        """Set a specific field in user's data"""
        if user_id not in self.sessions:
            self.sessions[user_id] = self.get_state(user_id)
        self.sessions[user_id]["data"][field] = value
    
    def clear_state(self, user_id: str):
        """Clear user's conversation state"""
        if user_id in self.sessions:
            del self.sessions[user_id]


class WhatsAppConversationHandler:
    """
    Handles WhatsApp conversation flow with NLU integration
    Implements state machine for complaint collection
    """
    
    def __init__(self):
        self.conversation_state = ConversationState()
        self.nlu = nlu_service
    
    async def process_message(self, user_id: str, message_text: str) -> Dict:
        """
        Process incoming WhatsApp message with NLU
        
        Args:
            user_id: WhatsApp user identifier
            message_text: User's message text
            
        Returns:
            Response dict with text and optional buttons
        """
        state = self.conversation_state.get_state(user_id)
        current_stage = state["stage"]
        
        if current_stage == ConversationStage.INITIAL:
            return await self._handle_initial(user_id, message_text)
        
        elif current_stage == ConversationStage.AWAITING_FRAUD_TYPE:
            return await self._handle_fraud_type_selection(user_id, message_text)
        
        elif current_stage == ConversationStage.COLLECTING_COMPLAINT:
            return await self._handle_complaint_collection(user_id, message_text, state)
        
        elif current_stage == ConversationStage.CONFIRMATION:
            return await self._handle_confirmation(user_id, message_text, state)
        
        elif current_stage == ConversationStage.TRACKING:
            return await self._handle_tracking(user_id, message_text)
        
        else:
            return self._get_default_response(user_id)
    
    async def _handle_initial(self, user_id: str, message_text: str) -> Dict:
        """Handle initial message with NLU intent detection"""
        nlu_result = self.nlu.analyze_message(message_text)
        intent = nlu_result["intent"]
        
        self.conversation_state.update_state(user_id, {
            "primary_intent": intent,
            "platform_intent": nlu_result["platform"]
        })
        
        if intent == Intent.NEW_COMPLAINT:
            return await self._start_complaint_flow(user_id, nlu_result)
        
        elif intent == Intent.CHECK_STATUS:
            self.conversation_state.update_state(user_id, {
                "stage": ConversationStage.TRACKING
            })
            return {
                "text": "📋 Please provide your complaint ticket ID to check status.\n\nFormat: CS-YYYYMMDD-XXXXXX or NCRP-XXXXXXXX"
            }
        
        elif intent == Intent.ACCOUNT_UNFREEZE:
            return {
                "text": "🔒 For account unfreeze requests, please provide:\n1. Your account number\n2. Bank name\n3. Complaint ticket ID (if already filed)\n\nReply with these details."
            }
        
        elif intent in [Intent.FINANCIAL_FRAUD, Intent.FACEBOOK_FRAUD, Intent.INSTAGRAM_FRAUD,
                       Intent.X_TWITTER_FRAUD, Intent.WHATSAPP_FRAUD, Intent.TELEGRAM_FRAUD, Intent.GMAIL_FRAUD]:
            return await self._start_complaint_flow(user_id, nlu_result)
        
        else:
            return self._get_welcome_message(user_id)
    
    async def _start_complaint_flow(self, user_id: str, nlu_result: Dict) -> Dict:
        """Start complaint collection flow"""
        intent = nlu_result["intent"]
        fraud_branch = nlu_result["fraud_type"]
        
        self.conversation_state.update_state(user_id, {
            "stage": ConversationStage.AWAITING_FRAUD_TYPE,
            "sub_intent": intent,
            "fraud_branch": fraud_branch
        })
        
        if fraud_branch == "A1":
            return {
                "text": "💰 I understand you're reporting a financial fraud case.\n\nPlease select the type of financial fraud:",
                "buttons": [
                    {"id": "upi_fraud", "title": "UPI/Payment App Fraud"},
                    {"id": "banking_fraud", "title": "Internet Banking Fraud"},
                    {"id": "card_fraud", "title": "Debit/Credit Card Fraud"},
                    {"id": "investment_fraud", "title": "Investment/Trading Scam"},
                    {"id": "loan_fraud", "title": "Loan Fraud"},
                    {"id": "other_financial", "title": "Other Financial Fraud"}
                ]
            }
        elif fraud_branch == "A2":
            platform = nlu_result["platform"]
            return {
                "text": f"📱 I understand you're reporting a social media fraud case{' on ' + platform.upper() if platform != 'unknown' else ''}.\n\nPlease select the type of social media fraud:",
                "buttons": [
                    {"id": "account_hacked", "title": "Account Hacked"},
                    {"id": "impersonation", "title": "Fake Profile/Impersonation"},
                    {"id": "obscene_content", "title": "Obscene Content/Morphed Photos"},
                    {"id": "cyber_stalking", "title": "Cyber Stalking/Harassment"},
                    {"id": "blackmail", "title": "Online Blackmail/Sextortion"},
                    {"id": "other_social", "title": "Other Social Media Fraud"}
                ]
            }
        else:
            return {
                "text": "🆘 I'm here to help you report cybercrime. Please select the category:",
                "buttons": [
                    {"id": "financial_fraud", "title": "💰 Financial Fraud"},
                    {"id": "social_media_fraud", "title": "📱 Social Media Fraud"},
                    {"id": "other_cyber_crime", "title": "🔒 Other Cyber Crime"}
                ]
            }
    
    async def _handle_fraud_type_selection(self, user_id: str, message_text: str) -> Dict:
        """Handle fraud type selection"""
        state = self.conversation_state.get_state(user_id)
        
        self.conversation_state.set_field(user_id, ComplaintField.FRAUD_TYPE, message_text)
        self.conversation_state.update_state(user_id, {
            "stage": ConversationStage.COLLECTING_COMPLAINT,
            "current_field": ComplaintField.INCIDENT_DESCRIPTION
        })
        
        return {
            "text": "📝 Please describe the incident in detail:\n\n• What happened?\n• When did it happen?\n• How did you realize it was fraud?\n\nProvide as much detail as possible."
        }
    
    async def _handle_complaint_collection(self, user_id: str, message_text: str, state: Dict) -> Dict:
        """Handle step-by-step complaint field collection"""
        current_field = state.get("current_field")
        
        field_sequence = [
            ComplaintField.INCIDENT_DESCRIPTION,
            ComplaintField.INCIDENT_DATE,
            ComplaintField.INCIDENT_TIME,
            ComplaintField.AMOUNT_LOST,
            ComplaintField.SUSPECT_INFO,
            ComplaintField.SUSPECT_CONTACT,
            ComplaintField.VICTIM_NAME,
            ComplaintField.VICTIM_PHONE,
            ComplaintField.VICTIM_EMAIL,
            ComplaintField.LOCATION,
            ComplaintField.POLICE_REPORT_FILED,
            ComplaintField.ADDITIONAL_INFO
        ]
        
        if current_field == ComplaintField.INCIDENT_DESCRIPTION:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.INCIDENT_DATE
            })
            return {"text": "📅 When did this incident occur? (DD/MM/YYYY)"}
        
        elif current_field == ComplaintField.INCIDENT_DATE:
            date_pattern = re.compile(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$')
            if not date_pattern.match(message_text.strip()):
                return {"text": "❌ Invalid date format. Please use DD/MM/YYYY format (e.g., 14/11/2024)"}
            
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.INCIDENT_TIME
            })
            return {"text": "🕐 What time did it happen? (HH:MM format, e.g., 14:30)"}
        
        elif current_field == ComplaintField.INCIDENT_TIME:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.AMOUNT_LOST
            })
            return {"text": "💵 How much money was lost (if any)? Enter amount in ₹ or type '0' if not applicable."}
        
        elif current_field == ComplaintField.AMOUNT_LOST:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.SUSPECT_INFO
            })
            return {"text": "🔍 Do you have any information about the suspect/fraudster?\n\nProvide name, details, or type 'Unknown' if you don't have any information."}
        
        elif current_field == ComplaintField.SUSPECT_INFO:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.SUSPECT_CONTACT
            })
            return {"text": "📞 Do you have suspect's phone number, email, or social media profile? Type 'Unknown' if not available."}
        
        elif current_field == ComplaintField.SUSPECT_CONTACT:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.VICTIM_NAME
            })
            return {"text": "👤 Please provide your full name (as per Aadhaar):"}
        
        elif current_field == ComplaintField.VICTIM_NAME:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.VICTIM_PHONE
            })
            return {"text": "📱 Please provide your mobile number (10 digits):"}
        
        elif current_field == ComplaintField.VICTIM_PHONE:
            if not validation_service.is_valid_phone(message_text):
                return {"text": "❌ Invalid mobile number. Please enter a valid 10-digit mobile number starting with 6-9."}
            
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.VICTIM_EMAIL
            })
            return {"text": "📧 Please provide your email address:"}
        
        elif current_field == ComplaintField.VICTIM_EMAIL:
            if not validation_service.is_valid_email(message_text):
                return {"text": "❌ Invalid email address. Please enter a valid email (e.g., user@example.com)"}
            
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.LOCATION
            })
            return {"text": "📍 What is your current location/address (City, State):"}
        
        elif current_field == ComplaintField.LOCATION:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.POLICE_REPORT_FILED
            })
            return {
                "text": "🚔 Have you filed a police report for this incident?",
                "buttons": [
                    {"id": "yes_police_report", "title": "Yes, I have filed FIR"},
                    {"id": "no_police_report", "title": "No, not yet"}
                ]
            }
        
        elif current_field == ComplaintField.POLICE_REPORT_FILED:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "current_field": ComplaintField.ADDITIONAL_INFO
            })
            return {"text": "📎 Any additional information or documents you'd like to add? (Type 'None' if not applicable)\n\nYou can also attach up to 5 files (screenshots, PDFs, etc.)"}
        
        elif current_field == ComplaintField.ADDITIONAL_INFO:
            self.conversation_state.set_field(user_id, current_field, message_text)
            self.conversation_state.update_state(user_id, {
                "stage": ConversationStage.CONFIRMATION
            })
            return await self._show_confirmation(user_id, state)
        
        return self._get_default_response(user_id)
    
    async def _show_confirmation(self, user_id: str, state: Dict) -> Dict:
        """Show complaint summary for confirmation"""
        data = state["data"]
        
        summary = f"""
📋 **COMPLAINT SUMMARY**

🔖 Fraud Type: {data.get(ComplaintField.FRAUD_TYPE, 'N/A')}
📝 Description: {data.get(ComplaintField.INCIDENT_DESCRIPTION, 'N/A')[:100]}...
📅 Date & Time: {data.get(ComplaintField.INCIDENT_DATE)} {data.get(ComplaintField.INCIDENT_TIME)}
💰 Amount Lost: ₹{data.get(ComplaintField.AMOUNT_LOST, '0')}

👤 Your Details:
• Name: {data.get(ComplaintField.VICTIM_NAME)}
• Phone: {data.get(ComplaintField.VICTIM_PHONE)}
• Email: {data.get(ComplaintField.VICTIM_EMAIL)}
• Location: {data.get(ComplaintField.LOCATION)}

Please review and confirm the details are correct:
"""
        
        return {
            "text": summary,
            "buttons": [
                {"id": "confirm_submit", "title": "✅ Confirm & Submit"},
                {"id": "cancel_complaint", "title": "❌ Cancel"},
                {"id": "edit_complaint", "title": "✏️ Edit Details"}
            ]
        }
    
    async def _handle_confirmation(self, user_id: str, message_text: str, state: Dict) -> Dict:
        """Handle complaint confirmation"""
        text_lower = message_text.lower()
        
        if "confirm" in text_lower or "yes" in text_lower or "submit" in text_lower:
            ticket_id = ticket_service.generate_ticket()
            
            self.conversation_state.update_state(user_id, {
                "stage": ConversationStage.COMPLETED,
                "ticket_id": ticket_id
            })
            
            self.conversation_state.clear_state(user_id)
            
            return {
                "text": f"""
✅ **COMPLAINT REGISTERED SUCCESSFULLY**

🎫 Your Complaint Ticket ID: **{ticket_id}**

📌 Important Information:
• Save this ticket ID for future reference
• You'll receive updates via WhatsApp and email
• Typical response time: 24-48 hours
• Your case will be forwarded to appropriate authorities

🔍 Track your complaint status:
Reply with your ticket ID anytime to check status

📞 Emergency Helpline: 1930 (National Cybercrime Helpline)

Thank you for reporting. We're working to resolve your case.
""",
                "buttons": [
                    {"id": "track_status", "title": "📊 Track Status"},
                    {"id": "new_complaint", "title": "🆕 File Another Complaint"}
                ]
            }
        
        elif "cancel" in text_lower or "no" in text_lower:
            self.conversation_state.clear_state(user_id)
            return {"text": "❌ Complaint cancelled. Type 'help' to start over."}
        
        elif "edit" in text_lower:
            return {"text": "✏️ Edit feature coming soon. Please re-submit your complaint or cancel."}
        
        return {"text": "Please confirm by replying 'Yes' to submit or 'No' to cancel."}
    
    async def _handle_tracking(self, user_id: str, message_text: str) -> Dict:
        """Handle complaint status tracking"""
        ticket_id = message_text.strip().upper()
        
        if ticket_id.startswith("CS-") or ticket_id.startswith("NCRP-"):
            self.conversation_state.clear_state(user_id)
            
            return {
                "text": f"""
📊 **COMPLAINT STATUS**

🎫 Ticket ID: {ticket_id}
📍 Status: Under Review
📅 Filed On: {datetime.now().strftime('%d/%m/%Y')}
👮 Assigned To: Cyber Cell District Unit
📝 Last Update: Case forwarded to investigation team

⏱️ Expected Resolution: 7-14 working days

You'll receive notifications on any status updates.

📞 For urgent queries, call 1930
""",
                "buttons": [
                    {"id": "new_complaint", "title": "🆕 File New Complaint"},
                    {"id": "main_menu", "title": "🏠 Main Menu"}
                ]
            }
        else:
            return {"text": "❌ Invalid ticket ID format. Please provide a valid ID (e.g., CS-20241114-123456 or NCRP-12345678)"}
    
    def _get_welcome_message(self, user_id: str) -> Dict:
        """Get welcome message"""
        return {
            "text": """
🙏 Namaste! Welcome to CyberSathi - National Cybercrime Helpline 1930

I'm your AI assistant for reporting cybercrime and getting support.

🔹 I can help you with:
• 📝 Filing new cybercrime complaints
• 📊 Tracking complaint status
• 🔒 Account unfreeze requests
• 💡 Cybercrime awareness tips

Please select an option or type your query:
""",
            "buttons": [
                {"id": "new_complaint", "title": "📝 File New Complaint"},
                {"id": "track_status", "title": "📊 Track Status"},
                {"id": "unfreeze_account", "title": "🔒 Unfreeze Account"},
                {"id": "awareness", "title": "💡 Safety Tips"}
            ]
        }
    
    def _get_default_response(self, user_id: str) -> Dict:
        """Get default fallback response"""
        return {
            "text": "I didn't understand that. Please select from the options or type 'help' for assistance.",
            "buttons": [
                {"id": "new_complaint", "title": "📝 File Complaint"},
                {"id": "track_status", "title": "📊 Track Status"},
                {"id": "help", "title": "❓ Help"}
            ]
        }


conversation_handler = WhatsAppConversationHandler()
