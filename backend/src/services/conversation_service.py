"""
Service layer for conversation-related operations.
"""
from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole


class ConversationService:
    """
    Service class for handling conversation operations.
    """

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Create a new conversation for the given user.
        """
        conversation = Conversation(
            user_id=user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """
        Retrieve a conversation by its ID.
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversation_with_messages(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """
        Retrieve a conversation with its associated messages.
        """
        # This will be implemented when we need to fetch conversation history
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversation_messages_ordered(session: Session, conversation_id: UUID) -> List[Message]:
        """
        Retrieve all messages for a conversation ordered by timestamp.

        Args:
            session: Database session
            conversation_id: ID of the conversation

        Returns:
            List of messages ordered by timestamp
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation_timestamp(session: Session, conversation: Conversation) -> Conversation:
        """
        Update the updated_at timestamp of a conversation.
        """
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation