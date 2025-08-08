#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Expiration check module for the Tally Ledger Head Processor Application.
Implements a simple 6-month expiration check based on current date.
"""

from datetime import datetime, timedelta
import sys

# Set the start date (current date when implementing this feature)
START_DATE = datetime(2025, 8, 8)  # August 8, 2025
EXPIRATION_MONTHS = 6

def calculate_expiration_date():
    """Calculate the expiration date (6 months from start date)."""
    # Add 6 months to the start date
    expiration_date = START_DATE + timedelta(days=180)  # Approximately 6 months
    return expiration_date

def is_expired():
    """
    Check if the application has expired.
    
    Returns:
        bool: True if expired, False if still valid
    """
    current_date = datetime.now()
    expiration_date = calculate_expiration_date()
    
    return current_date > expiration_date

def get_days_remaining():
    """
    Get the number of days remaining before expiration.
    
    Returns:
        int: Number of days remaining (negative if expired)
    """
    current_date = datetime.now()
    expiration_date = calculate_expiration_date()
    
    days_remaining = (expiration_date - current_date).days
    return days_remaining

def get_expiration_message():
    """
    Get an appropriate expiration message based on current status.
    
    Returns:
        str: Expiration status message
    """
    if is_expired():
        return "This application has expired. Please contact the developer for an updated version."
    
    days_remaining = get_days_remaining()
    expiration_date = calculate_expiration_date()
    
    if days_remaining <= 30:
        return f"Warning: This application will expire in {days_remaining} days on {expiration_date.strftime('%B %d, %Y')}."
    
    return f"Application expires on {expiration_date.strftime('%B %d, %Y')} ({days_remaining} days remaining)."

def should_disable_functionality():
    """
    Check if the application functionality should be disabled due to expiration.
    
    Returns:
        bool: True if functionality should be disabled, False otherwise
    """
    return is_expired()

def get_expiration_status():
    """
    Get detailed expiration status information.
    
    Returns:
        dict: Dictionary containing expiration status details
    """
    return {
        'is_expired': is_expired(),
        'days_remaining': get_days_remaining(),
        'expiration_date': calculate_expiration_date(),
        'start_date': START_DATE,
        'message': get_expiration_message()
    }
