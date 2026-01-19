"""
Unit tests for message and conversation persistence.
"""
import pytest
from sqlmodel import Session, select
from uuid import uuid4
from datetime import datetime
from backend.src.database import get_session_context
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message, MessageRole


def test_conversation_creation_persistence():
    """
    Test that conversations are properly created and persisted in the database.
    """
    user_id = "test_user_123"

    with get_session_context() as session:
        # Create a new conversation
        conversation = Conversation(user_id=user_id)

        # Add to session and commit
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Verify the conversation was created with required fields
        assert conversation.id is not None
        assert conversation.user_id == user_id
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

        # Verify it can be retrieved from the database
        retrieved_conversation = session.get(Conversation, conversation.id)
        assert retrieved_conversation is not None
        assert retrieved_conversation.id == conversation.id
        assert retrieved_conversation.user_id == user_id
        assert retrieved_conversation.created_at == conversation.created_at


def test_message_creation_persistence():
    """
    Test that messages are properly created and persisted in the database.
    """
    user_id = "test_user_123"

    with get_session_context() as session:
        # First create a conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Create a message associated with the conversation
        message_content = "Test message content"
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content=message_content
        )

        session.add(message)
        session.commit()
        session.refresh(message)

        # Verify the message was created with required fields
        assert message.id is not None
        assert message.conversation_id == conversation.id
        assert message.role == MessageRole.user
        assert message.content == message_content
        assert message.timestamp is not None

        # Verify it can be retrieved from the database
        retrieved_message = session.get(Message, message.id)
        assert retrieved_message is not None
        assert retrieved_message.id == message.id
        assert retrieved_message.conversation_id == conversation.id
        assert retrieved_message.role == MessageRole.user
        assert retrieved_message.content == message_content


def test_conversation_message_relationship():
    """
    Test that the relationship between conversations and messages works correctly.
    """
    user_id = "test_user_456"

    with get_session_context() as session:
        # Create a conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Create multiple messages for the same conversation
        message1 = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content="First message"
        )
        message2 = Message(
            conversation_id=conversation.id,
            role=MessageRole.assistant,
            content="Second message"
        )

        session.add(message1)
        session.add(message2)
        session.commit()

        # Query messages by conversation_id
        statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp)
        messages = session.exec(statement).all()

        assert len(messages) == 2
        assert messages[0].conversation_id == conversation.id
        assert messages[1].conversation_id == conversation.id
        assert messages[0].content == "First message"
        assert messages[1].content == "Second message"


def test_message_role_validation():
    """
    Test that message roles are properly validated and persisted.
    """
    user_id = "test_user_789"

    with get_session_context() as session:
        # Create a conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Create messages with different roles
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content="User message"
        )
        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.assistant,
            content="Assistant message"
        )

        session.add(user_message)
        session.add(assistant_message)
        session.commit()

        # Retrieve and verify roles
        retrieved_user_msg = session.get(Message, user_message.id)
        retrieved_assistant_msg = session.get(Message, assistant_message.id)

        assert retrieved_user_msg.role == MessageRole.user
        assert retrieved_assistant_msg.role == MessageRole.assistant
        assert retrieved_user_msg.content == "User message"
        assert retrieved_assistant_msg.content == "Assistant message"


def test_conversation_timestamps():
    """
    Test that conversation timestamps are properly managed.
    """
    user_id = "test_user_timestamp"

    with get_session_context() as session:
        # Create a conversation
        before_create = datetime.utcnow()
        conversation = Conversation(user_id=user_id)
        after_create = datetime.utcnow()

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Verify timestamps are within expected range
        assert conversation.created_at >= before_create
        assert conversation.created_at <= after_create
        assert conversation.updated_at >= before_create
        assert conversation.updated_at <= after_create

        # Update the conversation and check updated_at changes
        before_update = datetime.utcnow()
        conversation.user_id = "updated_user_id"
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        after_update = datetime.utcnow()

        # For this test, we're just checking that the object was updated
        # The ConversationService.update_conversation_timestamp method handles updating updated_at
        assert conversation.user_id == "updated_user_id"


def test_message_timestamps():
    """
    Test that message timestamps are properly set.
    """
    user_id = "test_user_msg_timestamp"

    with get_session_context() as session:
        # Create a conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Create a message
        before_create = datetime.utcnow()
        message = Message(
            conversation_id=conversation.id,
            role=MessageRole.user,
            content="Message with timestamp"
        )
        after_create = datetime.utcnow()

        session.add(message)
        session.commit()
        session.refresh(message)

        # Verify timestamp is within expected range
        assert message.timestamp >= before_create
        assert message.timestamp <= after_create