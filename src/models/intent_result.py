"""
Models for intent detection and result handling.
"""
from enum import Enum
from typing import Any, Dict, List, Optional


class IntentType(Enum):
    """Enumeration of possible intent types."""
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    HELP = "help"
    UNKNOWN = "unknown"


class IntentParameter:
    """Class representing parameters extracted from user input."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the parameter object to a dictionary."""
        result = {}
        for attr in dir(self):
            if not attr.startswith('_') and attr != 'to_dict':
                val = getattr(self, attr)
                if not callable(val):
                    result[attr] = val
        return result


class IntentResult:
    """Class representing the result of intent detection."""

    def __init__(self, intent_type: IntentType, confidence: float = 1.0,
                 parameters: Optional[IntentParameter] = None,
                 required_parameters: Optional[List[str]] = None):
        self.type = intent_type
        self.confidence = confidence
        self.parameters = parameters or IntentParameter()
        self.required_parameters = required_parameters or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert the intent result to a dictionary."""
        return {
            "type": self.type.value,
            "confidence": self.confidence,
            "parameters": self.parameters.to_dict() if self.parameters else {},
            "required_parameters": self.required_parameters
        }