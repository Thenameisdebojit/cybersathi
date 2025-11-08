# backend/app/services/whatsapp_adapter.py
"""
WhatsApp adapter skeleton.
- For dev uses "mock" send (prints to stdout)
- When WHATSAPP_API_URL and WHATSAPP_API_TOKEN set, performs real HTTP call (Meta Cloud or Twilio)
"""

import os
import requests
from app.config import Settings

settings = Settings()

def send_text(phone: str, text: str) -> dict:
    token = settings.WHATSAPP_API_TOKEN
    url = settings.WHATSAPP_API_URL
    if not token or not url:
        # mock mode
        print(f"[whatsapp_adapter] MOCK send to {phone}: {text}")
        return {"status": "mock", "phone": phone, "text": text}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text}
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=8)
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_template(phone: str, template_name: str, components: dict = None):
    # Placeholder for template sends (WhatsApp templates)
    text = f"[template:{template_name}]"
    if components:
        text += " " + str(components)
    return send_text(phone, text)
