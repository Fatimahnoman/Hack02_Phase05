"""
Behavior Rules module for implementing guarded behavior and safe fallbacks.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from ..models.intent_result import IntentResult, IntentType
from ..utils.logger import Logger


class ValidationResult:
    """Class representing the result of validation."""
    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None,
                 safe_fallback: Optional[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.safe_fallback = safe_fallback


class BehaviorRule(ABC):
    """Abstract base class for behavior rules."""

    @abstractmethod
    def validate(self, intent_result: IntentResult, tool_params: Dict[str, Any]) -> ValidationResult:
        """Validate the intent and its parameters."""
        pass


class AuthorizedActionsRule(BehaviorRule):
    """Rule to ensure only authorized actions are executed."""

    def __init__(self, allowed_intents: Optional[List[IntentType]] = None):
        self.allowed_intents = allowed_intents or [
            IntentType.ADD_TASK,
            IntentType.LIST_TASKS,
            IntentType.UPDATE_TASK,
            IntentType.COMPLETE_TASK,
            IntentType.DELETE_TASK,
            IntentType.HELP
        ]
        self.logger = Logger(__name__)

    def validate(self, intent_result: IntentResult, tool_params: Dict[str, Any]) -> ValidationResult:
        """Validate that the intent is authorized."""
        if intent_result.type not in self.allowed_intents:
            self.logger.warning(f"Unauthorized intent attempted: {intent_result.type.value}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Intent '{intent_result.type.value}' is not permitted"],
                safe_fallback="I'm sorry, I can't perform that action. Please ask for help to see available commands."
            )

        return ValidationResult(is_valid=True)


class ParameterValidationRule(BehaviorRule):
    """Rule to validate required parameters are present."""

    def validate(self, intent_result: IntentResult, tool_params: Dict[str, Any]) -> ValidationResult:
        """Validate that required parameters are provided."""
        errors = []

        # Check for missing required parameters
        for param_name in intent_result.required_parameters:
            if param_name not in tool_params or tool_params[param_name] is None:
                errors.append(f"Missing required parameter: {param_name}")

        if errors:
            # Determine what parameters are missing
            missing_params = [param for param in intent_result.required_parameters
                             if param not in tool_params or tool_params[param] is None]

            # Create a safe fallback message
            fallback_msg = f"I need more information to complete this task. "
            if missing_params:
                fallback_msg += f"Please provide: {', '.join(missing_params)}"

            return ValidationResult(
                is_valid=False,
                errors=errors,
                safe_fallback=fallback_msg
            )

        return ValidationResult(is_valid=True)


class IdValidationRule(BehaviorRule):
    """Rule to validate task IDs are valid when present."""

    def validate(self, intent_result: IntentResult, tool_params: Dict[str, Any]) -> ValidationResult:
        """Validate that task IDs are valid integers when present."""
        errors = []

        # Check if task_id is provided and is a valid integer
        if 'task_id' in tool_params:
            task_id = tool_params['task_id']
            try:
                # Attempt to convert to integer to validate
                int(task_id)
            except (ValueError, TypeError):
                errors.append(f"Invalid task ID: {task_id}. Task ID must be a number.")

        if errors:
            return ValidationResult(
                is_valid=False,
                errors=errors,
                safe_fallback="Invalid task ID provided. Please specify a valid task number."
            )

        return ValidationResult(is_valid=True)


class BehaviorRulesEngine:
    """Engine to execute behavior rules and enforce guarded behavior."""

    def __init__(self):
        self.rules = [
            AuthorizedActionsRule(),
            ParameterValidationRule(),
            IdValidationRule()
        ]
        self.logger = Logger(__name__)

    def validate_intent_execution(self, intent_result: IntentResult, tool_params: Dict[str, Any]) -> ValidationResult:
        """
        Validate the intent execution against all behavior rules.

        Args:
            intent_result: The detected intent
            tool_params: Parameters for the MCP tool

        Returns:
            ValidationResult indicating if execution is allowed
        """
        self.logger.info(f"Validating intent {intent_result.type.value} for execution")

        for rule in self.rules:
            validation_result = rule.validate(intent_result, tool_params)
            if not validation_result.is_valid:
                self.logger.warning(f"Intent validation failed: {'; '.join(validation_result.errors)}")
                return validation_result

        self.logger.info("Intent validation passed")
        return ValidationResult(is_valid=True)

    def execute_guarded_action(self, action_func, *args, **kwargs) -> Union[str, Dict[str, Any]]:
        """
        Execute an action with guarded behavior protection.

        Args:
            action_func: The function to execute
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the action or error response
        """
        try:
            result = action_func(*args, **kwargs)
            return result
        except Exception as e:
            self.logger.error(f"Error during guarded action execution: {str(e)}")
            return {
                "success": False,
                "message": "An error occurred while processing your request. Please try again.",
                "errors": [str(e)]
            }


# Create a singleton instance for easy access
behavior_engine = BehaviorRulesEngine()