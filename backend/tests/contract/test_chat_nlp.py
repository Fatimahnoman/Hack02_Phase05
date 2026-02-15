import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.src.database import engine
from app.src.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


def test_chat_api_nlp_commands_contract(client: TestClient, db_session: Session):
    """Contract test for chat API with NLP commands."""
    # Test the chat endpoint with various NLP commands
    
    # Test 1: Simple task creation command
    chat_request = {
        "user_input": "Create a task to buy groceries",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert "state_reflection" in response_data
    
    # Test 2: Task with priority
    chat_request = {
        "user_input": "Create a high priority task to fix the bug",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 3: Task with tags
    chat_request = {
        "user_input": "Create a task #work to prepare presentation",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 4: Task with due date
    chat_request = {
        "user_input": "Create a task to submit report by Friday",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 5: Complex command with multiple features
    chat_request = {
        "user_input": "Create a high priority #work task to finish project by tomorrow and remind me",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 6: Recurring task command
    chat_request = {
        "user_input": "Create a recurring task to water plants every Monday",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 7: Change priority of existing task (hypothetical)
    chat_request = {
        "user_input": "Make the grocery task high priority",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 8: Add tag to existing task (hypothetical)
    chat_request = {
        "user_input": "Add #urgent tag to the bug fix task",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    
    # Test 9: General conversation (should still work)
    chat_request = {
        "user_input": "Hello, how are you?",
        "user_id": "1"
    }
    
    response = client.post("/api/v1/chat/", json=chat_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    
    # Test 10: Check that state reflection is included
    assert "state_reflection" in response_data
    state_reflection = response_data["state_reflection"]
    assert "user_id" in state_reflection
    assert "task_count" in state_reflection