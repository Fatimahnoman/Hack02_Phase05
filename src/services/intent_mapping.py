"""
Intent Mapping service for connecting detected intents to MCP tool calls.
"""
from typing import Any, Dict, Optional
from ..models.intent_result import IntentResult, IntentType
from ..mcp.task_tools import task_tools, ExecutionResult
from ..utils.logger import Logger
from ..utils.error_handler import error_handler
from ..services.behavior_rules import behavior_engine


class IntentMapper:
    """Service for mapping detected intents to appropriate MCP tool calls."""

    def __init__(self):
        self.logger = Logger(__name__)

    def execute_intent(self, intent_result: IntentResult) -> ExecutionResult:
        """
        Execute the appropriate action based on the detected intent.

        Args:
            intent_result: The detected intent with parameters

        Returns:
            ExecutionResult from the action execution
        """
        self.logger.info(f"Executing intent: {intent_result.type.value}")

        # Validate the intent execution using behavior rules
        validation_result = behavior_engine.validate_intent_execution(
            intent_result,
            intent_result.parameters.to_dict()
        )

        if not validation_result.is_valid:
            self.logger.warning(f"Intent validation failed: {validation_result.errors}")
            return ExecutionResult(
                success=False,
                message=validation_result.safe_fallback,
                errors=validation_result.errors
            )

        # Prepare parameters for the tool call
        params = intent_result.parameters.to_dict()

        # Execute the appropriate action based on intent type
        try:
            if intent_result.type == IntentType.ADD_TASK:
                return self._execute_add_task(params)
            elif intent_result.type == IntentType.LIST_TASKS:
                return self._execute_list_tasks(params)
            elif intent_result.type == IntentType.UPDATE_TASK:
                return self._execute_update_task(params)
            elif intent_result.type == IntentType.COMPLETE_TASK:
                return self._execute_complete_task(params)
            elif intent_result.type == IntentType.DELETE_TASK:
                return self._execute_delete_task(params)
            elif intent_result.type == IntentType.HELP:
                return self._execute_help(params)
            elif intent_result.type == IntentType.UNKNOWN:
                return self._execute_unknown(params)
            else:
                return error_handler.handle_unauthorized_action(intent_result.type)
        except Exception as e:
            self.logger.error(f"Error executing intent {intent_result.type.value}: {str(e)}")
            return ExecutionResult(
                success=False,
                message=f"Failed to execute {intent_result.type.value} action",
                errors=[str(e)]
            )

    def _execute_add_task(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute add_task intent."""
        self.logger.info("Executing add_task intent")

        # Extract parameters with defaults
        description = params.get('task_description')
        priority = params.get('priority', 'normal')

        if not description:
            return ExecutionResult(
                success=False,
                message="Task description is required to create a task",
                errors=["Missing task_description parameter"]
            )

        # Call the MCP tool
        result = task_tools.create_task(description=description, priority=priority)
        self.logger.log_mcp_tool_call("create_task", {"description": description, "priority": priority})
        return result

    def _execute_list_tasks(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute list_tasks intent."""
        self.logger.info("Executing list_tasks intent")

        # Extract status filter parameter
        status = params.get('status')

        # Call the MCP tool
        result = task_tools.list_tasks(status=status)
        self.logger.log_mcp_tool_call("list_tasks", {"status": status})
        return result

    def _execute_update_task(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute update_task intent."""
        self.logger.info("Executing update_task intent")

        # Extract required parameters
        task_id = params.get('task_id')

        if not task_id:
            return ExecutionResult(
                success=False,
                message="Task ID is required to update a task",
                errors=["Missing task_id parameter"]
            )

        # Prepare update parameters (excluding task_id)
        updates = {k: v for k, v in params.items() if k != 'task_id'}

        # Call the MCP tool
        result = task_tools.update_task(task_id, **updates)
        self.logger.log_mcp_tool_call("update_task", {"task_id": task_id, "updates": updates})
        return result

    def _execute_complete_task(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute complete_task intent."""
        self.logger.info("Executing complete_task intent")

        # Extract required parameter
        task_id = params.get('task_id')

        if not task_id:
            return ExecutionResult(
                success=False,
                message="Task ID is required to complete a task",
                errors=["Missing task_id parameter"]
            )

        # Call the MCP tool
        result = task_tools.complete_task(task_id)
        self.logger.log_mcp_tool_call("complete_task", {"task_id": task_id})
        return result

    def _execute_delete_task(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute delete_task intent."""
        self.logger.info("Executing delete_task intent")

        # Extract required parameter
        task_id = params.get('task_id')

        if not task_id:
            return ExecutionResult(
                success=False,
                message="Task ID is required to delete a task",
                errors=["Missing task_id parameter"]
            )

        # Call the MCP tool
        result = task_tools.delete_task(task_id)
        self.logger.log_mcp_tool_call("delete_task", {"task_id": task_id})
        return result

    def _execute_help(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute help intent."""
        self.logger.info("Executing help intent")

        help_message = (
            "I can help you manage tasks! Here are the commands you can use:\n\n"
            "- 'add a task to [description]' - Create a new task\n"
            "- 'show me my tasks' - List all your tasks\n"
            "- 'update task [ID] to [new description]' - Update a task\n"
            "- 'complete task [ID]' or 'mark task [ID] as done' - Mark a task as completed\n"
            "- 'delete task [ID]' - Remove a task\n"
            "- 'help' - Show this help message\n\n"
            "Try saying something like: 'add a task to buy groceries'"
        )

        return ExecutionResult(
            success=True,
            message=help_message,
            data={"available_commands": [
                "add_task",
                "list_tasks",
                "update_task",
                "complete_task",
                "delete_task",
                "help"
            ]}
        )

    def _execute_unknown(self, params: Dict[str, Any]) -> ExecutionResult:
        """Execute unknown intent."""
        self.logger.info("Executing unknown intent fallback")

        return error_handler.handle_unknown_intent()

    def validate_required_parameters(self, intent_type: IntentType, params: Dict[str, Any]) -> ExecutionResult:
        """Validate that required parameters are present for the intent."""
        required_params_map = {
            IntentType.ADD_TASK: ['task_description'],
            IntentType.UPDATE_TASK: ['task_id'],
            IntentType.COMPLETE_TASK: ['task_id'],
            IntentType.DELETE_TASK: ['task_id']
        }

        required_params = required_params_map.get(intent_type, [])
        missing_params = []

        for param in required_params:
            if param not in params or params[param] is None:
                missing_params.append(param)

        if missing_params:
            message = f"Missing required parameters: {', '.join(missing_params)}"
            return ExecutionResult(
                success=False,
                message=message,
                errors=[f"Missing parameter: {param}" for param in missing_params]
            )

        return ExecutionResult(success=True)