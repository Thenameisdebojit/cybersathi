import hashlib
import hmac
import json
from fastapi import APIRouter, Request, Response, HTTPException, Header
from typing import Optional
from app.config import settings
from app.services.whatsapp_service import whatsapp_service
from app.services.nlp_service import nlp_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def verify_webhook_signature(payload: bytes, signature: Optional[str]) -> bool:
    if not signature or settings.DEBUG:
        return True
    
    try:
        expected_signature = hmac.new(
            settings.META_ACCESS_TOKEN.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        signature_parts = signature.split('=')
        if len(signature_parts) != 2:
            return False
        
        provided_signature = signature_parts[1]
        return hmac.compare_digest(expected_signature, provided_signature)
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False


@router.get("/webhook/whatsapp")
async def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == settings.META_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")
    
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook/whatsapp")
async def handle_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None)
):
    try:
        body = await request.body()
        
        if not verify_webhook_signature(body, x_hub_signature_256):
            raise HTTPException(status_code=403, detail="Invalid signature")
        
        data = json.loads(body)
        
        if data.get("object") != "whatsapp_business_account":
            return {"status": "ignored"}
        
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})
                    
                    messages = value.get("messages", [])
                    for message in messages:
                        await process_message(message, value)
        
        return {"status": "ok"}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def process_message(message: dict, value: dict):
    try:
        from_number = message.get("from")
        message_id = message.get("id")
        message_type = message.get("type")
        
        if message_type == "text":
            text = message.get("text", {}).get("body", "")
            
            nlp_response = await nlp_service.process_message(from_number, text)
            
            await whatsapp_service.send_message(
                to=from_number,
                message=nlp_response.get("text", "Thank you for contacting CyberSathi!"),
                buttons=nlp_response.get("buttons", [])
            )
        
        elif message_type == "interactive":
            interactive = message.get("interactive", {})
            button_reply = interactive.get("button_reply", {})
            list_reply = interactive.get("list_reply", {})
            
            response_id = button_reply.get("id") or list_reply.get("id")
            
            if response_id:
                nlp_response = await nlp_service.process_button_click(from_number, response_id)
                await whatsapp_service.send_message(
                    to=from_number,
                    message=nlp_response.get("text", "Processing your request...")
                )
        
        logger.info(f"Processed message {message_id} from {from_number}")
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
