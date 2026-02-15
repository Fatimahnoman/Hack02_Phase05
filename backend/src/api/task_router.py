from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_session_context
from ..models.task import TaskRead, TaskCreate, TaskUpdate, TaskStatusUpdate, TagRead
from ..models.reminder import ReminderRead
from ..services.task_service import TaskService
from ..services.tag_service import TagService
from ..services.reminder_service import ReminderService
from ..services.search_service import SearchService


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=dict)
def get_tasks(
    user_id: int = 1,  # In a real app, this would come from authentication
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    tag: Optional[List[str]] = Query(None, description="Filter by tag name"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks with due date >= this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks with due date <= this date"),
    without_due_date: Optional[bool] = Query(None, description="Include only tasks without due dates"),
    status: Optional[str] = Query(None, description="Filter by status (todo, in_progress, done)"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field (due_date, priority, created_at, title)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_session_context)
):
    """Retrieve a list of tasks with filtering, sorting, and pagination capabilities."""
    task_service = TaskService()
    
    skip = (page - 1) * limit
    
    tasks = task_service.get_tasks_by_user(
        db=db,
        user_id=user_id,
        priority=priority,
        tag_names=tag,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        without_due_date=without_due_date,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit
    )
    
    # Convert tasks to response format
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "completed_at": task.completed_at,
            "tags": [{"id": tag.id, "name": tag.name} for tag in task.tags],
            "reminder_offset": task.reminder_offset
        }
        task_list.append(task_dict)
    
    total = len(task_list)  # In a real implementation, you'd get the total count separately
    pages = (total + limit - 1) // limit
    
    return {
        "tasks": task_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }


@router.post("/", response_model=dict)
def create_task(task_data: TaskCreate, db: Session = Depends(get_session_context)):
    """Create a new task with optional priority, tags, due date, and reminder settings."""
    task_service = TaskService()
    task = task_service.create_task(db, task_data)
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "due_date": task.due_date,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "tags": [{"id": tag.id, "name": tag.name} for tag in task.tags],
        "reminder_offset": task.reminder_offset,
        "recurring_pattern_id": task.recurring_pattern_id
    }


@router.get("/{id}", response_model=dict)
def get_task(id: str, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Retrieve a specific task by ID."""
    task_service = TaskService()
    task = task_service.get_task_by_id(db, id, user_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "due_date": task.due_date,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "completed_at": task.completed_at,
        "tags": [{"id": tag.id, "name": tag.name} for tag in task.tags],
        "reminder_offset": task.reminder_offset
    }


@router.put("/{id}", response_model=dict)
def update_task(id: str, task_data: TaskUpdate, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Update an existing task."""
    task_service = TaskService()
    updated_task = task_service.update_task(db, id, task_data, user_id)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
        "priority": updated_task.priority,
        "status": updated_task.status,
        "due_date": updated_task.due_date,
        "created_at": updated_task.created_at,
        "updated_at": updated_task.updated_at,
        "completed_at": updated_task.completed_at,
        "tags": [{"id": tag.id, "name": tag.name} for tag in updated_task.tags],
        "reminder_offset": updated_task.reminder_offset
    }


@router.patch("/{id}/status", response_model=TaskRead)
def update_task_status(id: str, status_update: TaskStatusUpdate, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Update task completion status."""
    task_service = TaskService()
    task = task_service.get_task_by_id(db, id, user_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update status based on completion flag
    if status_update.completed:
        task.status = "done"
        task.completed_at = datetime.utcnow()
    else:
        if task.status == "done":
            task.status = "todo"
        task.completed_at = None
    
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{id}")
def delete_task(id: str, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Delete a specific task."""
    task_service = TaskService()
    success = task_service.delete_task(db, id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}


# Tags endpoints
@router.get("/tags", response_model=dict)
def get_tags(user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Retrieve a list of tags for the authenticated user."""
    tag_service = TagService()
    tags = tag_service.get_tags_by_user(db, user_id)
    
    # In a real implementation, you'd calculate usage_count
    tag_list = []
    for tag in tags:
        tag_list.append({
            "id": tag.id,
            "name": tag.name,
            "usage_count": 0  # Placeholder - would require counting related tasks
        })
    
    return {"tags": tag_list}


@router.post("/tags", response_model=TagRead)
def create_tag(tag_data: dict, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Create a new tag for the authenticated user."""
    tag_service = TagService()
    tag_create = TagCreate(name=tag_data["name"], user_id=user_id)
    tag = tag_service.create_tag(db, tag_create)
    
    return tag


# Search endpoints
@router.get("/search", response_model=dict)
def search_tasks(
    q: str = Query(..., description="Search query string"),
    user_id: int = 1,  # In a real app, this would come from authentication
    priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high)"),
    tag: Optional[List[str]] = Query(None, description="Filter by tag name"),
    status: Optional[str] = Query(None, description="Filter by status (todo, in_progress, done)"),
    sort_by: Optional[str] = Query("relevance", description="Sort by field (relevance, due_date, priority, created_at, title)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_session_context)
):
    """Search tasks by title and description with full-text search capabilities."""
    search_service = SearchService()
    
    skip = (page - 1) * limit
    
    tasks = search_service.search_tasks(
        db=db,
        user_id=user_id,
        query_str=q,
        priority=priority,
        tag_names=tag,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit
    )
    
    # Convert tasks to response format
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "tags": [{"id": tag.id, "name": tag.name} for tag in task.tags]
        }
        task_list.append(task_dict)
    
    total = len(task_list)  # In a real implementation, you'd get the total count separately
    pages = (total + limit - 1) // limit
    
    return {
        "tasks": task_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        },
        "search_info": {
            "query": q,
            "took_ms": 15  # Placeholder
        }
    }


# Reminder endpoints
@router.get("/reminders/upcoming", response_model=dict)
def get_upcoming_reminders(
    user_id: int = 1,  # In a real app, this would come from authentication
    hours_ahead: int = Query(24, description="Number of hours ahead to look for reminders"),
    db: Session = Depends(get_session_context)
):
    """Retrieve a list of upcoming reminders for the authenticated user."""
    reminder_service = ReminderService()
    reminders = reminder_service.get_upcoming_reminders(db, user_id, hours_ahead)
    
    # In a real implementation, you'd join with Task to get task title
    reminder_list = []
    for reminder in reminders:
        reminder_list.append({
            "id": reminder.id,
            "task_id": reminder.task_id,
            "task_title": "Sample Task Title",  # Would come from joining with Task
            "due_datetime": reminder.due_datetime,
            "reminder_datetime": reminder.reminder_datetime,
            "sent": reminder.sent,
            "snoozed_until": reminder.snoozed_until,
            "dismissed": reminder.dismissed,
            "created_at": reminder.created_at,
            "updated_at": reminder.updated_at
        })
    
    return {"reminders": reminder_list}


@router.post("/reminders/{id}/snooze", response_model=ReminderRead)
def snooze_reminder(id: str, snooze_data: dict, db: Session = Depends(get_session_context)):
    """Snooze a specific reminder."""
    reminder_service = ReminderService()
    minutes = snooze_data.get("minutes", 30)
    reminder = reminder_service.snooze_reminder(db, id, minutes)
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return reminder


@router.post("/reminders/{id}/dismiss", response_model=ReminderRead)
def dismiss_reminder(id: str, db: Session = Depends(get_session_context)):
    """Dismiss a specific reminder."""
    reminder_service = ReminderService()
    reminder = reminder_service.dismiss_reminder(db, id)
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return reminder