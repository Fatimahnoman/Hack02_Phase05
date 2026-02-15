from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime
from typing import Optional
from datetime import datetime
import uuid


class RecurringTaskPatternBase(SQLModel):
    """Base class for RecurringTaskPattern with shared attributes."""

    base_task_title: str = Field(min_length=1, max_length=255)
    base_task_description: Optional[str] = Field(default=None)
    recurrence_type: str = Field(sa_column=Column(String, nullable=False))  # ['daily', 'weekly', 'monthly', 'custom']
    interval: int = Field(default=1, ge=1)  # Interval between recurrences (e.g., every 2 weeks)
    start_date: datetime = Field(sa_column=Column(DateTime, nullable=False))  # When the recurrence starts
    end_date: Optional[datetime] = Field(default=None)  # When the recurrence ends (null for indefinite)
    weekdays_mask: Optional[int] = Field(default=None)  # Bitmask for days of week (for weekly patterns)
    user_id: int = Field(foreign_key="user.id")  # Owner of the pattern


class RecurringTaskPattern(RecurringTaskPatternBase, table=True):
    """RecurringTaskPattern model defining a pattern for recurring tasks."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at = datetime.utcnow()


class RecurringTaskPatternCreate(RecurringTaskPatternBase):
    """Schema for creating a new recurring task pattern."""
    recurrence_type: str
    interval: int
    start_date: datetime


class RecurringTaskPatternUpdate(SQLModel):
    """Schema for updating an existing recurring task pattern."""

    base_task_title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    base_task_description: Optional[str] = Field(default=None)
    recurrence_type: Optional[str] = Field(default=None)  # ['daily', 'weekly', 'monthly', 'custom']
    interval: Optional[int] = Field(default=None, ge=1)
    end_date: Optional[datetime] = Field(default=None)
    weekdays_mask: Optional[int] = Field(default=None)


class RecurringTaskPatternRead(RecurringTaskPatternBase):
    """Schema for reading recurring task pattern data."""

    id: str
    created_at: datetime
    updated_at: datetime