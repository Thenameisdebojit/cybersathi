# backend/app/services/llm_chatbot.py
"""LLM Chatbot service using OpenAI for answering user questions."""
import os
import logging
from typing import Optional
import openai

logger = logging.getLogger(__name__)


class LLMChatbot:
    """AI Chatbot for answering cybercrime-related questions."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            logger.info("✅ OpenAI LLM initialized")
        else:
            logger.warning("⚠️ OPENAI_API_KEY not found, chatbot will be disabled")
    
    @property
    def is_available(self) -> bool:
        """Check if chatbot is available."""
        return self.api_key is not None
    
    async def get_response(self, user_message: str, language: str = "en") -> str:
        """
        Get AI response to user question about cybercrime.
        
        Args:
            user_message: User's question
            language: Language code (en, hi, od)
            
        Returns:
            AI-generated response
        """
        if not self.is_available:
            return "AI assistant is currently unavailable. Please contact support at 1930."
        
        try:
            # System prompt for cybercrime assistant
            system_prompt = self._get_system_prompt(language)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "500")),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return "I apologize, but I'm having trouble processing your question right now. Please try again or contact our helpline at 1930."
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on language."""
        prompts = {
            "en": """You are CyberSathi, an AI assistant for India's National Cybercrime Helpline (1930). 
            Your role is to help citizens understand cybercrime, how to report it, and what steps to take.
            
            Key information:
            - You help with: UPI fraud, phishing, identity theft, online job fraud, investment fraud, social media hacks, ransomware
            - Always be empathetic and supportive to victims
            - Provide actionable steps they can take
            - Encourage them to file FIR through cybercrime.gov.in or call 1930
            - Keep responses concise and helpful
            - If you don't know something, direct them to call 1930
            
            Be professional, compassionate, and informative.""",
            
            "hi": """आप CyberSathi हैं, भारत की राष्ट्रीय साइबर अपराध हेल्पलाइन (1930) के लिए एक AI सहायक।
            आपकी भूमिका नागरिकों को साइबर अपराध को समझने, इसकी रिपोर्ट कैसे करें और क्या कदम उठाएं, इसमें मदद करना है।
            
            महत्वपूर्ण जानकारी:
            - आप मदद करते हैं: UPI धोखाधड़ी, फिशिंग, पहचान की चोरी, ऑनलाइन नौकरी धोखाधड़ी, निवेश धोखाधड़ी, सोशल मीडिया हैक, रैंसमवेयर
            - हमेशा पीड़ितों के प्रति सहानुभूतिपूर्ण और सहायक रहें
            - वे जो कदम उठा सकते हैं, उन्हें बताएं
            - उन्हें cybercrime.gov.in के माध्यम से FIR दर्ज करने या 1930 पर कॉल करने के लिए प्रोत्साहित करें
            - जवाब संक्षिप्त और सहायक रखें
            
            पेशेवर, दयालु और जानकारीपूर्ण बनें।""",
            
            "od": """ଆପଣ CyberSathi, ଭାରତର ଜାତୀୟ ସାଇବର କ୍ରାଇମ ହେଲ୍ପଲାଇନ (1930) ପାଇଁ ଏକ AI ସହାୟକ।
            ଆପଣଙ୍କର ଭୂମିକା ହେଉଛି ନାଗରିକମାନଙ୍କୁ ସାଇବର କ୍ରାଇମ ବୁଝିବାରେ, ଏହାକୁ କିପରି ରିପୋର୍ଟ କରିବେ ଏବଂ କେଉଁ ପଦକ୍ଷେପ ନେବେ ତାହା ସାହାଯ୍ୟ କରିବା।
            
            ସବୁବେଳେ ପେଶାଦାର, ଦୟାଳୁ ଏବଂ ସୂଚନାପୂର୍ଣ୍ଣ ହୁଅନ୍ତୁ।"""
        }
        
        return prompts.get(language, prompts["en"])


# Singleton instance
llm_chatbot = LLMChatbot()
