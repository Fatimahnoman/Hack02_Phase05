from sqlmodel import Session, select, func, or_, and_
from typing import List, Optional
from datetime import datetime
from ..models.task import Task, Tag
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


class SearchService:
    """Service class for searching and filtering tasks."""

    def search_tasks(
        self, 
        db: Session, 
        user_id: int, 
        query_str: str,
        priority: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        status: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        without_due_date: Optional[bool] = None,
        sort_by: Optional[str] = "relevance",  # Can be 'relevance', 'due_date', 'priority', 'created_at', 'title'
        sort_order: Optional[str] = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Search tasks by title and description with optional filters."""
        # Build the query with user filter
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply full-text search on title and description if query_str is provided
        if query_str:
            query = query.where(
                or_(
                    Task.title.contains(query_str),
                    Task.description.contains(query_str)
                )
            )
        
        # Apply other filters
        if priority:
            query = query.where(Task.priority == priority)
        
        if status:
            query = query.where(Task.status == status)
        
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)
        
        if without_due_date:
            query = query.where(Task.due_date.is_(None))
        
        # Apply tag filter
        if tag_names:
            # Join with tags to filter by tag names
            query = query.join(Task.tags).where(Tag.name.in_(tag_names))
        
        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            # Define priority order: low, medium, high
            priority_order = {'low': 1, 'medium': 2, 'high': 3}
            if sort_order == "desc":
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).desc())
            else:
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).asc())
        elif sort_by == "title":
            if sort_order == "desc":
                query = query.order_by(Task.title.desc())
            else:
                query = query.order_by(Task.title.asc())
        elif sort_by == "created_at":
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())
        else:  # Default to relevance if available, otherwise created_at
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        tasks = db.exec(query).all()
        return tasks

    def filter_tasks(
        self, 
        db: Session, 
        user_id: int, 
        priority: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        without_due_date: Optional[bool] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Filter tasks by various criteria without full-text search."""
        # Build the query with user filter
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply filters
        if priority:
            query = query.where(Task.priority == priority)
        
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)
        
        if without_due_date:
            query = query.where(Task.due_date.is_(None))
        
        if status:
            query = query.where(Task.status == status)
        
        # Apply tag filter
        if tag_names:
            # Join with tags to filter by tag names
            query = query.join(Task.tags).where(Tag.name.in_(tag_names))
        
        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            # Define priority order: low, medium, high
            if sort_order == "desc":
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).desc())
            else:
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).asc())
        elif sort_by == "title":
            if sort_order == "desc":
                query = query.order_by(Task.title.desc())
            else:
                query = query.order_by(Task.title.asc())
        else:  # Default to created_at
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        tasks = db.exec(query).all()
        return tasks

    def get_tasks_with_pagination(
        self,
        db: Session,
        user_id: int,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Get tasks with pagination and sorting."""
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).desc())
            else:
                query = query.order_by(func.array_position(['low', 'medium', 'high'], Task.priority).asc())
        elif sort_by == "title":
            if sort_order == "desc":
                query = query.order_by(Task.title.desc())
            else:
                query = query.order_by(Task.title.asc())
        else:  # Default to created_at
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        tasks = db.exec(query).all()
        return tasks