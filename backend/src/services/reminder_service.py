from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timedelta
from ..models.reminder import Reminder, ReminderCreate, ReminderUpdate
from ..dapr.pubsub import DaprPubSubUtils
from ..events.schemas import EventSchema, EventType, ReminderEventData
from fastapi import HTTPException
import logging


logger = logging.getLogger(__name__)


class ReminderService:
    """Service class for managing reminders."""

    def __init__(self):
        self.dapr_pubsub = DaprPubSubUtils()

    def create_reminder(self, db: Session, reminder_data: ReminderCreate) -> Reminder:
        """Create a new reminder."""
        # Validate that reminder is not in the past
        if reminder_data.reminder_datetime < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Reminder cannot be scheduled in the past")
        
        # Validate that reminder comes before due date
        if reminder_data.reminder_datetime >= reminder_data.due_datetime:
            raise HTTPException(status_code=400, detail="Reminder must be scheduled before due date")
        
        reminder = Reminder.model_validate(reminder_data)
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        # Publish event for reminder scheduling
        event_data = ReminderEventData(
            reminder_id=reminder.id,
            task_id=reminder.task_id,
            due_datetime=reminder.due_datetime,
            reminder_datetime=reminder.reminder_datetime,
            sent=reminder.sent,
            snoozed_until=reminder.snoozed_until,
            dismissed=reminder.dismissed,
            created_at=reminder.created_at,
            updated_at=reminder.updated_at
        )
        
        event = EventSchema(
            event_type=EventType.REMINDER_SCHEDULED,
            data=event_data.dict(),
            timestamp=datetime.utcnow()
        )
        
        # Publish the event via Dapr pub/sub
        import asyncio
        from ..dapr.pubsub import DaprPubSubUtils
        dapr_pubsub = DaprPubSubUtils()
        # In a real implementation, we would await this
        # await dapr_pubsub.publish_event("pubsub", "reminder.scheduled", event)
        
        return reminder

    async def schedule_reminders(self, db: Session):
        """Schedule reminders that are due to be sent."""
        try:
            now = datetime.utcnow()
            # Get all reminders that are scheduled to be sent but haven't been sent yet
            reminders_to_send = db.exec(
                select(Reminder)
                .where(Reminder.reminder_datetime <= now)
                .where(Reminder.sent == False)
                .where(Reminder.dismissed == False)
                .where(Reminder.snoozed_until.is_(None) | (Reminder.snoozed_until <= now))
            ).all()
            
            sent_count = 0
            for reminder in reminders_to_send:
                # Mark the reminder as sent
                reminder.sent = True
                reminder.updated_at = datetime.utcnow()
                
                # Update the database
                db.add(reminder)
                db.commit()
                
                # Publish event for reminder sent
                event_data = ReminderEventData(
                    reminder_id=reminder.id,
                    task_id=reminder.task_id,
                    due_datetime=reminder.due_datetime,
                    reminder_datetime=reminder.reminder_datetime,
                    sent=reminder.sent,
                    snoozed_until=reminder.snoozed_until,
                    dismissed=reminder.dismissed,
                    created_at=reminder.created_at,
                    updated_at=reminder.updated_at
                )
                
                event = EventSchema(
                    event_type=EventType.REMINDER_SENT,
                    data=event_data.dict(),
                    timestamp=datetime.utcnow()
                )
                
                # Publish the event via Dapr pub/sub
                from ..dapr.pubsub import DaprPubSubUtils
                dapr_pubsub = DaprPubSubUtils()
                # In a real implementation, we would await this
                # await dapr_pubsub.publish_event("pubsub", "reminder.sent", event)
                
                sent_count += 1
            
            logger.info(f"Sent {sent_count} reminders")
            return sent_count
            
        except Exception as e:
            logger.error(f"Error scheduling reminders: {str(e)}")
            return 0

    def get_reminder_by_id(self, db: Session, reminder_id: str) -> Optional[Reminder]:
        """Get a reminder by its ID."""
        reminder = db.get(Reminder, reminder_id)
        return reminder

    def get_upcoming_reminders(self, db: Session, user_id: int, hours_ahead: int = 24) -> List[Reminder]:
        """Get upcoming reminders for a user within the specified time window."""
        from ..models.task import Task
        
        cutoff_time = datetime.utcnow() + timedelta(hours=hours_ahead)
        
        # Join with Task to filter by user_id
        reminders = db.exec(
            select(Reminder)
            .join(Task, Reminder.task_id == Task.id)
            .where(Task.user_id == user_id)
            .where(Reminder.reminder_datetime <= cutoff_time)
            .where(Reminder.sent == False)
            .where(Reminder.dismissed == False)
            .order_by(Reminder.reminder_datetime.asc())
        ).all()
        
        return reminders

    def update_reminder(self, db: Session, reminder_id: str, reminder_data: ReminderUpdate) -> Optional[Reminder]:
        """Update an existing reminder."""
        reminder = db.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        update_data = reminder_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(reminder, field, value)
        
        reminder.updated_at = datetime.utcnow()
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder

    def snooze_reminder(self, db: Session, reminder_id: str, minutes: int) -> Optional[Reminder]:
        """Snooze a reminder for the specified number of minutes."""
        reminder = db.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        if reminder.dismissed:
            raise HTTPException(status_code=400, detail="Cannot snooze a dismissed reminder")
        
        # Calculate new reminder time
        new_reminder_time = datetime.utcnow() + timedelta(minutes=minutes)
        
        # Update reminder
        reminder.snoozed_until = new_reminder_time
        reminder.reminder_datetime = new_reminder_time
        reminder.sent = False  # Reset sent flag since it's being rescheduled
        reminder.updated_at = datetime.utcnow()
        
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return reminder

    def dismiss_reminder(self, db: Session, reminder_id: str) -> Optional[Reminder]:
        """Dismiss a reminder."""
        reminder = db.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        reminder.dismissed = True
        reminder.sent = True  # Mark as sent to prevent future delivery
        reminder.updated_at = datetime.utcnow()
        
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        
        return reminder

    def delete_reminder(self, db: Session, reminder_id: str) -> bool:
        """Delete a reminder by its ID."""
        reminder = db.get(Reminder, reminder_id)
        if not reminder:
            return False
        
        db.delete(reminder)
        db.commit()
        return True