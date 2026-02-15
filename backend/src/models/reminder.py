from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime
from typing import Optional
from datetime import datetime
import uuid


class ReminderBase(SQLModel):
    """Base class for Reminder with shared attributes."""

    task_id: str = Field(foreign_key="task.id", unique=True)  # Associated task
    due_datetime: datetime = Field(sa_column=Column(DateTime, nullable=False))  # When the reminder is due
    reminder_datetime: datetime = Field(sa_column=Column(DateTime, nullable=False))  # When the reminder should be sent
    sent: bool = Field(default=False)  # Whether the reminder has been sent
    snoozed_until: Optional[datetime] = Field(default=None)  # When the reminder is snoozed until
    dismissed: bool = Field(default=False)  # Whether the reminder has been dismissed


class Reminder(ReminderBase, table=True):
    """Reminder model managing reminder settings and status for tasks."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at = datetime.utcnow()


class ReminderCreate(ReminderBase):
    """Schema for creating a new reminder."""
    task_id: str
    due_datetime: datetime
    reminder_datetime: datetime


class ReminderUpdate(SQLModel):
    """Schema for updating an existing reminder."""

    sent: Optional[bool] = Field(default=None)
    snoozed_until: Optional[datetime] = Field(default=None)
    dismissed: Optional[bool] = Field(default=None)


class ReminderRead(ReminderBase):
    """Schema for reading reminder data."""

    id: str
    created_at: datetime
    updated_at: datetime