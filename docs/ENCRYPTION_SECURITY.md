# End-to-End Encryption & Security

## Overview
CyberSathi implements end-to-end encryption for sensitive data to ensure user privacy and compliance with data protection regulations.

## Encryption Service

### Implementation (`backend/app/services/encryption_service.py`)

The encryption service uses **Fernet** (symmetric encryption) with AES-256 in CBC mode.

### Key Features
1. **Symmetric Encryption**: Uses Fernet for fast, secure encryption
2. **Field-Level Encryption**: Encrypts specific sensitive fields
3. **Hash Functions**: SHA-256 for non-reversible hashing
4. **Key Management**: Centralized key storage in environment variables

## Encryption Methods

### Encrypt Data
```python
from app.services.encryption_service import encryption_service

encrypted = encryption_service.encrypt("sensitive data")
# Returns: base64-encoded encrypted string
```

### Decrypt Data
```python
decrypted = encryption_service.decrypt(encrypted_data)
# Returns: original plaintext string
```

### Hash Data (One-way)
```python
hashed = encryption_service.hash_data("password")
# Returns: SHA-256 hash (non-reversible)
```

### Encrypt Multiple Fields
```python
data = {
    "name": "John Doe",
    "phone": "+919999999999",
    "bank_account": "1234567890"
}

encrypted_data = encryption_service.encrypt_sensitive_fields(
    data, 
    fields=["phone", "bank_account"]
)
# Only specified fields are encrypted
```

## Sensitive Data Fields

The following fields are encrypted before storage:

### User Data
- Phone numbers
- Email addresses  
- Personal identification numbers
- Addresses

### Complaint Data
- Victim contact information
- Bank account numbers
- Transaction IDs
- Evidence file paths

### WhatsApp Messages
- Message content (stored encrypted)
- User phone numbers
- Conversation history

## Key Management

### Environment Configuration
```bash
ENCRYPTION_KEY=your_256_bit_encryption_key_here
```

### Key Requirements
- Minimum length: 32 bytes (256 bits)
- Must be URL-safe base64 encoded
- Rotate keys every 90 days

### Key Generation
```python
from cryptography.fernet import Fernet

# Generate a new key
key = Fernet.generate_key()
print(key.decode())
# Save this to your .env file
```

## Password Hashing

For user passwords, use bcrypt (via passlib):

```python
from app.services.auth_service import get_password_hash, verify_password

# Hash password
hashed = get_password_hash("user_password")

# Verify password
is_valid = verify_password("user_password", hashed)
```

## Data in Transit

### HTTPS Only
All API endpoints use HTTPS in production:
```python
# FastAPI automatically handles HTTPS
# Configure SSL certificates in deployment
```

### WhatsApp Communication
- All messages to/from WhatsApp are encrypted by Meta
- Additional encryption layer for database storage

## Data at Rest

### Database Encryption
- Sensitive fields encrypted before storage
- Database connections use SSL/TLS
- Regular encrypted backups

### File Storage
- Evidence files encrypted before upload
- Access controlled via signed URLs
- Automatic expiry for temporary files

## Compliance

### GDPR Compliance
- Right to be forgotten: encrypted data can be securely deleted
- Data minimization: only essential data encrypted and stored
- Consent management: user consent tracked for data processing

### Indian Data Protection Laws
- Personal data stored and processed in India
- Compliance with IT Act 2000
- Data localization requirements met

## Security Best Practices

### 1. Never Log Decrypted Data
```python
# BAD
logger.info(f"User phone: {decrypted_phone}")

# GOOD
logger.info(f"User phone: {encrypted_phone[:10]}...")
```

### 2. Use Encryption for All Sensitive Fields
```python
complaint_data = {
    "phone": encryption_service.encrypt(phone),
    "description": encryption_service.encrypt(description)
}
```

### 3. Secure Key Storage
- Never commit encryption keys to git
- Use environment variables
- Rotate keys regularly
- Use key management services (AWS KMS, HashiCorp Vault)

### 4. Input Validation
```python
from pydantic import BaseModel, validator

class ComplaintCreate(BaseModel):
    phone: str
    
    @validator('phone')
    def validate_phone(cls, v):
        # Validate phone format before encryption
        if not v.startswith('+91'):
            raise ValueError('Invalid phone number')
        return v
```

## Audit Logging

All encryption/decryption operations are logged:

```python
logger.info(f"Encrypted field: {field_name}, user_id: {user_id}")
```

Logs exclude actual decrypted values for security.

## Testing

### Unit Tests
```bash
pytest backend/tests/test_encryption.py
```

### Security Audits
- Regular penetration testing
- Code security reviews
- Dependency vulnerability scanning

## Key Rotation

### Procedure
1. Generate new encryption key
2. Decrypt all data with old key
3. Re-encrypt with new key
4. Update environment variable
5. Restart services

### Script
```python
# backend/scripts/rotate_keys.py
python backend/scripts/rotate_keys.py --old-key OLD --new-key NEW
```

## Disaster Recovery

### Backup Strategy
- Encrypted database backups daily
- Keys stored separately from data
- Disaster recovery plan documented

### Key Loss
If encryption key is lost, encrypted data cannot be recovered. 
Maintain secure key backups in multiple locations.

## Security Contacts

For security issues:
- Email: security@cybersathi.in
- Report via: https://cybersathi.in/security
- PGP Key: Available on website
