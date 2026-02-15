from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Enumeration of possible event types."""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    REMINDER_SCHEDULED = "reminder.scheduled"
    REMINDER_SENT = "reminder.sent"
    RECURRING_INSTANCE_CREATED = "recurring.instance.created"


class TaskEventData(BaseModel):
    """Data structure for task-related events."""
    task_id: str
    user_id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    tags: Optional[list] = []
    reminder_offset: Optional[int] = None


class ReminderEventData(BaseModel):
    """Data structure for reminder-related events."""
    reminder_id: str
    task_id: str
    due_datetime: datetime
    reminder_datetime: datetime
    sent: bool
    snoozed_until: Optional[datetime] = None
    dismissed: bool
    created_at: datetime
    updated_at: datetime


class RecurringInstanceEventData(BaseModel):
    """Data structure for recurring task instance events."""
    pattern_id: str
    new_task_id: str
    user_id: int
    title: str
    description: Optional[str] = None
    created_at: datetime


class EventSchema(BaseModel):
    """Base schema for all events."""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    source: str = "todo-backend"
    correlation_id: Optional[str] = None