"""
Conversation model for the stateless chat API.
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class ConversationBase(SQLModel):
    user_id: str
    # Additional fields can be added here as needed


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a unique chat thread between a user and the assistant.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(description="Identifier for the user who owns this conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when conversation was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when conversation was last updated")


class ConversationCreate(ConversationBase):
    """
    Model for creating a new conversation.
    """
    user_id: str
    pass


class ConversationRead(ConversationBase):
    """
    Model for reading conversation data.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime