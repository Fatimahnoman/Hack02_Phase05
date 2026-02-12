"""
Contract test for backend API endpoints
Tests that the backend API conforms to the expected contract
"""
import pytest
import requests


def test_get_todos():
    """Test GET /api/todos/ endpoint"""
    response = requests.get("http://localhost:8000/api/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_todo():
    """Test POST /api/todos/ endpoint"""
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }
    response = requests.post("http://localhost:8000/api/todos/", json=todo_data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == "Test Todo"


def test_get_single_todo():
    """Test GET /api/todos/{id} endpoint"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }
    create_response = requests.post("http://localhost:8000/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Then get it
    response = requests.get(f"http://localhost:8000/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id


def test_update_todo():
    """Test PUT /api/todos/{id} endpoint"""
    # First create a todo
    todo_data = {
        "title": "Original Title",
        "description": "Original Description"
    }
    create_response = requests.post("http://localhost:8000/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Then update it
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    response = requests.put(f"http://localhost:8000/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_delete_todo():
    """Test DELETE /api/todos/{id} endpoint"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }
    create_response = requests.post("http://localhost:8000/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Then delete it
    response = requests.delete(f"http://localhost:8000/api/todos/{todo_id}")
    assert response.status_code == 204


def test_update_todo_status():
    """Test PATCH /api/todos/{id}/status endpoint"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description"
    }
    create_response = requests.post("http://localhost:8000/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Then update its status
    status_data = {
        "completed": True
    }
    response = requests.patch(f"http://localhost:8000/api/todos/{todo_id}/status", json=status_data)
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_chat_endpoint():
    """Test POST /api/{user_id}/chat endpoint"""
    user_id = "test-user-id"
    message_data = {
        "message": "Hello, chatbot!"
    }
    response = requests.post(f"http://localhost:8000/api/{user_id}/chat", json=message_data)
    assert response.status_code == 200
    assert "conversation_id" in response.json()
    assert "message" in response.json()


def test_health_endpoint():
    """Test GET /health endpoint"""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_ready_endpoint():
    """Test GET /ready endpoint"""
    response = requests.get("http://localhost:8000/ready")
    assert response.status_code == 200
    assert "status" in response.json()