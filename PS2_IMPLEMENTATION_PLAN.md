# PS2.pdf Implementation Plan - WhatsApp Chatbot Field Collection

## Executive Summary

The current WhatsApp chatbot implementation collects basic complaint information but is **missing 8 out of 11 required personal identity fields** specified in PS2.pdf. This document provides a detailed plan to implement the complete PS2 workflow.

## Current State vs. PS2 Requirements

### ✅ Currently Collected Fields
1. **Name** (as VICTIM_NAME)
2. **Phone** (as VICTIM_PHONE, with validation)
3. **Email** (as VICTIM_EMAIL, with validation)
4. Incident description
5. Incident date
6. Amount lost
7. Suspect info

### ❌ Missing PS2 Required Fields
1. **Father/Spouse/Guardian Name** - NOT collected
2. **Date of Birth** - NOT collected
3. **Gender** - NOT collected
4. **Village** - NOT collected
5. **Post Office** - NOT collected
6. **Police Station** - NOT collected
7. **District** - NOT collected
8. **PIN Code** - NOT collected

## Implementation Approach (Based on Architect Review)

### Phase 1: Field Configuration System

Create a clean, maintainable field collection system using configuration-driven flow.

#### Step 1.1: Define Complete Field Flow

```python
# In backend/app/services/whatsapp_conversation.py

from typing import Callable, Optional, Dict, Any

class PS2Field(str, Enum):
    """Complete PS2.pdf required fields"""
    # Personal Identity Fields (PS2 Required)
    NAME = "name"
    GUARDIAN_NAME = "guardian_name"
    DOB = "dob"
    PHONE = "phone"
    EMAIL = "email"
    GENDER = "gender"
    VILLAGE = "village"
    POST_OFFICE = "post_office"
    POLICE_STATION = "police_station"
    DISTRICT = "district"
    PIN_CODE = "pin_code"
    
    # Complaint Details
    FRAUD_TYPE = "fraud_type"
    FRAUD_SUBTYPE = "fraud_subtype"
    INCIDENT_DESCRIPTION = "incident_description"
    INCIDENT_DATE = "incident_date"
    AMOUNT_LOST = "amount_lost"
    SUSPECT_INFO = "suspect_info"
    ADDITIONAL_INFO = "additional_info"

# Ordered field collection sequence
FIELD_FLOW = [
    # Step 1: Personal Identity (PS2 Required)
    PS2Field.NAME,
    PS2Field.GUARDIAN_NAME,
    PS2Field.DOB,
    PS2Field.GENDER,
    PS2Field.PHONE,
    PS2Field.EMAIL,
    PS2Field.VILLAGE,
    PS2Field.POST_OFFICE,
    PS2Field.POLICE_STATION,
    PS2Field.DISTRICT,
    PS2Field.PIN_CODE,
    
    # Step 2: Incident Details
    PS2Field.INCIDENT_DESCRIPTION,
    PS2Field.INCIDENT_DATE,
    PS2Field.AMOUNT_LOST,
    PS2Field.SUSPECT_INFO,
    PS2Field.ADDITIONAL_INFO,
]
```

#### Step 1.2: Create Field Configuration

```python
@dataclass
class FieldConfig:
    prompt: str
    validator: Optional[Callable[[str], bool]] = None
    error_message: Optional[str] = None
    normalizer: Optional[Callable[[str], str]] = None
    buttons: Optional[List[Dict]] = None
    help_text: Optional[str] = None

# Field configuration mapping
FIELD_CONFIG: Dict[PS2Field, FieldConfig] = {
    PS2Field.NAME: FieldConfig(
        prompt="👤 Please provide your full name (as per Aadhaar):",
        validator=lambda x: len(x.strip()) >= 3,
        error_message="❌ Name must be at least 3 characters long.",
        normalizer=str.title
    ),
    
    PS2Field.GUARDIAN_NAME: FieldConfig(
        prompt="👨‍👦 Please provide your Father's / Spouse's / Guardian's Name:",
        validator=lambda x: len(x.strip()) >= 3,
        error_message="❌ Guardian name must be at least 3 characters long.",
        normalizer=str.title
    ),
    
    PS2Field.DOB: FieldConfig(
        prompt="📅 Please provide your Date of Birth (DD/MM/YYYY):",
        validator=validation_service.is_valid_dob,
        error_message="❌ Invalid date format. Please use DD/MM/YYYY (e.g., 15/08/1990)",
        help_text="Example: 15/08/1990"
    ),
    
    PS2Field.GENDER: FieldConfig(
        prompt="⚧ Please select your gender:",
        buttons=[
            {"id": "male", "title": "Male"},
            {"id": "female", "title": "Female"},
            {"id": "other", "title": "Other"}
        ]
    ),
    
    PS2Field.PHONE: FieldConfig(
        prompt="📱 Please provide your mobile number (10 digits):",
        validator=validation_service.is_valid_phone,
        error_message="❌ Invalid mobile number. Must be 10 digits starting with 6-9.",
        normalizer=validation_service.normalize_phone,
        help_text="Example: 9876543210"
    ),
    
    PS2Field.EMAIL: FieldConfig(
        prompt="📧 Please provide your email address:",
        validator=validation_service.is_valid_email,
        error_message="❌ Invalid email. Please use format: user@example.com",
        help_text="Example: yourname@example.com"
    ),
    
    PS2Field.VILLAGE: FieldConfig(
        prompt="🏘️ Please provide your Village name:",
        validator=lambda x: len(x.strip()) >= 2,
        error_message="❌ Village name must be at least 2 characters."
    ),
    
    PS2Field.POST_OFFICE: FieldConfig(
        prompt="📮 Please provide your Post Office name:",
        validator=lambda x: len(x.strip()) >= 2,
        error_message="❌ Post Office name must be at least 2 characters."
    ),
    
    PS2Field.POLICE_STATION: FieldConfig(
        prompt="🚔 Please provide your Police Station name:",
        validator=lambda x: len(x.strip()) >= 2,
        error_message="❌ Police Station name must be at least 2 characters."
    ),
    
    PS2Field.DISTRICT: FieldConfig(
        prompt="🏛️ Please provide your District name:",
        validator=lambda x: len(x.strip()) >= 2,
        error_message="❌ District name must be at least 2 characters.",
        help_text="Example: Cuttack, Khordha, Puri"
    ),
    
    PS2Field.PIN_CODE: FieldConfig(
        prompt="📍 Please provide your PIN Code (6 digits):",
        validator=validation_service.is_valid_pin,
        error_message="❌ Invalid PIN code. Must be exactly 6 digits.",
        help_text="Example: 751001"
    ),
    
    # ... Add remaining fields
}
```

### Phase 2: Update Validation Service

Add missing validators to `backend/app/services/validation.py`:

```python
def is_valid_dob(dob_str: str) -> bool:
    """Validate date of birth in DD/MM/YYYY format"""
    pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(\d{4})$')
    if not pattern.match(dob_str):
        return False
    
    # Additional validation: check if date is valid and person is at least 18
    try:
        day, month, year = map(int, dob_str.split('/'))
        dob_date = datetime(year, month, day)
        age = (datetime.now() - dob_date).days / 365.25
        return 18 <= age <= 120
    except:
        return False

def normalize_phone(phone: str) -> str:
    """Normalize phone number (remove +91, spaces, etc.)"""
    phone = re.sub(r'[^\d]', '', phone)
    if phone.startswith('91') and len(phone) == 12:
        phone = phone[2:]
    return phone

def is_valid_pin(pin: str) -> bool:
    """Validate Indian PIN code (6 digits, first digit 1-9)"""
    return bool(re.match(r'^[1-9]\d{5}$', pin))
```

### Phase 3: Refactor Collection Flow

Replace the brittle `elif` chain with a config-driven approach:

```python
async def _handle_complaint_collection(
    self, user_id: str, message_text: str, state: Dict
) -> Dict:
    """Handle step-by-step PS2 field collection using configuration"""
    current_field = state.get("current_field")
    
    if current_field is None:
        current_field = FIELD_FLOW[0]
    
    # Get current field index
    try:
        current_index = FIELD_FLOW.index(current_field)
    except ValueError:
        return self._get_default_response(user_id)
    
    # Get field configuration
    config = FIELD_CONFIG.get(current_field)
    if not config:
        return self._get_default_response(user_id)
    
    # Validate input
    if config.validator and not config.validator(message_text):
        return {
            "text": config.error_message or "❌ Invalid input. Please try again.",
            "help": config.help_text
        }
    
    # Normalize and save
    value = message_text
    if config.normalizer:
        value = config.normalizer(value)
    
    self.conversation_state.set_field(user_id, current_field, value)
    
    # Move to next field or confirmation
    if current_index + 1 < len(FIELD_FLOW):
        next_field = FIELD_FLOW[current_index + 1]
        self.conversation_state.update_state(user_id, {
            "current_field": next_field
        })
        
        next_config = FIELD_CONFIG[next_field]
        response = {"text": next_config.prompt}
        
        if next_config.buttons:
            response["buttons"] = next_config.buttons
        if next_config.help_text:
            response["help"] = next_config.help_text
        
        return response
    else:
        # All fields collected - show confirmation
        self.conversation_state.update_state(user_id, {
            "stage": ConversationStage.CONFIRMATION
        })
        return await self._show_confirmation(user_id, state)
```

### Phase 4: Update Confirmation & Ticket Creation

Update the confirmation summary to show all PS2 fields:

```python
async def _show_confirmation(self, user_id: str, state: Dict) -> Dict:
    """Show complete PS2 complaint summary"""
    data = state["data"]
    
    summary = f"""
📋 **COMPLAINT SUMMARY - PLEASE VERIFY**

👤 **Personal Details:**
• Name: {data.get(PS2Field.NAME)}
• Father/Guardian: {data.get(PS2Field.GUARDIAN_NAME)}
• Date of Birth: {data.get(PS2Field.DOB)}
• Gender: {data.get(PS2Field.GENDER)}
• Phone: {data.get(PS2Field.PHONE)}
• Email: {data.get(PS2Field.EMAIL)}

📍 **Address:**
• Village: {data.get(PS2Field.VILLAGE)}
• Post Office: {data.get(PS2Field.POST_OFFICE)}
• Police Station: {data.get(PS2Field.POLICE_STATION)}
• District: {data.get(PS2Field.DISTRICT)}
• PIN Code: {data.get(PS2Field.PIN_CODE)}

🚨 **Complaint Details:**
• Type: {data.get(PS2Field.FRAUD_TYPE)}
• Description: {data.get(PS2Field.INCIDENT_DESCRIPTION, 'N/A')[:100]}...
• Date: {data.get(PS2Field.INCIDENT_DATE)}
• Amount Lost: ₹{data.get(PS2Field.AMOUNT_LOST, '0')}

Please verify all details are correct:
"""
    
    return {
        "text": summary,
        "buttons": [
            {"id": "confirm_submit", "title": "✅ Confirm & Submit"},
            {"id": "edit_complaint", "title": "✏️ Edit Details"},
            {"id": "cancel_complaint", "title": "❌ Cancel"}
        ]
    }
```

### Phase 5: Database Schema Update

Ensure the Complaint model stores all PS2 fields:

```python
# In backend/app/models/complaint.py

class ComplaintDocument(Document):
    # PS2 Personal Identity Fields
    name: str
    guardian_name: str
    dob: str  # DD/MM/YYYY format
    phone: str
    email: EmailStr
    gender: str
    village: str
    post_office: str
    police_station: str
    district: str
    pin_code: str
    
    # Complaint fields
    fraud_type: str
    fraud_subtype: Optional[str] = None
    incident_description: str
    incident_date: str
    amount_lost: float = 0.0
    suspect_info: Optional[str] = None
    additional_info: Optional[str] = None
    
    # System fields
    ticket_id: str
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Implementation Checklist

### Critical (Must Have)
- [ ] Add missing validators to `validation.py` (DOB, PIN, normalize_phone)
- [ ] Update `ComplaintField` enum to `PS2Field` with all 11 personal fields
- [ ] Create `FIELD_FLOW` ordered list
- [ ] Create `FIELD_CONFIG` dictionary with prompts and validators
- [ ] Refactor `_handle_complaint_collection` to use config-driven approach
- [ ] Update `_show_confirmation` to display all PS2 fields
- [ ] Update `ComplaintDocument` model with all PS2 fields
- [ ] Test complete flow end-to-end

### Important (Should Have)
- [ ] Add i18n support for Odia translations of all prompts
- [ ] Implement edit functionality (allow users to go back and change fields)
- [ ] Add progress indicator (e.g., "Step 3 of 16")
- [ ] Implement data persistence to prevent loss on disconnect
- [ ] Add help command to explain fields

### Nice to Have
- [ ] Pre-populate phone number from WhatsApp ID
- [ ] Implement smart district autocomplete
- [ ] Add voice input support for Odia speakers
- [ ] Implement attachment handling for supporting documents

## Testing Plan

1. **Unit Tests** - Test each validator independently
2. **Integration Tests** - Test complete flow with mock WhatsApp messages
3. **User Acceptance Testing** - Test with real users in Odia and English
4. **Edge Cases** - Invalid inputs, long names, special characters

## Backwards Compatibility

To maintain compatibility with existing code:

```python
# Migration mapping for old field names
LEGACY_FIELD_MAP = {
    "victim_name": PS2Field.NAME,
    "victim_phone": PS2Field.PHONE,
    "victim_email": PS2Field.EMAIL,
    "location": f"{PS2Field.VILLAGE}, {PS2Field.DISTRICT}",
}

def migrate_legacy_data(old_data: Dict) -> Dict:
    """Convert old field names to new PS2 field names"""
    new_data = {}
    for old_key, value in old_data.items():
        new_key = LEGACY_FIELD_MAP.get(old_key, old_key)
        new_data[new_key] = value
    return new_data
```

## Deployment Steps

1. **Development**: Implement changes in feature branch
2. **Testing**: Test on staging with MongoDB Atlas test database
3. **Migration**: Run data migration script for existing complaints
4. **Deployment**: Deploy to production with feature flag
5. **Monitoring**: Monitor conversation completion rates
6. **Rollback Plan**: Keep old code available for quick rollback if needed

## Estimated Effort

- **Implementation**: 8-12 hours
- **Testing**: 4-6 hours
- **Documentation**: 2-3 hours
- **Total**: 14-21 hours

## Next Steps

1. Review this plan with the development team
2. Create GitHub issues for each checklist item
3. Begin Phase 1 implementation
4. Set up test MongoDB Atlas instance
5. Schedule user testing session

## References

- PS2.pdf - Original requirements document
- `backend/app/services/whatsapp_conversation.py` - Current implementation
- `backend/app/services/validation.py` - Validation utilities
- `backend/app/models/complaint.py` - Database model
