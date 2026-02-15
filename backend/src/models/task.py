from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Table, ForeignKey, DateTime
from typing import Optional, List
from datetime import datetime
import uuid


# Temporarily removing many-to-many relationship to fix import error
# Association table for many-to-many relationship between Task and Tag
# task_tag_association = Table(
#     "task_tag",
#     SQLModel.metadata,
#     Column("task_id", String, ForeignKey("task.id"), primary_key=True),
#     Column("tag_id", String, ForeignKey("tag.id"), primary_key=True),
# )


class TaskBase(SQLModel):
    """Base class for Task with shared attributes."""

    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="todo", sa_column=Column(String, nullable=False))  # ['todo', 'in_progress', 'done']
    priority: str = Field(default="medium", sa_column=Column(String, nullable=False))  # ['low', 'medium', 'high']
    user_id: int = Field(default=1, foreign_key="user.id")  # Foreign key linking to User, defaults to user 1
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    reminder_offset: Optional[int] = Field(default=None)  # Minutes before due_date to send reminder
    recurring_pattern_id: Optional[str] = Field(default=None, foreign_key="recurringtaskpattern.id")


class Task(TaskBase, table=True):
    """Task model representing a specific work item that can be created, updated, or managed through natural language commands."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationship to tags - temporarily removed to fix import error
    # tags: List["Tag"] = Relationship(back_populates="tasks", link_model=task_tag_association)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'created_at' not in kwargs or kwargs['created_at'] is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    tags: Optional[List[str]] = []  # List of tag names to associate with the task
    recurring_pattern: Optional[dict] = None  # Recurring pattern definition


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)  # ['todo', 'in_progress', 'done']
    priority: Optional[str] = Field(default=None)  # ['low', 'medium', 'high']
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))
    reminder_offset: Optional[int] = Field(default=None)  # Minutes before due_date to send reminder
    tags: Optional[List[str]] = None  # List of tag names to associate with the task


class TaskRead(TaskBase):
    """Schema for reading task data."""

    id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    tags: List["TagRead"] = []


class TaskStatusUpdate(SQLModel):
    """Schema for updating task status."""

    completed: bool


class TagBase(SQLModel):
    """Base class for Tag with shared attributes."""

    name: str = Field(min_length=1, max_length=50)
    user_id: int = Field(foreign_key="user.id")


class Tag(TagBase, table=True):
    """Tag model representing a label that can be associated with multiple tasks."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks - temporarily removed to fix import error
    # tasks: List[Task] = Relationship(back_populates="tags", link_model=task_tag_association)


class TagCreate(TagBase):
    """Schema for creating a new tag."""
    pass


class TagRead(TagBase):
    """Schema for reading tag data."""

    id: str
    created_at: datetime
    usage_count: Optional[int] = 0  # Count of how many tasks use this tag


class TagUpdate(SQLModel):
    """Schema for updating an existing tag."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=50)