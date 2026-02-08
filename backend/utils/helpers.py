"""
Helper functions
"""

import re


def format_number(num):
    """
    Format number with thousand separators
    
    Parameters:
    -----------
    num : int or float
        Number to format
        
    Returns:
    --------
    str
        Formatted number string
    """
    if num is None:
        return "0"
    return f"{num:,}"


def validate_email(email):
    """
    Validate email format
    
    Parameters:
    -----------
    email : str
        Email address to validate
        
    Returns:
    --------
    bool
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_text(text):
    """
    Clean text for display
    
    Parameters:
    -----------
    text : str
        Text to clean
        
    Returns:
    --------
    str
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()