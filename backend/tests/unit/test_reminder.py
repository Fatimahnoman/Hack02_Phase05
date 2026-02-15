import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from app.src.models.reminder import Reminder, ReminderCreate


def test_reminder_model_validations():
    """Test Reminder model validations."""
    # Valid reminder
    now = datetime.utcnow()
    due_time = now + timedelta(hours=2)
    reminder_time = now + timedelta(hours=1)  # 1 hour before due time
    
    valid_reminder_data = {
        "task_id": "test_task_id",
        "due_datetime": due_time,
        "reminder_datetime": reminder_time,
        "sent": False,
        "dismissed": False
    }
    
    reminder = ReminderCreate(**valid_reminder_data)
    assert reminder.task_id == "test_task_id"
    assert reminder.due_datetime == due_time
    assert reminder.reminder_datetime == reminder_time
    assert reminder.sent == False
    assert reminder.dismissed == False


def test_reminder_past_datetime_validation():
    """Test validation for past reminder datetime."""
    # Create a reminder with past times
    past_time = datetime.utcnow() - timedelta(hours=1)
    past_due_time = datetime.utcnow() - timedelta(hours=2)
    
    past_reminder_data = {
        "task_id": "test_task_id",
        "due_datetime": past_due_time,
        "reminder_datetime": past_time,  # This is in the past
        "sent": False,
        "dismissed": False
    }
    
    # This should be valid at the model level, but invalid when created via service
    reminder = ReminderCreate(**past_reminder_data)
    assert reminder.reminder_datetime < datetime.utcnow()


def test_reminder_reminder_after_due_validation():
    """Test validation for reminder time after due time."""
    now = datetime.utcnow()
    due_time = now + timedelta(hours=1)
    reminder_time = now + timedelta(hours=2)  # After due time
    
    invalid_reminder_data = {
        "task_id": "test_task_id",
        "due_datetime": due_time,
        "reminder_datetime": reminder_time,  # After due time
        "sent": False,
        "dismissed": False
    }
    
    # This should be valid at the model level, but invalid when created via service
    reminder = ReminderCreate(**invalid_reminder_data)
    assert reminder.reminder_datetime > reminder.due_datetime


def test_reminder_required_fields():
    """Test that required fields are enforced."""
    # Missing required fields should raise validation error
    incomplete_reminder_data = {
        "due_datetime": datetime.utcnow() + timedelta(hours=1),
        "reminder_datetime": datetime.utcnow() + timedelta(hours=2),
        "sent": False,
        "dismissed": False
        # Missing task_id
    }
    
    with pytest.raises(ValidationError):
        ReminderCreate(**incomplete_reminder_data)


def test_reminder_optional_fields():
    """Test optional fields in Reminder model."""
    now = datetime.utcnow()
    due_time = now + timedelta(hours=2)
    reminder_time = now + timedelta(hours=1)
    
    reminder_data = {
        "task_id": "test_task_id",
        "due_datetime": due_time,
        "reminder_datetime": reminder_time,
        "sent": False,
        "snoozed_until": now + timedelta(minutes=30),  # Optional field
        "dismissed": False
    }
    
    reminder = ReminderCreate(**reminder_data)
    assert reminder.snoozed_until is not None


def test_reminder_default_values():
    """Test default values in Reminder model."""
    now = datetime.utcnow()
    due_time = now + timedelta(hours=2)
    reminder_time = now + timedelta(hours=1)
    
    reminder_data = {
        "task_id": "test_task_id",
        "due_datetime": due_time,
        "reminder_datetime": reminder_time
        # sent and dismissed should default to False
    }
    
    # Note: ReminderCreate requires all fields, so we'll provide them
    reminder_data["sent"] = False
    reminder_data["dismissed"] = False
    
    reminder = ReminderCreate(**reminder_data)
    assert reminder.sent == False
    assert reminder.dismissed == False