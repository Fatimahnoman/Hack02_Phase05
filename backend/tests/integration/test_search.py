import pytest
from sqlmodel import Session
from app.src.database import engine
from app.src.services.search_service import SearchService
from app.src.services.task_service import TaskService
from app.src.models.task import TaskCreate


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


def test_search_functionality_integration(db_session: Session):
    """Integration test for search functionality."""
    # Create test tasks
    task_service = TaskService()
    search_service = SearchService()
    
    # Create tasks with different content
    task1_data = {
        "title": "Marketing Report",
        "description": "Complete the quarterly marketing report",
        "priority": "high",
        "status": "todo",
        "user_id": 1
    }
    
    task2_data = {
        "title": "Team Meeting",
        "description": "Prepare agenda for team meeting",
        "priority": "medium",
        "status": "in_progress",
        "user_id": 1
    }
    
    task3_data = {
        "title": "Code Review",
        "description": "Review pull requests from team members",
        "priority": "low",
        "status": "todo",
        "user_id": 1
    }
    
    # Create the tasks
    task1 = task_service.create_task(db_session, TaskCreate(**task1_data))
    task2 = task_service.create_task(db_session, TaskCreate(**task2_data))
    task3 = task_service.create_task(db_session, TaskCreate(**task3_data))
    
    # Test basic search
    results = search_service.search_tasks(db_session, user_id=1, query_str="marketing")
    assert len(results) >= 1
    found_task = next((task for task in results if task.id == task1.id), None)
    assert found_task is not None
    assert "marketing" in found_task.title.lower() or "marketing" in found_task.description.lower()
    
    # Test search with filters
    results = search_service.search_tasks(
        db_session, 
        user_id=1, 
        query_str="report", 
        priority="high"
    )
    assert len(results) >= 1
    found_task = next((task for task in results if task.id == task1.id), None)
    assert found_task is not None
    assert found_task.priority == "high"
    
    # Test search with multiple filters
    results = search_service.search_tasks(
        db_session,
        user_id=1,
        query_str="meeting",
        priority="medium",
        status="in_progress"
    )
    assert len(results) >= 1
    found_task = next((task for task in results if task.id == task2.id), None)
    assert found_task is not None
    assert found_task.priority == "medium"
    assert found_task.status == "in_progress"
    
    # Test search with no results
    results = search_service.search_tasks(
        db_session,
        user_id=1,
        query_str="nonexistentkeyword"
    )
    assert len(results) == 0
    
    # Test search without query (should return all tasks for the user)
    results = search_service.search_tasks(
        db_session,
        user_id=1,
        query_str=""
    )
    # This should return all tasks for the user
    user_tasks = task_service.get_tasks_by_user(db_session, user_id=1)
    assert len(results) == len(user_tasks)