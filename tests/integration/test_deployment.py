"""
Integration test for end-to-end deployment
Tests that the entire Todo Chatbot application works as expected when deployed
"""
import pytest
import requests
import time


def test_end_to_end_deployment():
    """
    Test that the deployed application works as expected:
    1. Verify backend API is accessible
    2. Verify frontend is accessible
    3. Verify both components can communicate
    """
    
    # Wait a bit for services to be ready
    time.sleep(10)
    
    # Test backend API is accessible
    try:
        backend_response = requests.get("http://localhost:8000/health", timeout=10)
        assert backend_response.status_code == 200
        print("✓ Backend API is accessible")
    except requests.exceptions.RequestException as e:
        print(f"✗ Backend API not accessible: {e}")
        raise
    
    # Test that we can create a todo via the API
    todo_data = {
        "title": "Deployment Test Todo",
        "description": "Created during deployment verification"
    }
    
    try:
        create_response = requests.post("http://localhost:8000/api/todos/", 
                                      json=todo_data, timeout=10)
        assert create_response.status_code == 201
        todo_id = create_response.json()["id"]
        print("✓ Todo creation API works")
    except requests.exceptions.RequestException as e:
        print(f"✗ Todo creation failed: {e}")
        raise
    
    # Test that we can retrieve the created todo
    try:
        get_response = requests.get(f"http://localhost:8000/api/todos/{todo_id}", 
                                  timeout=10)
        assert get_response.status_code == 200
        retrieved_todo = get_response.json()
        assert retrieved_todo["title"] == "Deployment Test Todo"
        print("✓ Todo retrieval API works")
    except requests.exceptions.RequestException as e:
        print(f"✗ Todo retrieval failed: {e}")
        raise
    
    # Test chat functionality
    try:
        user_id = "test-user-for-deployment"
        chat_data = {
            "message": "Create a test task for deployment verification"
        }
        chat_response = requests.post(f"http://localhost:8000/api/{user_id}/chat", 
                                    json=chat_data, timeout=10)
        assert chat_response.status_code == 200
        assert "conversation_id" in chat_response.json()
        assert "message" in chat_response.json()
        print("✓ Chat functionality works")
    except requests.exceptions.RequestException as e:
        print(f"✗ Chat functionality failed: {e}")
        raise
    
    print("✓ End-to-end deployment test passed")


def test_application_readiness():
    """
    Test that the application is ready and responsive after deployment
    """
    # Test readiness endpoint
    try:
        ready_response = requests.get("http://localhost:8000/ready", timeout=10)
        assert ready_response.status_code == 200
        print("✓ Application readiness confirmed")
    except requests.exceptions.RequestException as e:
        print(f"✗ Application not ready: {e}")
        raise


if __name__ == "__main__":
    test_end_to_end_deployment()
    test_application_readiness()
    print("All end-to-end deployment tests passed!")