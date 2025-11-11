import httpx
import logging
from typing import List, Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class WhatsAppService:
    def __init__(self):
        self.api_version = settings.WHATSAPP_API_VERSION
        self.phone_number_id = settings.META_PHONE_NUMBER_ID
        self.access_token = settings.META_ACCESS_TOKEN
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"
    
    async def send_message(
        self,
        to: str,
        message: str,
        buttons: Optional[List[Dict]] = None
    ) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        if buttons and len(buttons) > 0:
            payload = self._create_interactive_message(to, message, buttons)
        else:
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"WhatsApp API error: {e}")
            return {"error": str(e)}
    
    def _create_interactive_message(self, to: str, message: str, buttons: List[Dict]) -> Dict:
        if len(buttons) <= 3:
            return {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": message},
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": btn.get("id", f"btn_{i}"),
                                    "title": btn.get("title", f"Option {i+1}")[:20]
                                }
                            }
                            for i, btn in enumerate(buttons[:3])
                        ]
                    }
                }
            }
        else:
            return {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {"text": message},
                    "action": {
                        "button": "Choose Option",
                        "sections": [
                            {
                                "title": "Options",
                                "rows": [
                                    {
                                        "id": btn.get("id", f"btn_{i}"),
                                        "title": btn.get("title", f"Option {i+1}")[:24],
                                        "description": btn.get("description", "")[:72]
                                    }
                                    for i, btn in enumerate(buttons[:10])
                                ]
                            }
                        ]
                    }
                }
            }
    
    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "en",
        parameters: Optional[List[str]] = None
    ) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        
        if parameters:
            payload["template"]["components"] = [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": param} for param in parameters]
                }
            ]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"WhatsApp template API error: {e}")
            return {"error": str(e)}


whatsapp_service = WhatsAppService()
