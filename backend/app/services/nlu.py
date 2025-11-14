"""
Natural Language Understanding (NLU) Service for CyberSathi WhatsApp Chatbot
Implements keyword + regex based intent classification without ML/LLM
Based on Prompt 3 requirements
"""

import re
from typing import Dict, Optional, List
from enum import Enum


class Intent(str, Enum):
    """Root intents for conversation routing"""
    NEW_COMPLAINT = "NEW_COMPLAINT"
    CHECK_STATUS = "CHECK_STATUS"
    ACCOUNT_UNFREEZE = "ACCOUNT_UNFREEZE"
    OTHER_QUERY = "OTHER_QUERY"
    
    FINANCIAL_FRAUD = "FINANCIAL_FRAUD"
    
    FACEBOOK_FRAUD = "FACEBOOK_FRAUD"
    INSTAGRAM_FRAUD = "INSTAGRAM_FRAUD"
    X_TWITTER_FRAUD = "X_TWITTER_FRAUD"
    WHATSAPP_FRAUD = "WHATSAPP_FRAUD"
    TELEGRAM_FRAUD = "TELEGRAM_FRAUD"
    GMAIL_FRAUD = "GMAIL_FRAUD"
    
    HACKED_ACCOUNT = "HACKED_ACCOUNT"
    IMPERSONATION = "IMPERSONATION"
    OBSCENE_CONTENT = "OBSCENE_CONTENT"


class Platform(str, Enum):
    """Social media platforms"""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    X_TWITTER = "x_twitter"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    GMAIL = "gmail"
    UNKNOWN = "unknown"


class NLUService:
    """
    Rule-based NLU service for intent detection and entity extraction
    No deep learning, no LLMs - pure keyword/regex matching
    """
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_patterns = self._initialize_entity_patterns()
    
    def _initialize_intent_patterns(self) -> Dict[Intent, List[re.Pattern]]:
        """Initialize regex patterns for each intent"""
        return {
            # Root Intents
            Intent.NEW_COMPLAINT: [
                re.compile(r'\b(new\s+)?complaint\b', re.IGNORECASE),
                re.compile(r'\bscam(med)?\b', re.IGNORECASE),
                re.compile(r'\bfraud(ed)?\b', re.IGNORECASE),
                re.compile(r'\bcyber\s*crime\b', re.IGNORECASE),
                re.compile(r'\breport\b', re.IGNORECASE),
                re.compile(r'\bhel+p\b', re.IGNORECASE),
                re.compile(r'\bcheated\b', re.IGNORECASE),
                re.compile(r'\bduped\b', re.IGNORECASE),
                re.compile(r'\bfile\s+complaint\b', re.IGNORECASE),
            ],
            Intent.CHECK_STATUS: [
                re.compile(r'\bstatus\b', re.IGNORECASE),
                re.compile(r'\btrack(ing)?\b', re.IGNORECASE),
                re.compile(r'\backnowledgement\b', re.IGNORECASE),
                re.compile(r'\bticket\b', re.IGNORECASE),
                re.compile(r'\bCS-\d+\b', re.IGNORECASE),
                re.compile(r'\bNCRP-\d+\b', re.IGNORECASE),
                re.compile(r'\bcheck\s+my\s+(case|complaint|status)\b', re.IGNORECASE),
                re.compile(r'\bwhere\s+is\s+my\b', re.IGNORECASE),
            ],
            Intent.ACCOUNT_UNFREEZE: [
                re.compile(r'\bunfreeze\b', re.IGNORECASE),
                re.compile(r'\baccount.*(freez|frozen)\b', re.IGNORECASE),
                re.compile(r'\bfrozen\b.*\baccount\b', re.IGNORECASE),
                re.compile(r'\bblocked\b.*\baccount\b', re.IGNORECASE),
                re.compile(r'\brestore\b.*\baccount\b', re.IGNORECASE),
                re.compile(r'\baccount.*\b(blocked|locked)\b', re.IGNORECASE),
            ],
            
            # Financial Fraud
            Intent.FINANCIAL_FRAUD: [
                re.compile(r'\bupi\b', re.IGNORECASE),
                re.compile(r'\bmoney\b', re.IGNORECASE),
                re.compile(r'\btransaction\b', re.IGNORECASE),
                re.compile(r'\bdeducted\b', re.IGNORECASE),
                re.compile(r'\bimps\b', re.IGNORECASE),
                re.compile(r'\bneft\b', re.IGNORECASE),
                re.compile(r'\brtgs\b', re.IGNORECASE),
                re.compile(r'\bbank\b', re.IGNORECASE),
                re.compile(r'\bpayment\b', re.IGNORECASE),
                re.compile(r'\brupees?\b', re.IGNORECASE),
                re.compile(r'₹\d+', re.IGNORECASE),
                re.compile(r'\butr\b', re.IGNORECASE),
                re.compile(r'\bonline\s+payment\b', re.IGNORECASE),
                re.compile(r'\bpaytm\b', re.IGNORECASE),
                re.compile(r'\bphonep(e|ay)\b', re.IGNORECASE),
                re.compile(r'\bgpay\b', re.IGNORECASE),
            ],
            
            # Social Media Fraud
            Intent.FACEBOOK_FRAUD: [
                re.compile(r'\bfacebook\b', re.IGNORECASE),
                re.compile(r'\bfb\b', re.IGNORECASE),
                re.compile(r'\bmeta\b', re.IGNORECASE),
            ],
            Intent.INSTAGRAM_FRAUD: [
                re.compile(r'\binstagram\b', re.IGNORECASE),
                re.compile(r'\binsta\b', re.IGNORECASE),
                re.compile(r'\big\b', re.IGNORECASE),
            ],
            Intent.X_TWITTER_FRAUD: [
                re.compile(r'\btwitter\b', re.IGNORECASE),
                re.compile(r'\bx\.com\b', re.IGNORECASE),
                re.compile(r'\btweet\b', re.IGNORECASE),
            ],
            Intent.WHATSAPP_FRAUD: [
                re.compile(r'\bwhatsapp\b', re.IGNORECASE),
                re.compile(r'\bwa\b', re.IGNORECASE),
                re.compile(r'\bwhats\s*app\b', re.IGNORECASE),
            ],
            Intent.TELEGRAM_FRAUD: [
                re.compile(r'\btelegram\b', re.IGNORECASE),
            ],
            Intent.GMAIL_FRAUD: [
                re.compile(r'\bgmail\b', re.IGNORECASE),
                re.compile(r'\bgoogle\s+account\b', re.IGNORECASE),
                re.compile(r'\bemail\s+hacked?\b', re.IGNORECASE),
            ],
            
            # Enhancement Intents
            Intent.HACKED_ACCOUNT: [
                re.compile(r'\bhacked?\b', re.IGNORECASE),
                re.compile(r'\bhacking\b', re.IGNORECASE),
                re.compile(r'\baccount\s+compromised\b', re.IGNORECASE),
                re.compile(r'\bunauthori[sz]ed\s+access\b', re.IGNORECASE),
            ],
            Intent.IMPERSONATION: [
                re.compile(r'\bimpersonat(e|ion)\b', re.IGNORECASE),
                re.compile(r'\bfake\s+profile\b', re.IGNORECASE),
                re.compile(r'\bpretending\s+to\s+be\b', re.IGNORECASE),
                re.compile(r'\bidentity\s+theft\b', re.IGNORECASE),
            ],
            Intent.OBSCENE_CONTENT: [
                re.compile(r'\bobscene\b', re.IGNORECASE),
                re.compile(r'\bpornography\b', re.IGNORECASE),
                re.compile(r'\bvulgar\b', re.IGNORECASE),
                re.compile(r'\binappropriate\s+content\b', re.IGNORECASE),
                re.compile(r'\bmorphed\s+photo\b', re.IGNORECASE),
            ],
        }
    
    def _initialize_entity_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for entity extraction"""
        return {
            'utr_number': re.compile(r'\b\d{12,16}\b'),
            'phone_number': re.compile(r'\b[6-9]\d{9}\b'),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'amount': re.compile(r'₹?\s*\d+(?:,\d+)*(?:\.\d{2})?'),
            'date': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            'ticket_id': re.compile(r'\b(CS|NCRP)-\d{8}-\d{6}\b', re.IGNORECASE),
        }
    
    def detect_intent(self, text: str) -> Intent:
        """
        Detect primary intent from user message
        Priority order: Most specific intents first, then general intents
        
        Args:
            text: User's message text
            
        Returns:
            Detected Intent enum value
        """
        if not text or not text.strip():
            return Intent.OTHER_QUERY
        
        text = text.strip()
        
        intent_priority = [
            Intent.CHECK_STATUS,
            Intent.ACCOUNT_UNFREEZE,
            Intent.FINANCIAL_FRAUD,
            Intent.FACEBOOK_FRAUD,
            Intent.INSTAGRAM_FRAUD,
            Intent.X_TWITTER_FRAUD,
            Intent.WHATSAPP_FRAUD,
            Intent.TELEGRAM_FRAUD,
            Intent.GMAIL_FRAUD,
            Intent.HACKED_ACCOUNT,
            Intent.IMPERSONATION,
            Intent.OBSCENE_CONTENT,
            Intent.NEW_COMPLAINT,
        ]
        
        for intent in intent_priority:
            patterns = self.intent_patterns.get(intent, [])
            for pattern in patterns:
                if pattern.search(text):
                    return intent
        
        return Intent.OTHER_QUERY
    
    def detect_platform(self, text: str) -> Platform:
        """
        Detect social media platform from user message
        
        Args:
            text: User's message text
            
        Returns:
            Detected Platform enum value
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['facebook', 'fb']):
            return Platform.FACEBOOK
        elif any(word in text_lower for word in ['instagram', 'insta', 'ig']):
            return Platform.INSTAGRAM
        elif any(word in text_lower for word in ['twitter', 'x.com', 'tweet']):
            return Platform.X_TWITTER
        elif 'whatsapp' in text_lower or 'wa' in text_lower:
            return Platform.WHATSAPP
        elif 'telegram' in text_lower:
            return Platform.TELEGRAM
        elif any(word in text_lower for word in ['gmail', 'google account']):
            return Platform.GMAIL
        
        return Platform.UNKNOWN
    
    def extract_entities(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract entities from user message using regex patterns
        
        Args:
            text: User's message text
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        for entity_name, pattern in self.entity_patterns.items():
            match = pattern.search(text)
            entities[entity_name] = match.group(0) if match else None
        
        return entities
    
    def classify_fraud_type(self, intent: Intent) -> str:
        """
        Classify fraud into A1 (Financial) or A2 (Social Media) branches
        
        Args:
            intent: Detected Intent
            
        Returns:
            "A1" for financial fraud, "A2" for social media fraud, "OTHER" otherwise
        """
        financial_intents = {Intent.FINANCIAL_FRAUD}
        social_media_intents = {
            Intent.FACEBOOK_FRAUD,
            Intent.INSTAGRAM_FRAUD,
            Intent.X_TWITTER_FRAUD,
            Intent.WHATSAPP_FRAUD,
            Intent.TELEGRAM_FRAUD,
            Intent.GMAIL_FRAUD,
        }
        
        if intent in financial_intents:
            return "A1"
        elif intent in social_media_intents:
            return "A2"
        else:
            return "OTHER"
    
    def analyze_message(self, text: str) -> Dict:
        """
        Complete NLU analysis of user message
        
        Args:
            text: User's message text
            
        Returns:
            Dictionary containing:
                - intent: Detected intent
                - platform: Detected platform (if social media)
                - fraud_type: A1/A2/OTHER classification
                - entities: Extracted entities
        """
        intent = self.detect_intent(text)
        platform = self.detect_platform(text)
        fraud_type = self.classify_fraud_type(intent)
        entities = self.extract_entities(text)
        
        return {
            "intent": intent,
            "platform": platform,
            "fraud_type": fraud_type,
            "entities": entities,
            "original_text": text
        }


nlu_service = NLUService()
