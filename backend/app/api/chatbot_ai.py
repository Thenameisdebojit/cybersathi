# backend/app/api/chatbot_ai.py
"""AI Chatbot API using OpenAI for cybercrime questions."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

# Initialize OpenAI client with safe error handling
_openai_client: Optional[OpenAI] = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        _openai_client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Warning: Failed to initialize OpenAI client: {e}")

def get_openai_client() -> OpenAI:
    """Get OpenAI client or raise error if not configured."""
    if _openai_client is None:
        raise HTTPException(
            status_code=503,
            detail="AI chatbot is not configured. Please set OPENAI_API_KEY environment variable."
        )
    return _openai_client

# System prompt for cybercrime knowledge
CYBERCRIME_SYSTEM_PROMPT = """You are an expert AI assistant for India's Cybercrime Helpline (1930) - CyberSathi. 
Your role is to help users understand cybercrime, fraud prevention, and how to report incidents.

Knowledge areas:
- All 23 types of financial fraud (Investment/Trading, Customer Care Fraud, UPI Fraud, APK Fraud, Fake Franchisee, 
  Online Job Fraud, Debit/Credit Card Fraud, E-commerce, Loan App, Sextortion, OLX, Lottery, Hotel Booking, 
  Gaming App, AEPS, Tower Installation, E-Wallet, Digital Arrest, Fake Website, Ticket Booking, Insurance Maturity, Others)
- Social media fraud (Facebook, Instagram, X/Twitter, WhatsApp, Telegram, Gmail hacking, Fraud calls/SMS)
- How to file complaints on India's National Cybercrime Reporting Portal (cybercrime.gov.in)
- Evidence collection and documentation
- Account freezing and unfreezing procedures
- Prevention tips and best practices

Guidelines:
- Be helpful, clear, and empathetic
- Provide actionable advice
- Mention the 1930 helpline when appropriate
- Explain technical terms in simple language
- Focus on Indian context and laws
- If asked about specific cases, advise to call 1930 or visit cybercrime.gov.in
- Never provide legal advice or guarantee outcomes

Answer concisely but comprehensively."""


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request with message history."""
    messages: List[ChatMessage]
    max_tokens: int = 500


class ChatResponse(BaseModel):
    """Chat response."""
    message: str
    usage: dict


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat with AI assistant about cybercrime.
    
    Uses OpenAI GPT-4 to answer questions about cybercrime, fraud types,
    prevention, and reporting procedures.
    """
    # Get client with proper error handling
    client = get_openai_client()
    
    try:
        # Prepare messages with system prompt
        messages = [
            {"role": "system", "content": CYBERCRIME_SYSTEM_PROMPT}
        ]
        
        # Add user messages from history
        for msg in request.messages[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use gpt-4o-mini for cost efficiency
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=0.7,
        )
        
        return ChatResponse(
            message=response.choices[0].message.content,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/chat/examples")
async def get_example_questions():
    """Get example questions users can ask."""
    return {
        "examples": [
            "What is UPI fraud and how can I protect myself?",
            "I received a suspicious call claiming to be from my bank. What should I do?",
            "How do I file a cybercrime complaint in India?",
            "What evidence do I need to report online fraud?",
            "My social media account was hacked. What steps should I take?",
            "What is digital arrest fraud?",
            "How can I check if a website is fake?",
            "What is the process to unfreeze my bank account?",
            "I lost money in an investment scam. Can I get it back?",
            "What are the different types of online job frauds?"
        ]
    }
