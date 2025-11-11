# WhatsApp Integration Guide

## Overview
CyberSathi integrates with WhatsApp Business API (Meta Cloud API) to provide a chatbot interface for reporting cybercrimes.

## Setup

### 1. Meta Developer Account
1. Create a Meta Developer account at https://developers.facebook.com
2. Create a new app with WhatsApp Business API
3. Get your App ID, App Secret, and Phone Number ID

### 2. Webhook Configuration

Configure your webhook URL in Meta Dashboard:
```
URL: https://your-domain.com/webhook/whatsapp
Verify Token: <your_verify_token>
```

Subscribe to these webhook fields:
- `messages`
- `message_status` (optional)

### 3. Environment Variables

```bash
META_VERIFY_TOKEN=your_verify_token_here
META_ACCESS_TOKEN=your_meta_access_token_here
META_PHONE_NUMBER_ID=your_phone_number_id_here
META_BUSINESS_ACCOUNT_ID=your_business_account_id_here
WHATSAPP_API_VERSION=v18.0
```

## Message Flow

### 1. User Sends Message
User sends a message via WhatsApp → Meta Cloud API → Your Webhook

### 2. Webhook Receives Message
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "field": "messages",
      "value": {
        "messages": [{
          "from": "919999999999",
          "id": "wamid.xxx",
          "type": "text",
          "text": {
            "body": "I want to report a fraud"
          }
        }]
      }
    }]
  }]
}
```

### 3. Process with NLP
The message is processed by the NLP service to detect intent and language.

### 4. Send Response
```python
await whatsapp_service.send_message(
    to="919999999999",
    message="How can I help you?",
    buttons=[
        {"id": "report_fraud", "title": "Report Fraud"},
        {"id": "track_case", "title": "Track Case"}
    ]
)
```

## Message Types

### Text Messages
```python
{
  "messaging_product": "whatsapp",
  "to": "919999999999",
  "type": "text",
  "text": {
    "body": "Your message here"
  }
}
```

### Interactive Messages (Buttons)
```python
{
  "messaging_product": "whatsapp",
  "to": "919999999999",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {"text": "Choose an option:"},
    "action": {
      "buttons": [
        {"type": "reply", "reply": {"id": "btn1", "title": "Option 1"}},
        {"type": "reply", "reply": {"id": "btn2", "title": "Option 2"}}
      ]
    }
  }
}
```

### Interactive Messages (List)
```python
{
  "messaging_product": "whatsapp",
  "to": "919999999999",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "body": {"text": "Select fraud type:"},
    "action": {
      "button": "Choose",
      "sections": [{
        "title": "Fraud Types",
        "rows": [
          {"id": "upi", "title": "UPI Fraud"},
          {"id": "phishing", "title": "Phishing"}
        ]
      }]
    }
  }
}
```

### Template Messages
```python
await whatsapp_service.send_template_message(
    to="919999999999",
    template_name="case_registered",
    language_code="en",
    parameters=["CS-A1B2C3D4"]
)
```

## Conversation Flow

### 1. Welcome Message
User: "Hi"
Bot: Shows welcome message with quick reply buttons

### 2. Report Fraud Flow
1. User clicks "Report Fraud"
2. Bot asks for fraud type
3. User selects type
4. Bot asks for description
5. User provides details
6. Bot asks for amount
7. User enters amount
8. Bot creates complaint and returns reference ID

### 3. Track Case Flow
1. User clicks "Track Case"
2. Bot asks for reference ID
3. User provides ID
4. Bot fetches and displays status

### 4. Awareness Tips
User clicks "Safety Tips"
Bot: Sends cybersecurity awareness content

## Signature Verification

Verify incoming webhooks using X-Hub-Signature-256 header:

```python
import hashlib
import hmac

def verify_signature(payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        ACCESS_TOKEN.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    provided = signature.split('=')[1]
    return hmac.compare_digest(expected, provided)
```

## Error Handling

### Network Errors
- Automatic retry with exponential backoff
- Log all errors for monitoring

### Invalid Messages
- Gracefully handle unsupported message types
- Send helpful error messages to users

### Rate Limiting
- Meta enforces rate limits per phone number
- Queue messages if limit is reached

## Multilingual Support

### Language Detection
```python
language = nlp_service.detect_language(text)
# Returns: "english" or "odia"
```

### Responses
```python
if language == "odia":
    message = "ସାଇବରସାଥୀରେ ସ୍ୱାଗତ!"
else:
    message = "Welcome to CyberSathi!"
```

## Testing

### Webhook Testing
Use Meta's Webhooks tool to send test messages.

### Local Testing with ngrok
```bash
ngrok http 8000
# Use ngrok URL in Meta webhook config
```

## Best Practices

1. **Response Time**: Reply within 24 hours to maintain session
2. **Message Templates**: Use approved templates for notifications
3. **User Privacy**: Never log sensitive user data
4. **Error Messages**: Provide clear, helpful error messages
5. **Fallback**: Always have a fallback for unrecognized inputs

## Limitations

- Maximum 3 buttons per message
- Button titles: max 20 characters
- List rows: max 10 items
- Message text: max 4096 characters
- 24-hour session window for free-form messages

## Support

- WhatsApp Business API Docs: https://developers.facebook.com/docs/whatsapp
- Meta Support: https://business.facebook.com/support
