from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate, Tag
from ..models.recurring_task import RecurringTaskPattern
from ..models.reminder import Reminder
from .tag_service import TagService
from fastapi import HTTPException


class TaskService:
    """Service class for managing tasks with enhanced features."""
    
    def __init__(self):
        self.tag_service = TagService()

    def create_task(self, db: Session, task_data: TaskCreate) -> Task:
        """Create a new task with optional tags and recurring pattern."""
        # Create the task
        task = Task.model_validate(task_data, update={"status": "todo"})
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Associate tags if provided
        if task_data.tags:
            if len(task_data.tags) > 5:
                raise HTTPException(status_code=400, detail="Maximum 5 tags allowed per task")
            
            for tag_name in task_data.tags:
                # Get or create tag
                tag = self.tag_service.get_tag_by_name_and_user(db, tag_name, task.user_id)
                if not tag:
                    tag_create = self.tag_service.create_tag(
                        db, 
                        TagCreate(name=tag_name, user_id=task.user_id)
                    )
                    tag = tag_create
                
                task.tags.append(tag)
        
        # Handle recurring pattern if provided
        if task_data.recurring_pattern:
            pattern_data = task_data.recurring_pattern
            pattern = RecurringTaskPattern(
                base_task_title=task.title,
                base_task_description=task.description,
                recurrence_type=pattern_data.get('recurrence_type'),
                interval=pattern_data.get('interval', 1),
                start_date=pattern_data.get('start_date'),
                end_date=pattern_data.get('end_date'),
                weekdays_mask=pattern_data.get('weekdays_mask'),
                user_id=task.user_id
            )
            db.add(pattern)
            db.commit()
            db.refresh(pattern)
            
            # Link the task to the recurring pattern
            task.recurring_pattern_id = pattern.id
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return task

    def get_tasks_by_user(
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
        """Get tasks for a specific user with optional filters and sorting."""
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
            from sqlalchemy.orm import joinedload
            query = query.options(joinedload(Task.tags))
            # Additional filtering logic would be needed here
            
        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                query = query.order_by(Task.priority.desc())
            else:
                query = query.order_by(Task.priority.asc())
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

    def get_task_by_id(self, db: Session, task_id: str, user_id: int) -> Optional[Task]:
        """Get a task by its ID for a specific user."""
        task = db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        return task

    def update_task(self, db: Session, task_id: str, task_data: TaskUpdate, user_id: int) -> Optional[Task]:
        """Update an existing task."""
        task = db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        
        if not task:
            return None
        
        # Update task fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field != 'tags':  # Handle tags separately
                setattr(task, field, value)
        
        # Handle tags update
        if 'tags' in update_data and update_data['tags'] is not None:
            if len(update_data['tags']) > 5:
                raise HTTPException(status_code=400, detail="Maximum 5 tags allowed per task")
            
            # Clear existing tags
            task.tags.clear()
            
            # Add new tags
            for tag_name in update_data['tags']:
                tag = self.tag_service.get_tag_by_name_and_user(db, tag_name, user_id)
                if not tag:
                    tag_create = self.tag_service.create_tag(
                        db, 
                        TagCreate(name=tag_name, user_id=user_id)
                    )
                    tag = tag_create
                
                task.tags.append(tag)
        
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: str, user_id: int) -> bool:
        """Delete a task by its ID for a specific user."""
        task = db.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        
        if not task:
            return False
        
        db.delete(task)
        db.commit()
        return True

    def search_tasks(
        self, 
        db: Session, 
        user_id: int, 
        query_str: str,
        priority: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = "relevance",  # Can be 'relevance', 'due_date', 'priority', 'created_at', 'title'
        sort_order: Optional[str] = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Search tasks by title and description with optional filters."""
        # This is a simplified search implementation
        # In a real implementation, you would use PostgreSQL full-text search
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply full-text search on title and description
        query = query.where(
            Task.title.contains(query_str) | Task.description.contains(query_str)
        )
        
        # Apply other filters
        if priority:
            query = query.where(Task.priority == priority)
        
        if status:
            query = query.where(Task.status == status)
        
        # Apply tag filter
        if tag_names:
            # Join with tags to filter by tag names
            from sqlalchemy.orm import joinedload
            query = query.options(joinedload(Task.tags))
            # Additional filtering logic would be needed here
        
        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                query = query.order_by(Task.priority.desc())
            else:
                query = query.order_by(Task.priority.asc())
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