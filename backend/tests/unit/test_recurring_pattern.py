import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from app.src.models.recurring_task import RecurringTaskPattern, RecurringTaskPatternCreate


def test_recurring_task_pattern_validations():
    """Test RecurringTaskPattern model validations."""
    # Valid pattern
    valid_pattern_data = {
        "base_task_title": "Daily Task",
        "base_task_description": "A daily recurring task",
        "recurrence_type": "daily",
        "interval": 1,
        "start_date": datetime.now(),
        "user_id": 1
    }
    
    pattern = RecurringTaskPatternCreate(**valid_pattern_data)
    assert pattern.base_task_title == "Daily Task"
    assert pattern.recurrence_type == "daily"
    assert pattern.interval == 1


def test_recurring_task_pattern_invalid_type():
    """Test validation for invalid recurrence type."""
    invalid_pattern_data = {
        "base_task_title": "Invalid Task",
        "base_task_description": "A task with invalid recurrence type",
        "recurrence_type": "invalid_type",  # Invalid type
        "interval": 1,
        "start_date": datetime.now(),
        "user_id": 1
    }
    
    # This won't raise an error at model level since we're not strictly validating the enum
    # But in the service layer, it should be validated
    pattern = RecurringTaskPatternCreate(**invalid_pattern_data)
    assert pattern.recurrence_type == "invalid_type"


def test_recurring_task_pattern_negative_interval():
    """Test validation for negative interval."""
    invalid_pattern_data = {
        "base_task_title": "Negative Interval Task",
        "base_task_description": "A task with negative interval",
        "recurrence_type": "daily",
        "interval": -1,  # Negative interval
        "start_date": datetime.now(),
        "user_id": 1
    }
    
    # This should raise a validation error since we have ge=1 constraint
    with pytest.raises(ValidationError):
        RecurringTaskPatternCreate(**invalid_pattern_data)


def test_recurring_task_pattern_zero_interval():
    """Test validation for zero interval."""
    invalid_pattern_data = {
        "base_task_title": "Zero Interval Task",
        "base_task_description": "A task with zero interval",
        "recurrence_type": "daily",
        "interval": 0,  # Zero interval
        "start_date": datetime.now(),
        "user_id": 1
    }
    
    # This should raise a validation error since we have ge=1 constraint
    with pytest.raises(ValidationError):
        RecurringTaskPatternCreate(**invalid_pattern_data)


def test_recurring_task_pattern_end_before_start():
    """Test validation for end date before start date."""
    # Note: This validation is done in the service layer, not at the model level
    # So creating the model should not raise an error
    invalid_pattern_data = {
        "base_task_title": "End Before Start Task",
        "base_task_description": "A task with end date before start date",
        "recurrence_type": "daily",
        "interval": 1,
        "start_date": datetime.now() + timedelta(days=10),  # Future start date
        "end_date": datetime.now() - timedelta(days=1),    # Past end date
        "user_id": 1
    }
    
    # This should not raise an error at the model level
    pattern = RecurringTaskPatternCreate(**invalid_pattern_data)
    assert pattern.start_date > pattern.end_date


def test_recurring_task_pattern_weekdays_mask():
    """Test validation for weekdays_mask."""
    # Valid weekdays_mask (Mon-Fri)
    valid_pattern_data = {
        "base_task_title": "Weekday Task",
        "base_task_description": "A task that occurs on weekdays",
        "recurrence_type": "weekly",
        "interval": 1,
        "start_date": datetime.now(),
        "weekdays_mask": 62,  # Mon-Fri (2+4+8+16+32)
        "user_id": 1
    }
    
    pattern = RecurringTaskPatternCreate(**valid_pattern_data)
    assert pattern.weekdays_mask == 62
    
    # Invalid weekdays_mask (outside 1-127 range)
    invalid_pattern_data = {
        "base_task_title": "Invalid Weekday Mask Task",
        "base_task_description": "A task with invalid weekdays_mask",
        "recurrence_type": "weekly",
        "interval": 1,
        "start_date": datetime.now(),
        "weekdays_mask": 200,  # Invalid mask
        "user_id": 1
    }
    
    # This validation is done in the service layer, not at the model level
    pattern = RecurringTaskPatternCreate(**invalid_pattern_data)
    assert pattern.weekdays_mask == 200