"""
Message model for the stateless chat API.
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class MessageRole(str, Enum):
    """
    Enum for message roles (sender types).
    """
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    conversation_id: UUID
    role: MessageRole
    content: str
    # Additional fields can be added here as needed


class Message(MessageBase, table=True):
    """
    Message model containing the content of a communication, the role (user/assistant),
    timestamp, and association with a conversation.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(description="Foreign key linking to Conversation")
    role: MessageRole = Field(sa_column_kwargs={"name": "role"}, description="Indicates sender type: user or assistant")
    content: str = Field(description="The actual message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the message was created")


class MessageCreate(MessageBase):
    """
    Model for creating a new message.
    """
    conversation_id: UUID
    role: MessageRole
    content: str


class MessageRead(MessageBase):
    """
    Model for reading message data.
    """
    id: UUID
    timestamp: datetime