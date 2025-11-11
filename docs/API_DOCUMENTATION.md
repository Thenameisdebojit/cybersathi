# CyberSathi API Documentation

## Overview
CyberSathi Backend API provides endpoints for managing cybercrime complaints, tracking cases, and integrating with the WhatsApp chatbot.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health Check
```http
GET /health
```
Returns the API health status.

**Response:**
```json
{
  "status": "ok",
  "service": "CyberSathi Backend"
}
```

### Complaints

#### Create Complaint
```http
POST /api/v1/complaints/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+919999999999",
  "language": "en",
  "incident_type": "upi_fraud",
  "description": "Lost money via UPI scam",
  "date_of_incident": "2025-01-10T10:00:00Z",
  "amount": 5000,
  "platform": "PhonePe",
  "txn_id": "TXN123456"
}
```

**Response:**
```json
{
  "id": 1,
  "reference_id": "CS-A1B2C3D4",
  "name": "John Doe",
  "phone": "+919999999999",
  "incident_type": "upi_fraud",
  "status": "registered",
  "created_at": "2025-01-10T10:05:00Z"
}
```

#### List Complaints
```http
GET /api/v1/complaints/list?limit=100
```

**Query Parameters:**
- `limit` (optional): Maximum number of complaints to return (default: 100)

**Response:** Array of complaint objects

#### Get Complaint by Reference ID
```http
GET /api/v1/complaints/{reference_id}
```

**Response:** Single complaint object or 404 if not found

### WhatsApp Webhook

#### Webhook Verification
```http
GET /webhook/whatsapp
```

**Query Parameters:**
- `hub.mode`: subscription
- `hub.challenge`: verification token
- `hub.verify_token`: your verify token

Used by Meta to verify your webhook endpoint.

#### Handle Incoming Messages
```http
POST /webhook/whatsapp
```

**Headers:**
- `X-Hub-Signature-256`: Message signature for verification

Receives and processes incoming WhatsApp messages from users.

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message description"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting
Currently not implemented. Future versions will include rate limiting.

## Webhooks
The API can send webhooks for complaint status updates. Configure webhook URL in settings.
