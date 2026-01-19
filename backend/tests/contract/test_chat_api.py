"""
Contract tests for the chat API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from uuid import uuid4

client = TestClient(app)


def test_post_chat_endpoint_contract():
    """
    Test the contract of the POST /api/{user_id}/chat endpoint.
    Verifies that the endpoint accepts the correct request format and returns the expected response format.
    """
    user_id = "test_user_123"

    # Test request without conversation_id (new conversation)
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": "Hello, how can you help me?"}
    )

    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "conversation_id" in data
    assert "message" in data

    # Verify conversation_id is a valid UUID string
    assert isinstance(data["conversation_id"], str)

    # Verify message is a string
    assert isinstance(data["message"], str)


def test_post_chat_endpoint_with_conversation_id():
    """
    Test the contract of the POST /api/{user_id}/chat endpoint with existing conversation_id.
    """
    user_id = "test_user_123"
    conversation_id = str(uuid4())

    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "Continuing the conversation",
            "conversation_id": conversation_id
        }
    )

    assert response.status_code == 200

    # Verify response structure
    data = response.json()
    assert "conversation_id" in data
    assert "message" in data
    assert data["conversation_id"] == conversation_id  # Should return the same conversation_id
    assert isinstance(data["message"], str)


def test_post_chat_endpoint_missing_message():
    """
    Test that the endpoint returns an error when message is missing.
    """
    user_id = "test_user_123"

    response = client.post(
        f"/api/{user_id}/chat",
        json={}
    )

    # Should return validation error (422) because message is required
    assert response.status_code == 422


def test_post_chat_endpoint_invalid_json():
    """
    Test that the endpoint handles invalid JSON gracefully.
    """
    user_id = "test_user_123"

    response = client.post(
        f"/api/{user_id}/chat",
        content="{invalid json}",
        headers={"Content-Type": "application/json"}
    )

    # Should return 422 for invalid JSON
    assert response.status_code >= 400


def test_post_chat_endpoint_invalid_conversation_id_format():
    """
    Test that the endpoint returns an error when conversation_id has invalid format.
    """
    user_id = "test_user_123"
    invalid_conversation_id = "not-a-valid-uuid"

    response = client.post(
        f"/api/{user_id}/chat",
        json={
            "message": "Test message",
            "conversation_id": invalid_conversation_id
        }
    )

    # Should return 400 for invalid conversation_id format
    assert response.status_code == 400