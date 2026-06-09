
import re
from datetime import datetime

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class Validator:
    """Utility class for input validation."""
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """
        Validate date format.
        
        Args:
            date_str (str): Date string to validate
            format (str): Expected date format
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_string(value, min_length=1, max_length=255):
        """
        Validate string length.
        
        Args:
            value: Value to validate
            min_length (int): Minimum length
            max_length (int): Maximum length
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(value, str):
            return False
        return min_length <= len(value.strip()) <= max_length
    
    @staticmethod
    def validate_positive_int(value):
        """
        Validate positive integer (> 0).
        
        Args:
            value: Value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            return isinstance(value, int) and value > 0
        except:
            return False
    
    @staticmethod
    def validate_non_negative_int(value):
        """
        Validate non-negative integer (>= 0).
        
        Args:
            value: Value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            return isinstance(value, int) and value >= 0
        except:
            return False
