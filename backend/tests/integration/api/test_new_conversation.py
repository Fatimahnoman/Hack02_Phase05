"""
Integration tests for new conversation creation functionality.
"""
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database import get_session_context
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message
from uuid import uuid4

client = TestClient(app)


def test_create_new_conversation():
    """
    Test that a new conversation is created when no conversation_id is provided.
    """
    user_id = "test_user_123"

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Hello, how can you help me?"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "conversation_id" in data
    assert "message" in data

    conversation_id = data["conversation_id"]
    assert conversation_id is not None
    assert isinstance(conversation_id, str)

    # Verify the conversation was actually created in the database
    with get_session_context() as session:
        conversation = session.get(Conversation, conversation_id)
        assert conversation is not None
        assert conversation.user_id == user_id


def test_new_conversation_contains_user_message():
    """
    Test that the user's message is persisted when creating a new conversation.
    """
    user_id = "test_user_123"
    user_message = "Hello, how can you help me?"

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": user_message}
    )

    assert response.status_code == 200

    data = response.json()
    conversation_id = data["conversation_id"]

    # Verify the message was saved to the database
    with get_session_context() as session:
        messages = session.query(Message).filter(Message.conversation_id == conversation_id).all()

        # Should have both user message and assistant response
        assert len(messages) >= 1

        # At least one message should be from the user with the correct content
        user_messages = [msg for msg in messages if msg.role.value == "user"]
        assert len(user_messages) >= 1
        assert user_messages[0].content == user_message


def test_new_conversation_returns_assistant_response():
    """
    Test that the endpoint returns an assistant response when creating a new conversation.
    """
    user_id = "test_user_123"

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Hello, how can you help me?"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"] is not None
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0  # Response should not be empty