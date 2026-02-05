"""
Model for representing missing parameter requests.
"""
from typing import List, Optional, Dict, Any
from .intent_result import IntentType


class MissingParameterRequest:
    """Class representing a request for missing parameters from user."""

    def __init__(self,
                 intent_type: IntentType,
                 missing_parameters: List[str],
                 suggested_values: Optional[Dict[str, Any]] = None,
                 context: Optional[str] = None):
        """
        Initialize a missing parameter request.

        Args:
            intent_type: The intent that needs the missing parameters
            missing_parameters: List of parameter names that are missing
            suggested_values: Suggested values for the missing parameters
            context: Context information about the current operation
        """
        self.intent_type = intent_type
        self.missing_parameters = missing_parameters
        self.suggested_values = suggested_values or {}
        self.context = context

    def get_request_message(self) -> str:
        """Get a user-friendly message requesting the missing parameters."""
        if len(self.missing_parameters) == 1:
            param = self.missing_parameters[0]
            base_msg = f"I need more information to complete this {self.intent_type.value} action."

            if param == 'task_description':
                return f"{base_msg} What would you like to name your task?"
            elif param == 'task_id':
                return f"{base_msg} Which task would you like to work with? Please provide the task number."
            elif param == 'description':
                return f"{base_msg} What should the new description be?"
            else:
                return f"{base_msg} Please provide: {param}"

        else:
            params_str = ", ".join(self.missing_parameters)
            return (f"I need more information to complete this {self.intent_type.value} action. "
                   f"Please provide: {params_str}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the missing parameter request to a dictionary."""
        return {
            "intent_type": self.intent_type.value,
            "missing_parameters": self.missing_parameters,
            "suggested_values": self.suggested_values,
            "context": self.context,
            "request_message": self.get_request_message()
        }

    def __repr__(self) -> str:
        """String representation of the missing parameter request."""
        return (f"MissingParameterRequest(intent_type={self.intent_type.value}, "
               f"missing_parameters={self.missing_parameters})")


class ParameterRequirement:
    """Class representing a parameter requirement for an intent."""

    def __init__(self, name: str, description: str, required: bool = True, example: Optional[str] = None):
        """
        Initialize a parameter requirement.

        Args:
            name: Name of the parameter
            description: Description of what the parameter represents
            required: Whether the parameter is required or optional
            example: Example value for the parameter
        """
        self.name = name
        self.description = description
        self.required = required
        self.example = example

    def to_dict(self) -> Dict[str, Any]:
        """Convert the parameter requirement to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "example": self.example
        }