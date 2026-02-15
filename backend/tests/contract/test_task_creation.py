import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import patch
from app.src.models.task import Task, Tag
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


def test_post_tasks_with_priority_and_tags(client: TestClient, db_session: Session):
    """Test creating a task with priority and tags via POST /tasks endpoint."""
    # Sample request data
    task_data = {
        "title": "Test Task with Priority and Tags",
        "description": "A test task with priority and tags",
        "priority": "high",
        "tags": ["work", "important"]
    }
    
    # Make the request
    response = client.post("/api/v1/tasks/", json=task_data)
    
    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    
    # Check that the response contains expected fields
    assert "id" in response_data
    assert response_data["title"] == "Test Task with Priority and Tags"
    assert response_data["priority"] == "high"
    assert len(response_data["tags"]) == 2
    assert {"name": "work"} in [{"name": tag["name"]} for tag in response_data["tags"]]
    assert {"name": "important"} in [{"name": tag["name"]} for tag in response_data["tags"]]
    
    # Verify the task was saved to the database
    task = db_session.get(Task, response_data["id"])
    assert task is not None
    assert task.title == "Test Task with Priority and Tags"
    assert task.priority == "high"
    
    # Verify tags were created and associated
    assert len(task.tags) == 2
    tag_names = [tag.name for tag in task.tags]
    assert "work" in tag_names
    assert "important" in tag_names