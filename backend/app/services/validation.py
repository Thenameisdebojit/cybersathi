"""
Validation Service for CyberSathi
Implements exact validation rules as per PS2.pdf requirements
"""

import re
from datetime import datetime
from typing import Optional, Tuple


class ValidationService:
    """
    Validation service with exact regex patterns from requirements.
    All patterns follow the specifications from Prompt 1.
    """
    
    # Exact regex patterns from requirements
    MOBILE_REGEX = re.compile(r'^[6-9]\d{9}$')
    EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    PIN_REGEX = re.compile(r'^[1-9][0-9]{5}$')
    DOB_REGEX = re.compile(r'^(0[1-9]|[12][0-9]|3[01])[-/]?(0[1-9]|1[012])[-/]?\d{4}$')
    TICKET_ID_REGEX = re.compile(r'^CS-\d{8}-\d{6}$')
    
    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        """
        Validate Indian mobile number.
        Pattern: ^[6-9]\\d{9}$
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not phone:
            return False
        
        clean_phone = phone.strip().replace('+91', '').replace(' ', '').replace('-', '')
        return bool(cls.MOBILE_REGEX.match(clean_phone))
    
    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        """
        Validate email address.
        Pattern: ^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False
        
        return bool(cls.EMAIL_REGEX.match(email.strip()))
    
    @classmethod
    def is_valid_pin(cls, pin: str) -> bool:
        """
        Validate Indian PIN code (6 digits, cannot start with 0).
        Pattern: ^[1-9][0-9]{5}$
        
        Args:
            pin: PIN code to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not pin:
            return False
        
        return bool(cls.PIN_REGEX.match(pin.strip()))
    
    @classmethod
    def is_valid_dob(cls, dob: str) -> Tuple[bool, Optional[str]]:
        """
        Validate date of birth.
        Accepts: DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD
        Pattern: ^(0[1-9]|[12][0-9]|3[01])[-/]?(0[1-9]|1[012])[-/]?\\d{4}$
        
        Args:
            dob: Date of birth string
            
        Returns:
            Tuple of (is_valid, normalized_date)
        """
        if not dob:
            return False, None
        
        dob = dob.strip()
        
        if cls.DOB_REGEX.match(dob):
            try:
                normalized = cls._normalize_date(dob)
                return True, normalized
            except ValueError:
                return False, None
        
        if re.match(r'^\d{4}[-/]\d{2}[-/]\d{2}$', dob):
            try:
                dt = datetime.strptime(dob.replace('/', '-'), '%Y-%m-%d')
                return True, dt.strftime('%d-%m-%Y')
            except ValueError:
                return False, None
        
        return False, None
    
    @classmethod
    def is_valid_ticket_id(cls, ticket_id: str) -> bool:
        """
        Validate ticket ID format.
        Pattern: CS-YYYYMMDD-XXXXXX
        
        Args:
            ticket_id: Ticket ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not ticket_id:
            return False
        
        return bool(cls.TICKET_ID_REGEX.match(ticket_id.strip()))
    
    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate name (non-empty, reasonable length).
        
        Args:
            name: Name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Name is required"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        
        if len(name.strip()) > 100:
            return False, "Name must be less than 100 characters"
        
        return True, None
    
    @classmethod
    def validate_description(cls, description: str, min_length: int = 10) -> Tuple[bool, Optional[str]]:
        """
        Validate complaint description.
        
        Args:
            description: Description to validate
            min_length: Minimum required length
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not description or not description.strip():
            return False, "Description is required"
        
        if len(description.strip()) < min_length:
            return False, f"Description must be at least {min_length} characters"
        
        return True, None
    
    @classmethod
    def validate_gender(cls, gender: str) -> Tuple[bool, Optional[str]]:
        """
        Validate gender field.
        
        Args:
            gender: Gender value
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_genders = ['male', 'female', 'other', 'prefer_not_to_say']
        
        if not gender:
            return False, "Gender is required"
        
        if gender.lower() not in valid_genders:
            return False, f"Gender must be one of: {', '.join(valid_genders)}"
        
        return True, None
    
    @classmethod
    def _normalize_date(cls, date_str: str) -> str:
        """
        Normalize date to DD-MM-YYYY format.
        
        Args:
            date_str: Date string in various formats
            
        Returns:
            Normalized date string in DD-MM-YYYY format
        """
        date_str = date_str.replace('/', '-')
        
        for fmt in ['%d-%m-%Y', '%d%m%Y']:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%d-%m-%Y')
            except ValueError:
                continue
        
        raise ValueError(f"Could not parse date: {date_str}")


validation_service = ValidationService()
