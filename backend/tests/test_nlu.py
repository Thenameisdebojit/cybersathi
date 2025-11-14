"""
Unit tests for NLU Service
Tests all intents and entity extraction as per Prompt 3 requirements
"""

import pytest
from app.services.nlu import nlu_service, Intent, Platform


class TestIntentDetection:
    """Test suite for intent detection"""
    
    def test_new_complaint_intent(self):
        """Test NEW_COMPLAINT intent detection"""
        test_cases = [
            "I want to file a new complaint",
            "I was scammed",
            "fraud happened",
            "help me report cybercrime",
            "I got cheated",
            "someone duped me",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.NEW_COMPLAINT, f"Failed for: {case}"
    
    def test_check_status_intent(self):
        """Test CHECK_STATUS intent detection"""
        test_cases = [
            "check my ticket",
            "what is the status",
            "track my complaint",
            "acknowledgement number CS-12345678",
            "where is my case",
            "NCRP-87654321 status",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.CHECK_STATUS, f"Failed for: {case}"
    
    def test_account_unfreeze_intent(self):
        """Test ACCOUNT_UNFREEZE intent detection"""
        test_cases = [
            "unfreeze my account",
            "account is frozen",
            "blocked account need help",
            "restore my account",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.ACCOUNT_UNFREEZE, f"Failed for: {case}"
    
    def test_financial_fraud_intent(self):
        """Test FINANCIAL_FRAUD intent detection"""
        test_cases = [
            "My money is stuck",
            "UPI payment went wrong",
            "money was deducted from my account",
            "unauthorized transaction of ₹5000",
            "NEFT scam",
            "bank fraud happened",
            "PhonePe payment issue",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.FINANCIAL_FRAUD, f"Failed for: {case}"
    
    def test_facebook_fraud_intent(self):
        """Test FACEBOOK_FRAUD intent detection"""
        test_cases = [
            "my facebook account got hacked",
            "FB fraud",
            "someone hacked my facebook",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.FACEBOOK_FRAUD, f"Failed for: {case}"
    
    def test_instagram_fraud_intent(self):
        """Test INSTAGRAM_FRAUD intent detection"""
        test_cases = [
            "instagram account hacked",
            "insta fraud",
            "IG account issue",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.INSTAGRAM_FRAUD, f"Failed for: {case}"
    
    def test_twitter_fraud_intent(self):
        """Test X_TWITTER_FRAUD intent detection"""
        test_cases = [
            "twitter account hacked",
            "x.com issue",
            "tweet scam",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.X_TWITTER_FRAUD, f"Failed for: {case}"
    
    def test_whatsapp_fraud_intent(self):
        """Test WHATSAPP_FRAUD intent detection"""
        test_cases = [
            "whatsapp scam",
            "WA fraud",
            "someone on whats app cheated me",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.WHATSAPP_FRAUD, f"Failed for: {case}"
    
    def test_telegram_fraud_intent(self):
        """Test TELEGRAM_FRAUD intent detection"""
        test_cases = [
            "telegram scam",
            "fraud on telegram",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.TELEGRAM_FRAUD, f"Failed for: {case}"
    
    def test_gmail_fraud_intent(self):
        """Test GMAIL_FRAUD intent detection"""
        test_cases = [
            "gmail account hacked",
            "google account compromised",
            "email hacked",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.GMAIL_FRAUD, f"Failed for: {case}"
    
    def test_other_query_fallback(self):
        """Test OTHER_QUERY fallback"""
        test_cases = [
            "hello",
            "random text xyz",
            "what is the weather",
            "",
        ]
        
        for case in test_cases:
            intent = nlu_service.detect_intent(case)
            assert intent == Intent.OTHER_QUERY, f"Failed for: {case}"


class TestPlatformDetection:
    """Test suite for platform detection"""
    
    def test_facebook_platform(self):
        """Test Facebook platform detection"""
        assert nlu_service.detect_platform("facebook fraud") == Platform.FACEBOOK
        assert nlu_service.detect_platform("FB scam") == Platform.FACEBOOK
    
    def test_instagram_platform(self):
        """Test Instagram platform detection"""
        assert nlu_service.detect_platform("instagram hacked") == Platform.INSTAGRAM
        assert nlu_service.detect_platform("insta issue") == Platform.INSTAGRAM
    
    def test_twitter_platform(self):
        """Test Twitter/X platform detection"""
        assert nlu_service.detect_platform("twitter scam") == Platform.X_TWITTER
        assert nlu_service.detect_platform("x.com fraud") == Platform.X_TWITTER
    
    def test_whatsapp_platform(self):
        """Test WhatsApp platform detection"""
        assert nlu_service.detect_platform("whatsapp fraud") == Platform.WHATSAPP
    
    def test_telegram_platform(self):
        """Test Telegram platform detection"""
        assert nlu_service.detect_platform("telegram scam") == Platform.TELEGRAM
    
    def test_gmail_platform(self):
        """Test Gmail platform detection"""
        assert nlu_service.detect_platform("gmail hacked") == Platform.GMAIL
        assert nlu_service.detect_platform("google account issue") == Platform.GMAIL
    
    def test_unknown_platform(self):
        """Test unknown platform fallback"""
        assert nlu_service.detect_platform("random text") == Platform.UNKNOWN


class TestEntityExtraction:
    """Test suite for entity extraction"""
    
    def test_utr_extraction(self):
        """Test UTR number extraction"""
        entities = nlu_service.extract_entities("My UTR is 123456789012")
        assert entities['utr_number'] == "123456789012"
    
    def test_phone_extraction(self):
        """Test phone number extraction"""
        entities = nlu_service.extract_entities("Call me at 9876543210")
        assert entities['phone_number'] == "9876543210"
    
    def test_email_extraction(self):
        """Test email extraction"""
        entities = nlu_service.extract_entities("Contact me at user@example.com")
        assert entities['email'] == "user@example.com"
    
    def test_amount_extraction(self):
        """Test amount extraction"""
        entities = nlu_service.extract_entities("Lost ₹5000")
        assert entities['amount'] is not None
    
    def test_date_extraction(self):
        """Test date extraction"""
        entities = nlu_service.extract_entities("Happened on 14/11/2024")
        assert entities['date'] == "14/11/2024"
    
    def test_ticket_id_extraction(self):
        """Test ticket ID extraction"""
        entities = nlu_service.extract_entities("My ticket is CS-20241114-123456")
        assert entities['ticket_id'] == "CS-20241114-123456"


class TestFraudTypeClassification:
    """Test fraud type classification (A1/A2 branches)"""
    
    def test_financial_fraud_classification(self):
        """Test A1 branch classification"""
        intent = Intent.FINANCIAL_FRAUD
        fraud_type = nlu_service.classify_fraud_type(intent)
        assert fraud_type == "A1"
    
    def test_social_media_fraud_classification(self):
        """Test A2 branch classification"""
        social_media_intents = [
            Intent.FACEBOOK_FRAUD,
            Intent.INSTAGRAM_FRAUD,
            Intent.X_TWITTER_FRAUD,
            Intent.WHATSAPP_FRAUD,
            Intent.TELEGRAM_FRAUD,
            Intent.GMAIL_FRAUD,
        ]
        
        for intent in social_media_intents:
            fraud_type = nlu_service.classify_fraud_type(intent)
            assert fraud_type == "A2", f"Failed for intent: {intent}"
    
    def test_other_classification(self):
        """Test OTHER classification"""
        intent = Intent.OTHER_QUERY
        fraud_type = nlu_service.classify_fraud_type(intent)
        assert fraud_type == "OTHER"


class TestCompleteNLUAnalysis:
    """Test complete NLU analysis"""
    
    def test_financial_fraud_analysis(self):
        """Test complete analysis for financial fraud"""
        result = nlu_service.analyze_message("My money ₹10000 was deducted via UPI. UTR: 123456789012")
        
        assert result['intent'] == Intent.FINANCIAL_FRAUD
        assert result['fraud_type'] == "A1"
        assert result['entities']['utr_number'] == "123456789012"
        assert result['entities']['amount'] is not None
    
    def test_social_media_fraud_analysis(self):
        """Test complete analysis for social media fraud"""
        result = nlu_service.analyze_message("My facebook account was hacked yesterday")
        
        assert result['intent'] == Intent.FACEBOOK_FRAUD
        assert result['platform'] == Platform.FACEBOOK
        assert result['fraud_type'] == "A2"
    
    def test_status_check_analysis(self):
        """Test complete analysis for status check"""
        result = nlu_service.analyze_message("Check status for CS-20241114-123456")
        
        assert result['intent'] == Intent.CHECK_STATUS
        assert result['entities']['ticket_id'] == "CS-20241114-123456"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
