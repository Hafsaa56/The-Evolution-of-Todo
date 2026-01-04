import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re

def validate_email(email: str) -> bool:
    """
    Validate an email address format.

    Args:
        email: The email address to validate

    Returns:
        bool: True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """
    Validate a password based on security requirements.
    Password must be at least 8 characters long and contain at least one uppercase,
    one lowercase, one number, and one special character.

    Args:
        password: The password to validate

    Returns:
        bool: True if password meets requirements, False otherwise
    """
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'\d', password):
        return False

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title.

    Args:
        title: The task title to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title cannot be empty"

    if len(title.strip()) < 1:
        return False, "Title must be at least 1 character long"

    if len(title) > 200:
        return False, "Title must be less than 200 characters"

    return True, ""

def validate_description(description: str | None) -> tuple[bool, str]:
    """
    Validate task description (optional field).

    Args:
        description: The task description to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if description is None:
        return True, ""

    if len(description) > 2000:
        return False, "Description must be less than 2000 characters"

    return True, ""

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing potentially dangerous characters.

    Args:
        input_str: The input string to sanitize

    Returns:
        str: Sanitized string
    """
    # Remove null bytes and control characters (except newlines/tabs)
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', input_str)
    # Strip leading/trailing whitespace
    return sanitized.strip()