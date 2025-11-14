"""
PII Masking Utility for CyberSathi
Implements data privacy and security best practices
"""

import re
from typing import Optional


class PIIMaskingService:
    """
    Service for masking Personally Identifiable Information (PII).
    Used for logging, display, and compliance with data protection regulations.
    """
    
    @staticmethod
    def mask_phone(phone: str, visible_digits: int = 4) -> str:
        """
        Mask phone number, showing only last N digits.
        
        Example: 9876543210 -> ******3210
        
        Args:
            phone: Phone number to mask
            visible_digits: Number of digits to show at the end (default: 4)
            
        Returns:
            Masked phone number
        """
        if not phone:
            return ""
        
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if len(clean_phone) <= visible_digits:
            return clean_phone
        
        masked_count = len(clean_phone) - visible_digits
        masked = ('*' * masked_count) + clean_phone[-visible_digits:]
        
        return masked
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email address, showing first 2 chars and domain.
        
        Example: john.doe@gmail.com -> jo*****@gmail.com
        
        Args:
            email: Email address to mask
            
        Returns:
            Masked email address
        """
        if not email or '@' not in email:
            return ""
        
        try:
            local, domain = email.split('@', 1)
            
            if len(local) <= 2:
                masked_local = local[0] + '*'
            else:
                masked_local = local[:2] + '*' * (len(local) - 2)
            
            return f"{masked_local}@{domain}"
        
        except (ValueError, IndexError):
            return email
    
    @staticmethod
    def mask_aadhaar(aadhaar: str) -> str:
        """
        Mask Aadhaar number, showing only last 4 digits.
        
        Example: 1234-5678-9012 -> ****-****-9012
        
        Args:
            aadhaar: Aadhaar number to mask
            
        Returns:
            Masked Aadhaar number
        """
        if not aadhaar:
            return ""
        
        clean_aadhaar = re.sub(r'[^\d]', '', aadhaar)
        
        if len(clean_aadhaar) != 12:
            return aadhaar
        
        return f"****-****-{clean_aadhaar[-4:]}"
    
    @staticmethod
    def mask_bank_account(account: str, visible_digits: int = 4) -> str:
        """
        Mask bank account number.
        
        Example: 123456789012 -> ********9012
        
        Args:
            account: Bank account number to mask
            visible_digits: Number of digits to show at the end
            
        Returns:
            Masked account number
        """
        if not account:
            return ""
        
        clean_account = re.sub(r'[^\d]', '', account)
        
        if len(clean_account) <= visible_digits:
            return clean_account
        
        masked_count = len(clean_account) - visible_digits
        return ('*' * masked_count) + clean_account[-visible_digits:]
    
    @staticmethod
    def mask_name(name: str, show_first: bool = True) -> str:
        """
        Mask name, showing only first name or initials.
        
        Example: John Michael Doe -> John M. D.
        
        Args:
            name: Full name to mask
            show_first: Whether to show first name fully
            
        Returns:
            Masked name
        """
        if not name:
            return ""
        
        parts = name.strip().split()
        
        if not parts:
            return ""
        
        if len(parts) == 1:
            return parts[0] if show_first else parts[0][0] + '.'
        
        if show_first:
            result = [parts[0]]
            result.extend([p[0] + '.' for p in parts[1:]])
        else:
            result = [p[0] + '.' for p in parts]
        
        return ' '.join(result)
    
    @staticmethod
    def mask_for_logging(text: str) -> str:
        """
        Automatically detect and mask PII in text for logging.
        
        Masks:
        - Phone numbers
        - Email addresses
        - Aadhaar-like patterns
        
        Args:
            text: Text to sanitize
            
        Returns:
            Text with PII masked
        """
        if not text:
            return ""
        
        result = text
        
        phone_pattern = r'(?:\+91[-\s]?)?[6-9]\d{9}'
        result = re.sub(phone_pattern, '[PHONE_MASKED]', result)
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        result = re.sub(email_pattern, '[EMAIL_MASKED]', result)
        
        aadhaar_pattern = r'\d{4}[-\s]?\d{4}[-\s]?\d{4}'
        result = re.sub(aadhaar_pattern, '[AADHAAR_MASKED]', result)
        
        return result
    
    @staticmethod
    def get_masked_complaint_data(complaint_data: dict) -> dict:
        """
        Return a copy of complaint data with PII fields masked.
        Safe for logging and display in non-secure contexts.
        
        Args:
            complaint_data: Original complaint dictionary
            
        Returns:
            Dictionary with masked PII fields
        """
        masked = complaint_data.copy()
        
        if 'phone' in masked and masked['phone']:
            masked['phone'] = PIIMaskingService.mask_phone(masked['phone'])
        
        if 'email' in masked and masked['email']:
            masked['email'] = PIIMaskingService.mask_email(masked['email'])
        
        if 'bank_account' in masked and masked['bank_account']:
            masked['bank_account'] = PIIMaskingService.mask_bank_account(masked['bank_account'])
        
        if 'aadhaar' in masked and masked['aadhaar']:
            masked['aadhaar'] = PIIMaskingService.mask_aadhaar(masked['aadhaar'])
        
        return masked


pii_masking = PIIMaskingService()
