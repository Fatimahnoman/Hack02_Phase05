"""
Integration tests for server restart conversation continuity.
This test verifies that conversations survive server restarts by persisting in the database.
"""
import pytest
from backend.src.database import get_session_context
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message, MessageRole
from uuid import uuid4


def test_conversation_persists_after_simulated_restart():
    """
    Test that conversations and messages persist in the database after a simulated server restart.
    This simulates the stateless nature where all data is stored in the database.
    """
    user_id = "test_user_123"
    conversation_id = str(uuid4())

    # Simulate creating a conversation and messages in the database
    with get_session_context() as session:
        # Create a conversation
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id
        )
        session.add(conversation)
        session.commit()

        # Add some messages to the conversation
        user_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.user,
            content="Hello, how can you help me?"
        )
        session.add(user_message)
        session.commit()

        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.assistant,
            content="Hello! I'm your AI assistant and I'm ready to help."
        )
        session.add(assistant_message)
        session.commit()

        # Verify data was saved
        saved_conversation = session.get(Conversation, conversation_id)
        assert saved_conversation is not None
        assert saved_conversation.user_id == user_id

        # Get all messages for this conversation
        messages = session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()

        assert len(messages) == 2
        assert messages[0].role.value == "user"
        assert messages[0].content == "Hello, how can you help me?"
        assert messages[1].role.value == "assistant"
        assert messages[1].content == "Hello! I'm your AI assistant and I'm ready to help."

    # Simulate server restart by getting a new session
    # This verifies that data persists in the database across restarts
    with get_session_context() as new_session:
        # Retrieve the same conversation and messages
        retrieved_conversation = new_session.get(Conversation, conversation_id)
        assert retrieved_conversation is not None
        assert retrieved_conversation.user_id == user_id
        assert retrieved_conversation.id == conversation_id

        # Retrieve messages
        retrieved_messages = new_session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()

        assert len(retrieved_messages) == 2
        assert retrieved_messages[0].role.value == "user"
        assert retrieved_messages[0].content == "Hello, how can you help me?"
        assert retrieved_messages[1].role.value == "assistant"
        assert retrieved_messages[1].content == "Hello! I'm your AI assistant and I'm ready to help."


def test_stateless_operation_verification():
    """
    Test that the system operates in a stateless manner by verifying that
    all state is maintained in the database and not in server memory.
    """
    user_id = "test_user_456"

    # Create conversation and messages in one session
    conversation_id = None
    with get_session_context() as session:
        # Create conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        conversation_id = str(conversation.id)

        # Add messages
        user_msg = Message(
            conversation_id=conversation_id,
            role=MessageRole.user,
            content="Test message 1"
        )
        assistant_msg = Message(
            conversation_id=conversation_id,
            role=MessageRole.assistant,
            content="Test response 1"
        )
        session.add(user_msg)
        session.add(assistant_msg)
        session.commit()

    # Verify in a completely separate session (simulating stateless operation)
    with get_session_context() as another_session:
        # Verify conversation exists
        retrieved_conversation = another_session.get(Conversation, conversation_id)
        assert retrieved_conversation is not None
        assert retrieved_conversation.user_id == user_id

        # Verify messages exist
        messages = another_session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp).all()

        assert len(messages) == 2
        assert all(msg.conversation_id == conversation_id for msg in messages)

    # This confirms that all state is stored in the database,
    # not in server memory, satisfying the stateless requirement


def test_database_connection_resilience():
    """
    Test that the database connection and session management works properly
    across different operations, simulating server resilience.
    """
    user_id = "test_user_789"

    # Perform multiple separate operations to test connection resilience
    conversation_ids = []

    # Operation 1: Create first conversation
    with get_session_context() as session:
        conv1 = Conversation(user_id=user_id + "_1")
        session.add(conv1)
        session.commit()
        conversation_ids.append(str(conv1.id))

    # Operation 2: Create second conversation
    with get_session_context() as session:
        conv2 = Conversation(user_id=user_id + "_2")
        session.add(conv2)
        session.commit()
        conversation_ids.append(str(conv2.id))

    # Operation 3: Add messages to first conversation
    with get_session_context() as session:
        msg1 = Message(
            conversation_id=conversation_ids[0],
            role=MessageRole.user,
            content="Message for first conversation"
        )
        session.add(msg1)
        session.commit()

    # Operation 4: Add messages to second conversation
    with get_session_context() as session:
        msg2 = Message(
            conversation_id=conversation_ids[1],
            role=MessageRole.user,
            content="Message for second conversation"
        )
        session.add(msg2)
        session.commit()

    # Verify all data is intact
    with get_session_context() as session:
        # Check first conversation
        conv1 = session.get(Conversation, conversation_ids[0])
        assert conv1 is not None
        conv1_msgs = session.query(Message).filter(
            Message.conversation_id == conversation_ids[0]
        ).all()
        assert len(conv1_msgs) == 1

        # Check second conversation
        conv2 = session.get(Conversation, conversation_ids[1])
        assert conv2 is not None
        conv2_msgs = session.query(Message).filter(
            Message.conversation_id == conversation_ids[1]
        ).all()
        assert len(conv2_msgs) == 1