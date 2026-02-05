"""
MCP Task Tools module for integrating with Model Context Protocol tools.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from ..utils.logger import Logger
from ..utils.error_handler import ExecutionResult, error_handler


class Task(BaseModel):
    """Represents a task in the system."""
    id: int
    description: str
    completed: bool = False
    priority: str = "normal"
    created_at: Optional[str] = None


class TaskTools:
    """MCP-compatible task management tools."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
        self.logger = Logger(__name__)

    def create_task(self, description: str, priority: str = "normal") -> ExecutionResult:
        """
        Create a new task.

        Args:
            description: Description of the task
            priority: Priority level (low, normal, high)

        Returns:
            ExecutionResult with task information
        """
        try:
            if not description or not description.strip():
                raise ValueError("Task description is required")

            # Create the task
            task = Task(
                id=self.next_id,
                description=description.strip(),
                priority=priority
            )

            # Add to tasks list
            self.tasks.append(task)
            self.next_id += 1

            self.logger.info(f"Task created: ID {task.id}, Description: {task.description}")

            return ExecutionResult(
                success=True,
                message=f"Task '{task.description}' has been added successfully",
                data={"task_id": task.id, "status": "created", "task": task.model_dump()}
            )
        except Exception as e:
            self.logger.error(f"Error creating task: {str(e)}")
            sanitized_error = error_handler.sanitize_error_message(e)
            return ExecutionResult(
                success=False,
                message=sanitized_error,
                errors=[str(e)]
            )

    def list_tasks(self, status: Optional[str] = None) -> ExecutionResult:
        """
        List all tasks or filter by status.

        Args:
            status: Filter tasks by status ('completed', 'pending', 'all')

        Returns:
            ExecutionResult with list of tasks
        """
        try:
            filtered_tasks = self.tasks

            if status == "completed":
                filtered_tasks = [task for task in self.tasks if task.completed]
            elif status == "pending":
                filtered_tasks = [task for task in self.tasks if not task.completed]

            task_dicts = [task.model_dump() for task in filtered_tasks]

            message = f"Found {len(filtered_tasks)} task(s)"
            if status:
                message += f" ({status})"

            return ExecutionResult(
                success=True,
                message=message,
                data={"tasks": task_dicts, "total_count": len(filtered_tasks)}
            )
        except Exception as e:
            self.logger.error(f"Error listing tasks: {str(e)}")
            sanitized_error = error_handler.sanitize_error_message(e)
            return ExecutionResult(
                success=False,
                message=sanitized_error,
                errors=[str(e)]
            )

    def update_task(self, task_id: int, **updates) -> ExecutionResult:
        """
        Update a task with provided changes.

        Args:
            task_id: ID of the task to update
            **updates: Fields to update (description, completed, priority)

        Returns:
            ExecutionResult with update result
        """
        try:
            # Find the task
            task_index = None
            for i, task in enumerate(self.tasks):
                if task.id == task_id:
                    task_index = i
                    break

            if task_index is None:
                raise ValueError(f"Task with ID {task_id} not found")

            # Get the task to update
            task = self.tasks[task_index]

            # Apply updates
            for field, value in updates.items():
                if hasattr(task, field):
                    setattr(task, field, value)

            self.logger.info(f"Task updated: ID {task.id}, Updates: {list(updates.keys())}")

            return ExecutionResult(
                success=True,
                message=f"Task '{task.description}' has been updated successfully",
                data={"task_id": task.id, "updated_fields": list(updates.keys()), "task": task.model_dump()}
            )
        except Exception as e:
            self.logger.error(f"Error updating task: {str(e)}")
            sanitized_error = error_handler.sanitize_error_message(e)
            return ExecutionResult(
                success=False,
                message=sanitized_error,
                errors=[str(e)]
            )

    def complete_task(self, task_id: int) -> ExecutionResult:
        """
        Mark a task as completed.

        Args:
            task_id: ID of the task to mark as completed

        Returns:
            ExecutionResult with completion result
        """
        try:
            result = self.update_task(task_id, completed=True)
            if result.success:
                result.message = f"Task with ID {task_id} has been marked as completed"
            return result
        except Exception as e:
            self.logger.error(f"Error completing task: {str(e)}")
            sanitized_error = error_handler.sanitize_error_message(e)
            return ExecutionResult(
                success=False,
                message=sanitized_error,
                errors=[str(e)]
            )

    def delete_task(self, task_id: int) -> ExecutionResult:
        """
        Delete a task.

        Args:
            task_id: ID of the task to delete

        Returns:
            ExecutionResult with deletion result
        """
        try:
            # Find the task
            task_to_delete = None
            for i, task in enumerate(self.tasks):
                if task.id == task_id:
                    task_to_delete = task
                    self.tasks.pop(i)
                    break

            if not task_to_delete:
                raise ValueError(f"Task with ID {task_id} not found")

            self.logger.info(f"Task deleted: ID {task_to_delete.id}")

            return ExecutionResult(
                success=True,
                message=f"Task '{task_to_delete.description}' has been deleted successfully",
                data={"task_id": task_to_delete.id, "status": "deleted"}
            )
        except Exception as e:
            self.logger.error(f"Error deleting task: {str(e)}")
            sanitized_error = error_handler.sanitize_error_message(e)
            return ExecutionResult(
                success=False,
                message=sanitized_error,
                errors=[str(e)]
            )


# Create a global instance for use
task_tools = TaskTools()


def get_available_tools():
    """Return a list of available MCP tools."""
    return {
        "create_task": {
            "description": "Create a new task",
            "parameters": {
                "description": {"type": "string", "required": True},
                "priority": {"type": "string", "default": "normal"}
            }
        },
        "list_tasks": {
            "description": "List all tasks",
            "parameters": {
                "status": {"type": "string", "enum": ["all", "completed", "pending"], "default": "all"}
            }
        },
        "update_task": {
            "description": "Update a task",
            "parameters": {
                "task_id": {"type": "integer", "required": True},
                "description": {"type": "string"},
                "completed": {"type": "boolean"},
                "priority": {"type": "string"}
            }
        },
        "complete_task": {
            "description": "Mark a task as completed",
            "parameters": {
                "task_id": {"type": "integer", "required": True}
            }
        },
        "delete_task": {
            "description": "Delete a task",
            "parameters": {
                "task_id": {"type": "integer", "required": True}
            }
        }
    }