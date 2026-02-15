from typing import Dict, Any
from sqlmodel import Session
from .schemas import EventSchema, EventType, TaskEventData, ReminderEventData, RecurringInstanceEventData
from ..models.task import Task
from ..models.reminder import Reminder
from ..models.recurring_task import RecurringTaskPattern
from ..services.task_service import TaskService
from ..services.reminder_service import ReminderService
from ..dapr.client import DaprClientWrapper
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class EventHandler:
    """Handler for processing different types of events."""
    
    def __init__(self, db_session: Session, dapr_client: DaprClientWrapper):
        self.db = db_session
        self.dapr_client = dapr_client
        self.task_service = TaskService()
        self.reminder_service = ReminderService()
    
    async def handle_event(self, event: EventSchema) -> bool:
        """Route the event to the appropriate handler based on event type."""
        try:
            if event.event_type == EventType.TASK_CREATED:
                return await self.handle_task_created(event.data)
            elif event.event_type == EventType.TASK_UPDATED:
                return await self.handle_task_updated(event.data)
            elif event.event_type == EventType.TASK_COMPLETED:
                return await self.handle_task_completed(event.data)
            elif event.event_type == EventType.TASK_DELETED:
                return await self.handle_task_deleted(event.data)
            elif event.event_type == EventType.REMINDER_SCHEDULED:
                return await self.handle_reminder_scheduled(event.data)
            elif event.event_type == EventType.REMINDER_SENT:
                return await self.handle_reminder_sent(event.data)
            elif event.event_type == EventType.RECURRING_INSTANCE_CREATED:
                return await self.handle_recurring_instance_created(event.data)
            else:
                logger.warning(f"Unknown event type: {event.event_type}")
                return False
        except Exception as e:
            logger.error(f"Error handling event {event.event_type}: {str(e)}")
            return False
    
    async def handle_task_created(self, data: Dict[str, Any]) -> bool:
        """Handle task created event."""
        logger.info(f"Handling task created event for task ID: {data.get('task_id')}")
        # This would typically update caches or trigger other workflows
        return True
    
    async def handle_task_updated(self, data: Dict[str, Any]) -> bool:
        """Handle task updated event."""
        logger.info(f"Handling task updated event for task ID: {data.get('task_id')}")
        # This would typically update caches or notify other services
        return True
    
    async def handle_task_completed(self, data: Dict[str, Any]) -> bool:
        """Handle task completed event."""
        logger.info(f"Handling task completed event for task ID: {data.get('task_id')}")
        
        # If this task has a recurring pattern, create the next instance
        task_data = TaskEventData(**data)
        task = self.db.query(Task).filter(Task.id == task_data.task_id).first()
        
        if task and task.recurring_pattern_id:
            await self.create_next_recurring_instance(task)
        
        return True
    
    async def handle_task_deleted(self, data: Dict[str, Any]) -> bool:
        """Handle task deleted event."""
        logger.info(f"Handling task deleted event for task ID: {data.get('task_id')}")
        # This would typically clean up related resources
        return True
    
    async def handle_reminder_scheduled(self, data: Dict[str, Any]) -> bool:
        """Handle reminder scheduled event."""
        logger.info(f"Handling reminder scheduled event for reminder ID: {data.get('reminder_id')}")
        # This would typically update notification systems
        return True
    
    async def handle_reminder_sent(self, data: Dict[str, Any]) -> bool:
        """Handle reminder sent event."""
        logger.info(f"Handling reminder sent event for reminder ID: {data.get('reminder_id')}")
        # This would typically update notification status
        return True
    
    async def handle_recurring_instance_created(self, data: Dict[str, Any]) -> bool:
        """Handle recurring instance created event."""
        logger.info(f"Handling recurring instance created event for pattern ID: {data.get('pattern_id')}")
        # This would typically notify users of the new task
        return True
    
    async def create_next_recurring_instance(self, completed_task: Task) -> bool:
        """Create the next instance of a recurring task based on its pattern."""
        try:
            # Get the recurring pattern
            pattern = self.db.query(RecurringTaskPattern).filter(
                RecurringTaskPattern.id == completed_task.recurring_pattern_id
            ).first()
            
            if not pattern:
                logger.error(f"No recurring pattern found for task {completed_task.id}")
                return False
            
            # Check if we should create a new instance based on the pattern
            now = datetime.utcnow()
            if pattern.end_date and now > pattern.end_date:
                # Pattern has ended, don't create new instance
                return True
            
            # Create a new task based on the pattern
            new_task_data = {
                "title": pattern.base_task_title,
                "description": pattern.base_task_description,
                "user_id": completed_task.user_id,
                "priority": completed_task.priority,  # Maintain the same priority
                "status": "todo"
            }
            
            # Calculate next due date based on recurrence pattern
            # This is a simplified implementation - in reality, you'd have more complex logic
            # depending on the recurrence type (daily, weekly, monthly, etc.)
            
            new_task = Task(**new_task_data)
            self.db.add(new_task)
            self.db.commit()
            self.db.refresh(new_task)
            
            # If the original task had a due date and reminder, set those for the new task too
            if completed_task.due_date and completed_task.reminder_offset:
                # Calculate next due date based on recurrence pattern
                # This would require more complex logic in a real implementation
                pass
            
            # Publish event for the new instance
            from .schemas import EventSchema, EventType
            event_data = {
                "pattern_id": pattern.id,
                "new_task_id": new_task.id,
                "user_id": new_task.user_id,
                "title": new_task.title,
                "created_at": new_task.created_at
            }
            
            event = EventSchema(
                event_type=EventType.RECURRING_INSTANCE_CREATED,
                data=event_data,
                timestamp=datetime.utcnow()
            )
            
            # Publish the event via Dapr
            # await self.dapr_client.publish_event("pubsub", "recurring.instance.created", event)
            
            logger.info(f"Created new recurring instance for pattern {pattern.id}: {new_task.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating next recurring instance: {str(e)}")
            return False