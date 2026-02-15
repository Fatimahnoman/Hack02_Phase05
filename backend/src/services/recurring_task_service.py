from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from ..models.recurring_task import RecurringTaskPattern, RecurringTaskPatternCreate, RecurringTaskPatternUpdate
from ..models.task import Task
from ..dapr.pubsub import DaprPubSubUtils
from ..events.schemas import EventSchema, EventType, RecurringInstanceEventData
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


class RecurringTaskService:
    """Service class for managing recurring task patterns."""

    def __init__(self):
        self.dapr_pubsub = DaprPubSubUtils()

    def create_recurring_pattern(self, db: Session, pattern_data: RecurringTaskPatternCreate) -> RecurringTaskPattern:
        """Create a new recurring task pattern."""
        # Validate start date is in the future
        if pattern_data.start_date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Start date must be in the future")
        
        # Validate end date is after start date if provided
        if pattern_data.end_date and pattern_data.end_date < pattern_data.start_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        # Validate interval is positive
        if pattern_data.interval <= 0:
            raise HTTPException(status_code=400, detail="Interval must be positive")
        
        # Validate recurrence type
        valid_types = ['daily', 'weekly', 'monthly', 'custom']
        if pattern_data.recurrence_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"Invalid recurrence type. Valid types: {valid_types}")
        
        # Validate weekdays_mask for weekly patterns
        if pattern_data.recurrence_type == 'weekly':
            if pattern_data.weekdays_mask and (pattern_data.weekdays_mask < 1 or pattern_data.weekdays_mask > 127):
                # 127 = 0b1111111 (all 7 days)
                raise HTTPException(status_code=400, detail="Invalid weekdays mask for weekly pattern")
        
        pattern = RecurringTaskPattern.model_validate(pattern_data)
        db.add(pattern)
        db.commit()
        db.refresh(pattern)
        
        return pattern

    def get_recurring_pattern_by_id(self, db: Session, pattern_id: str, user_id: int) -> Optional[RecurringTaskPattern]:
        """Get a recurring pattern by its ID for a specific user."""
        pattern = db.exec(
            select(RecurringTaskPattern)
            .where(RecurringTaskPattern.id == pattern_id)
            .where(RecurringTaskPattern.user_id == user_id)
        ).first()
        return pattern

    def get_recurring_patterns_by_user(self, db: Session, user_id: int) -> List[RecurringTaskPattern]:
        """Get all recurring patterns for a specific user."""
        patterns = db.exec(
            select(RecurringTaskPattern)
            .where(RecurringTaskPattern.user_id == user_id)
            .order_by(RecurringTaskPattern.created_at.desc())
        ).all()
        return patterns

    def update_recurring_pattern(self, db: Session, pattern_id: str, pattern_data: RecurringTaskPatternUpdate, user_id: int) -> Optional[RecurringTaskPattern]:
        """Update an existing recurring pattern."""
        pattern = db.exec(
            select(RecurringTaskPattern)
            .where(RecurringTaskPattern.id == pattern_id)
            .where(RecurringTaskPattern.user_id == user_id)
        ).first()
        
        if not pattern:
            return None
        
        update_data = pattern_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pattern, field, value)
        
        pattern.updated_at = datetime.utcnow()
        db.add(pattern)
        db.commit()
        db.refresh(pattern)
        return pattern

    def delete_recurring_pattern(self, db: Session, pattern_id: str, user_id: int) -> bool:
        """Delete a recurring pattern by its ID for a specific user."""
        pattern = db.exec(
            select(RecurringTaskPattern)
            .where(RecurringTaskPattern.id == pattern_id)
            .where(RecurringTaskPattern.user_id == user_id)
        ).first()
        
        if not pattern:
            return False
        
        db.delete(pattern)
        db.commit()
        return True

    def generate_next_instance(self, db: Session, pattern: RecurringTaskPattern) -> Optional[Task]:
        """Generate the next instance of a recurring task based on the pattern."""
        try:
            # Check if pattern has ended
            if pattern.end_date and datetime.utcnow() > pattern.end_date:
                logger.info(f"Pattern {pattern.id} has ended, not creating new instance")
                return None
            
            # Create a new task based on the pattern
            new_task_data = {
                "title": pattern.base_task_title,
                "description": pattern.base_task_description,
                "user_id": pattern.user_id,
                "status": "todo"
            }
            
            new_task = Task(**new_task_data)
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            
            # Publish event for the new instance
            event_data = RecurringInstanceEventData(
                pattern_id=pattern.id,
                new_task_id=new_task.id,
                user_id=new_task.user_id,
                title=new_task.title,
                description=new_task.description,
                created_at=new_task.created_at
            )
            
            event = EventSchema(
                event_type=EventType.RECURRING_INSTANCE_CREATED,
                data=event_data.dict(),
                timestamp=datetime.utcnow()
            )
            
            # Publish the event via Dapr pub/sub
            import asyncio
            from ..dapr.pubsub import DaprPubSubUtils
            dapr_pubsub = DaprPubSubUtils()
            # In a real implementation, we would await this
            # await dapr_pubsub.publish_event("pubsub", "recurring.instance.created", event)
            
            logger.info(f"Created new recurring instance for pattern {pattern.id}: {new_task.id}")
            return new_task
            
        except Exception as e:
            logger.error(f"Error generating next recurring instance: {str(e)}")
            return None

    async def schedule_recurring_tasks(self, db: Session):
        """Schedule recurring tasks based on their patterns."""
        try:
            # Get all recurring patterns that might need new instances created
            now = datetime.utcnow()
            patterns = db.exec(
                select(RecurringTaskPattern)
                .where(RecurringTaskPattern.start_date <= now)
                .where(or_(RecurringTaskPattern.end_date.is_(None), RecurringTaskPattern.end_date >= now))
            ).all()
            
            created_instances = 0
            for pattern in patterns:
                # Check if a new instance should be created based on the recurrence pattern
                should_create = self.should_create_new_instance(pattern, now)
                if should_create:
                    new_task = self.generate_next_instance(db, pattern)
                    if new_task:
                        created_instances += 1
                        
            logger.info(f"Scheduled {created_instances} new recurring task instances")
            return created_instances
            
        except Exception as e:
            logger.error(f"Error scheduling recurring tasks: {str(e)}")
            return 0

    def should_create_new_instance(self, pattern: RecurringTaskPattern, current_time: datetime) -> bool:
        """Determine if a new instance should be created based on the pattern and current time."""
        # This is a simplified implementation
        # In a real system, you'd need more complex logic to determine if a new instance
        # should be created based on the recurrence type and interval
        
        # For daily patterns
        if pattern.recurrence_type == "daily":
            # Check if at least 'interval' days have passed since the last instance
            # This would require tracking the last created instance time
            return True  # Simplified for demo purposes
        
        # For weekly patterns
        elif pattern.recurrence_type == "weekly":
            if pattern.weekdays_mask:
                # Check if current day is in the specified weekdays
                current_weekday_bit = 1 << current_time.weekday()
                if pattern.weekdays_mask & current_weekday_bit:
                    # Check if enough intervals have passed
                    return True
            else:
                # Default to same weekday as start date
                return current_time.weekday() == pattern.start_date.weekday()
        
        # For monthly patterns
        elif pattern.recurrence_type == "monthly":
            # Check if it's the same day of the month as the start date
            # Handle months with different number of days appropriately
            start_day = pattern.start_date.day
            current_day = current_time.day
            
            # Special handling for months with fewer days than start_day
            if current_day == start_day or (start_day > 28 and current_day == current_time.day):
                return True
        
        # For custom patterns
        elif pattern.recurrence_type == "custom":
            # Custom logic would go here based on the specific pattern
            return True
        
        return False