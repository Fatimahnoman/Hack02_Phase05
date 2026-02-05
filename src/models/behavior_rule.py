"""
Models for behavior rule system.
"""
from enum import Enum
from typing import List, Optional, Dict, Any


class RuleType(Enum):
    """Enumeration of behavior rule types."""
    AUTHORIZED_ACTIONS = "authorized_actions"
    PARAMETER_VALIDATION = "parameter_validation"
    ID_VALIDATION = "id_validation"
    CUSTOM_RULE = "custom_rule"


class RuleCondition:
    """Represents a condition for a behavior rule."""

    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator  # e.g., 'equals', 'contains', 'greater_than', etc.
        self.value = value


class BehaviorRuleConfig:
    """Configuration for a behavior rule."""

    def __init__(self,
                 rule_type: RuleType,
                 conditions: Optional[List[RuleCondition]] = None,
                 allowed_values: Optional[List[Any]] = None,
                 blocked_values: Optional[List[Any]] = None,
                 validation_message: Optional[str] = None):
        self.rule_type = rule_type
        self.conditions = conditions or []
        self.allowed_values = allowed_values or []
        self.blocked_values = blocked_values or []
        self.validation_message = validation_message


class ValidationError:
    """Class representing a validation error."""

    def __init__(self,
                 code: str,
                 message: str,
                 field: Optional[str] = None,
                 value: Optional[Any] = None):
        self.code = code
        self.message = message
        self.field = field
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        """Convert the validation error to a dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "field": self.field,
            "value": self.value
        }


class ValidationResult:
    """Class representing the result of validation."""

    def __init__(self,
                 is_valid: bool,
                 errors: Optional[List[ValidationError]] = None,
                 safe_fallback: Optional[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.safe_fallback = safe_fallback

    def to_dict(self) -> Dict[str, Any]:
        """Convert the validation result to a dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": [error.to_dict() for error in self.errors],
            "safe_fallback": self.safe_fallback
        }