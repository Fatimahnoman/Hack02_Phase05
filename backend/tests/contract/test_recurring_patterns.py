import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.src.database import engine
from app.src.main import app
from datetime import datetime


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


def test_post_recurring_patterns_endpoint(client: TestClient, db_session: Session):
    """Test POST /recurring-patterns endpoint."""
    # Sample recurring pattern data
    pattern_data = {
        "base_task_title": "Daily Standup",
        "base_task_description": "Daily team standup meeting",
        "recurrence_type": "daily",
        "interval": 1,
        "start_date": "2023-12-01T00:00:00Z",
        "end_date": "2024-12-01T00:00:00Z",
        "user_id": 1
    }
    
    # Make the request
    response = client.post("/api/v1/recurring-patterns/", json=pattern_data)
    
    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    
    # Check that the response contains expected fields
    assert "id" in response_data
    assert response_data["base_task_title"] == "Daily Standup"
    assert response_data["base_task_description"] == "Daily team standup meeting"
    assert response_data["recurrence_type"] == "daily"
    assert response_data["interval"] == 1
    assert response_data["user_id"] == 1
    
    # Test with weekly pattern and weekdays_mask
    weekly_pattern_data = {
        "base_task_title": "Weekly Review",
        "base_task_description": "Weekly team review meeting",
        "recurrence_type": "weekly",
        "interval": 1,
        "start_date": "2023-12-01T00:00:00Z",
        "end_date": "2024-12-01T00:00:00Z",
        "weekdays_mask": 62,  # Mon-Fri (2+4+8+16+32)
        "user_id": 1
    }
    
    response = client.post("/api/v1/recurring-patterns/", json=weekly_pattern_data)
    assert response.status_code == 200
    response_data = response.json()
    
    assert response_data["base_task_title"] == "Weekly Review"
    assert response_data["recurrence_type"] == "weekly"
    assert response_data["weekdays_mask"] == 62
    
    # Test with invalid recurrence type (should fail)
    invalid_pattern_data = {
        "base_task_title": "Invalid Pattern",
        "base_task_description": "Pattern with invalid type",
        "recurrence_type": "invalid_type",
        "interval": 1,
        "start_date": "2023-12-01T00:00:00Z",
        "user_id": 1
    }
    
    response = client.post("/api/v1/recurring-patterns/", json=invalid_pattern_data)
    # This might return 422 or 400 depending on validation
    # If validation is done in the service layer, it might return 400
    assert response.status_code in [400, 422]