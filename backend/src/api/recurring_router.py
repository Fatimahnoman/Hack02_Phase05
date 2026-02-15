from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..database import get_session_context
from ..models.recurring_task import (
    RecurringTaskPatternRead, 
    RecurringTaskPatternCreate, 
    RecurringTaskPatternUpdate
)
from ..services.recurring_task_service import RecurringTaskService


router = APIRouter(prefix="/recurring-patterns", tags=["recurring-patterns"])

@router.get("/", response_model=dict)
def get_recurring_patterns(user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Retrieve a list of recurring task patterns for the authenticated user."""
    recurring_service = RecurringTaskService()
    patterns = recurring_service.get_recurring_patterns_by_user(db, user_id)
    
    pattern_list = []
    for pattern in patterns:
        pattern_list.append({
            "id": pattern.id,
            "base_task_title": pattern.base_task_title,
            "base_task_description": pattern.base_task_description,
            "recurrence_type": pattern.recurrence_type,
            "interval": pattern.interval,
            "start_date": pattern.start_date,
            "end_date": pattern.end_date,
            "weekdays_mask": pattern.weekdays_mask,
            "created_at": pattern.created_at,
            "updated_at": pattern.updated_at
        })
    
    return {"patterns": pattern_list}


@router.post("/", response_model=dict)
def create_recurring_pattern(
    pattern_data: RecurringTaskPatternCreate,
    user_id: int = 1,  # user_id from auth in real app
    db: Session = Depends(get_session_context)
):
    """Create a new recurring task pattern."""
    recurring_service = RecurringTaskService()
    
    # Add user_id to the pattern data
    pattern_data_dict = pattern_data.model_dump()
    pattern_data_dict["user_id"] = user_id
    pattern_data_with_user = RecurringTaskPatternCreate(**pattern_data_dict)
    
    pattern = recurring_service.create_recurring_pattern(db, pattern_data_with_user)
    
    return {
        "id": pattern.id,
        "base_task_title": pattern.base_task_title,
        "base_task_description": pattern.base_task_description,
        "recurrence_type": pattern.recurrence_type,
        "interval": pattern.interval,
        "start_date": pattern.start_date,
        "end_date": pattern.end_date,
        "weekdays_mask": pattern.weekdays_mask,
        "created_at": pattern.created_at,
        "updated_at": pattern.updated_at
    }


@router.get("/{id}", response_model=RecurringTaskPatternRead)
def get_recurring_pattern(id: str, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Retrieve a specific recurring task pattern by ID."""
    recurring_service = RecurringTaskService()
    pattern = recurring_service.get_recurring_pattern_by_id(db, id, user_id)
    
    if not pattern:
        raise HTTPException(status_code=404, detail="Recurring pattern not found")
    
    return pattern


@router.put("/{id}", response_model=RecurringTaskPatternRead)
def update_recurring_pattern(
    id: str,
    pattern_data: RecurringTaskPatternUpdate,
    user_id: int = 1,  # user_id from auth in real app
    db: Session = Depends(get_session_context)
):
    """Update an existing recurring task pattern."""
    recurring_service = RecurringTaskService()
    updated_pattern = recurring_service.update_recurring_pattern(db, id, pattern_data, user_id)
    
    if not updated_pattern:
        raise HTTPException(status_code=404, detail="Recurring pattern not found")
    
    return updated_pattern


@router.delete("/{id}")
def delete_recurring_pattern(id: str, user_id: int = 1, db: Session = Depends(get_session_context)):  # user_id from auth in real app
    """Delete a specific recurring task pattern."""
    recurring_service = RecurringTaskService()
    success = recurring_service.delete_recurring_pattern(db, id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Recurring pattern not found")
    
    return {"message": "Recurring pattern deleted successfully"}