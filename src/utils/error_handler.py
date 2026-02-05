"""
Error handling and validation framework for the intent mapping system.
"""
from typing import Any, Dict, List, Optional
from ..models.intent_result import IntentType


class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(self, message: str, error_code: Optional[str] = None, field: Optional[str] = None):
        self.message = message
        self.error_code = error_code or "VALIDATION_ERROR"
        self.field = field
        super().__init__(message)


class ExecutionResult:
    """Class representing the result of an execution attempt."""

    def __init__(self, success: bool = True, message: str = "",
                 data: Optional[Dict[str, Any]] = None, errors: Optional[List[str]] = None):
        self.success = success
        self.message = message
        self.data = data or {}
        self.errors = errors or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert the execution result to a dictionary."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors
        }


class ValidationResult:
    """Class representing the result of validation."""

    def __init__(self, is_valid: bool, errors: Optional[List[ValidationError]] = None):
        self.is_valid = is_valid
        self.errors = errors or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert the validation result to a dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": [{"message": err.message, "code": err.error_code, "field": err.field}
                      for err in self.errors]
        }


class ErrorHandler:
    """Error handling framework for the intent mapping system."""

    def __init__(self):
        self.error_templates = {
            "MISSING_PARAMETER": "Missing required parameter: {field}",
            "INVALID_PARAMETER": "Invalid parameter value for {field}: {value}",
            "UNAUTHORIZED_ACTION": "This action is not permitted: {action}",
            "TASK_NOT_FOUND": "Task with ID {id} not found",
            "CONNECTION_ERROR": "Unable to connect to required service",
            "PERMISSION_DENIED": "Insufficient permissions for this action",
            "UNKNOWN_INTENT": "Could not understand the request. Please try rephrasing.",
        }

    def create_validation_error(self, field: str, value: Any = None,
                               error_code: str = "INVALID_PARAMETER") -> ValidationError:
        """Create a validation error with appropriate message."""
        message = self.error_templates[error_code].format(field=field, value=value)
        return ValidationError(message, error_code, field)

    def handle_validation_errors(self, errors: List[ValidationError]) -> ExecutionResult:
        """Convert validation errors to execution result."""
        error_messages = [err.message for err in errors]
        return ExecutionResult(
            success=False,
            message="Validation failed",
            errors=error_messages
        )

    def handle_unknown_intent(self) -> ExecutionResult:
        """Handle cases where intent cannot be determined."""
        return ExecutionResult(
            success=False,
            message=self.error_templates["UNKNOWN_INTENT"],
            errors=[self.error_templates["UNKNOWN_INTENT"]]
        )

    def handle_unauthorized_action(self, intent_type: IntentType) -> ExecutionResult:
        """Handle attempts to execute unauthorized actions."""
        message = self.error_templates["UNAUTHORIZED_ACTION"].format(action=intent_type.value)
        return ExecutionResult(
            success=False,
            message=message,
            errors=[message]
        )

    def sanitize_error_message(self, error: Exception) -> str:
        """Sanitize error messages to prevent exposure of internal details."""
        error_type = type(error).__name__

        # Map known internal errors to user-friendly messages
        if "SQL" in error_type.upper() or "DATABASE" in str(error).upper():
            return "Database operation failed. Please try again."
        elif "CONNECTION" in str(error).upper():
            return "Connection to service failed. Please try again later."
        elif "TIMEOUT" in error_type.upper():
            return "Operation timed out. Please try again."
        else:
            return f"An unexpected error occurred: {error_type}"


# Singleton instance
error_handler = ErrorHandler()