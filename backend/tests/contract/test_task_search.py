import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.src.database import engine
from app.src.main import app
from app.src.models.task import Task


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


def test_get_tasks_search_endpoint(client: TestClient, db_session: Session):
    """Test GET /tasks/search endpoint."""
    # Create some test tasks in the database
    # This would normally be done through the API, but for testing purposes
    # we'll create them directly or via the service
    
    # First, create a task that we can search for
    task_data = {
        "title": "Searchable Task Title",
        "description": "This is a task with searchable content",
        "priority": "medium",
        "status": "todo",
        "user_id": 1
    }
    
    # Add the task via the API
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    
    # Now search for the task
    response = client.get("/api/v1/tasks/search?q=searchable")
    assert response.status_code == 200
    data = response.json()
    
    # Verify the search results
    assert "tasks" in data
    assert len(data["tasks"]) >= 1
    found_task = next((task for task in data["tasks"] if task["id"] == created_task["id"]), None)
    assert found_task is not None
    assert "searchable" in found_task["title"].lower() or "searchable" in found_task["description"].lower()
    
    # Test search with filters
    response = client.get("/api/v1/tasks/search?q=searchable&priority=medium")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) >= 1
    found_task = next((task for task in data["tasks"] if task["id"] == created_task["id"]), None)
    assert found_task is not None
    assert found_task["priority"] == "medium"
    
    # Test search with no results
    response = client.get("/api/v1/tasks/search?q=nonsensicalwordthatdoesnotexist")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 0