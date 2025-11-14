"""
Ticket Generation Service for CyberSathi
Generates unique ticket IDs in format: CS-YYYYMMDD-XXXXXX
"""

import random
from datetime import datetime
from typing import Optional


class TicketService:
    """
    Service for generating unique ticket IDs.
    Format: CS-YYYYMMDD-XXXXXX
    Where:
        CS = CyberSathi prefix
        YYYYMMDD = Current date
        XXXXXX = 6-digit random number (100000-999999)
    """
    
    @staticmethod
    def generate_ticket() -> str:
        """
        Generate a unique ticket ID.
        
        Format: CS-YYYYMMDD-XXXXXX
        Example: CS-20241114-234567
        
        Returns:
            Generated ticket ID string
        """
        ts = datetime.now()
        ymd = ts.strftime('%Y%m%d')
        
        suffix = random.randint(100000, 999999)
        
        ticket_id = f"CS-{ymd}-{suffix}"
        
        return ticket_id
    
    @staticmethod
    def generate_reference_id(length: int = 8) -> str:
        """
        Generate a shorter reference ID for backward compatibility.
        
        Format: CS-XXXXXXXX (alphanumeric)
        Example: CS-A1B2C3D4
        
        Args:
            length: Length of the alphanumeric suffix (default: 8)
            
        Returns:
            Generated reference ID string
        """
        import string
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choices(chars, k=length))
        
        return f"CS-{suffix}"
    
    @staticmethod
    def validate_ticket_format(ticket_id: str) -> bool:
        """
        Validate if ticket ID matches the expected format.
        
        Args:
            ticket_id: Ticket ID to validate
            
        Returns:
            True if valid format, False otherwise
        """
        import re
        pattern = r'^CS-\d{8}-\d{6}$'
        return bool(re.match(pattern, ticket_id))
    
    @staticmethod
    def extract_date_from_ticket(ticket_id: str) -> Optional[datetime]:
        """
        Extract the date component from a ticket ID.
        
        Args:
            ticket_id: Ticket ID in format CS-YYYYMMDD-XXXXXX
            
        Returns:
            datetime object or None if invalid
        """
        try:
            if not ticket_id.startswith('CS-'):
                return None
            
            parts = ticket_id.split('-')
            if len(parts) != 3:
                return None
            
            date_str = parts[1]
            if len(date_str) != 8:
                return None
            
            return datetime.strptime(date_str, '%Y%m%d')
        
        except (ValueError, IndexError):
            return None


ticket_service = TicketService()
