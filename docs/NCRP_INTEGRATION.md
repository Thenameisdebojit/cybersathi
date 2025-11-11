# NCRP Integration Specification

## Overview
Integration with the National Cybercrime Reporting Portal (NCRP) at cybercrime.gov.in for submitting and tracking complaints.

## Implementation Details

### NCRP Adapter (`backend/app/services/ncrp_adapter.py`)

The NCRP adapter handles all communication with the cybercrime portal.

#### Features
1. **OAuth2 Authentication**: Supports OAuth2 token-based authentication
2. **Retry Logic**: Automatic retry with exponential backoff (max 3 attempts)
3. **Idempotency**: Uses idempotency keys to prevent duplicate submissions
4. **Response Caching**: Caches responses to reduce API calls
5. **Mock Mode**: Development mode for testing without live API

### Authentication

#### OAuth2 Flow
```python
# Token endpoint
POST https://cybercrime.gov.in/api/oauth/token

Request:
{
  "grant_type": "client_credentials",
  "client_id": "<your_client_id>",
  "client_secret": "<your_client_secret>"
}

Response:
{
  "access_token": "<token>",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### API Endpoints

#### Submit Complaint
```python
POST https://cybercrime.gov.in/api/complaints

Headers:
- Authorization: Bearer <access_token>
- X-API-Key: <api_key>
- X-Idempotency-Key: <unique_id>

Payload:
{
  "complaint_type": "upi_fraud",
  "description": "Description of the incident",
  "victim_name": "John Doe",
  "victim_phone": "+919999999999",
  "victim_email": "john@example.com",
  "incident_date": "2025-01-10",
  "amount_lost": 5000,
  "platform": "PhonePe",
  "evidence": []
}

Response:
{
  "status": "submitted",
  "complaint_id": "NCRP-12345678",
  "reference_id": "NCRP-12345678",
  "message": "Complaint submitted successfully"
}
```

#### Get Complaint Status
```python
GET https://cybercrime.gov.in/api/complaints/{complaint_id}

Headers:
- Authorization: Bearer <access_token>
- X-API-Key: <api_key>

Response:
{
  "complaint_id": "NCRP-12345678",
  "status": "under_review",
  "last_updated": "2025-01-10T15:30:00Z",
  "assigned_officer": "Officer Name",
  "remarks": "Under investigation"
}
```

#### Update Complaint
```python
PATCH https://cybercrime.gov.in/api/complaints/{complaint_id}

Headers:
- Authorization: Bearer <access_token>
- X-API-Key: <api_key>

Payload:
{
  "additional_info": "New information",
  "evidence": ["file1.pdf", "file2.jpg"]
}

Response:
{
  "complaint_id": "NCRP-12345678",
  "status": "updated",
  "message": "Complaint updated successfully"
}
```

## Error Handling

### Retry Logic
- Max retries: 3
- Backoff factor: 2 (exponential)
- Wait times: 2s, 4s, 8s

### Error Responses
- `401 Unauthorized`: Token expired or invalid
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Complaint not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Server Error`: NCRP server issue

## Mock Mode

For development and testing, the adapter supports mock mode:

```python
# Enable mock mode in .env
DEBUG=True
NCRP_API_KEY=

# Mock responses will be generated
{
  "status": "submitted",
  "complaint_id": "NCRP-MOCK123",
  "message": "Complaint received (mock mode)"
}
```

## Data Mapping

| CyberSathi Field | NCRP Field |
|------------------|------------|
| incident_type | complaint_type |
| name | victim_name |
| phone | victim_phone |
| email | victim_email |
| description | description |
| incident_date | incident_date |
| amount | amount_lost |
| platform | platform |
| attachments | evidence |

## Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **MTLS**: Support for mutual TLS authentication
3. **Encryption**: All data transmitted over HTTPS
4. **Data Sanitization**: Input validation before submission
5. **Audit Logging**: All API calls are logged

## Testing

### Mock NCRP Server
A mock server is available for testing:
```bash
python backend/tests/mock_ncrp.py
```

### Integration Tests
```bash
pytest backend/tests/test_ncrp_adapter.py
```

## Configuration

Required environment variables:
```bash
NCRP_API_URL=https://cybercrime.gov.in/api
NCRP_CLIENT_ID=your_client_id
NCRP_CLIENT_SECRET=your_client_secret
NCRP_API_KEY=your_api_key
```

## Rate Limits
- Submissions: 100 per hour
- Status checks: 1000 per hour
- Updates: 50 per hour

## Support
For NCRP API access and credentials, contact:
- Email: api@cybercrime.gov.in
- Helpline: 1930
