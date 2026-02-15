from datetime import datetime, timezone, timedelta
import pytz
from typing import Optional


def convert_utc_to_user_timezone(utc_dt: datetime, user_timezone: str) -> datetime:
    """
    Convert a UTC datetime to the user's local timezone.
    
    Args:
        utc_dt: The datetime in UTC
        user_timezone: The user's timezone (e.g., 'America/New_York')
        
    Returns:
        The datetime converted to the user's timezone
    """
    if utc_dt.tzinfo is None:
        # If the datetime is naive, assume it's UTC
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    
    user_tz = pytz.timezone(user_timezone)
    return utc_dt.astimezone(user_tz)


def convert_user_timezone_to_utc(user_dt: datetime, user_timezone: str) -> datetime:
    """
    Convert a user's local datetime to UTC.
    
    Args:
        user_dt: The datetime in the user's timezone
        user_timezone: The user's timezone (e.g., 'America/New_York')
        
    Returns:
        The datetime converted to UTC
    """
    user_tz = pytz.timezone(user_timezone)
    if user_dt.tzinfo is None:
        # If the datetime is naive, localize it to the user's timezone
        user_dt = user_tz.localize(user_dt)
    else:
        # If it already has timezone info, convert it to the user's timezone
        user_dt = user_dt.astimezone(user_tz)
    
    return user_dt.astimezone(timezone.utc)


def get_current_time_in_timezone(user_timezone: str) -> datetime:
    """
    Get the current time in the user's timezone.
    
    Args:
        user_timezone: The user's timezone (e.g., 'America/New_York')
        
    Returns:
        The current datetime in the user's timezone
    """
    user_tz = pytz.timezone(user_timezone)
    return datetime.now(user_tz)


def add_timezone_offset(dt: datetime, offset_hours: int) -> datetime:
    """
    Add a timezone offset to a datetime.
    
    Args:
        dt: The datetime to add offset to
        offset_hours: The offset in hours (positive or negative)
        
    Returns:
        The datetime with the offset applied
    """
    offset = timedelta(hours=offset_hours)
    return dt + offset


def validate_timezone(timezone_str: str) -> bool:
    """
    Validate if a timezone string is valid.
    
    Args:
        timezone_str: The timezone string to validate
        
    Returns:
        True if the timezone is valid, False otherwise
    """
    try:
        pytz.timezone(timezone_str)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False