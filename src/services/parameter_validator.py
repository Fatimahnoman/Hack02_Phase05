"""
Parameter Validator service for validating required parameters in intents.
"""
from typing import Dict, Any, List, Optional
from ..models.intent_result import IntentResult, IntentType
from ..models.missing_parameter_request import MissingParameterRequest
from ..utils.logger import Logger


class ParameterValidator:
    """Service for validating required parameters in intents."""

    def __init__(self):
        self.logger = Logger(__name__)

    def validate_required_parameters(self, intent_result: IntentResult,
                                  provided_params: Dict[str, Any]) -> MissingParameterRequest:
        """
        Validate that all required parameters are present for an intent.

        Args:
            intent_result: The detected intent with required parameters
            provided_params: Dictionary of parameters provided by the user

        Returns:
            MissingParameterRequest if any required parameters are missing,
            None if all required parameters are present
        """
        missing_params = []

        # Check for each required parameter
        for required_param in intent_result.required_parameters:
            if required_param not in provided_params or provided_params[required_param] is None:
                missing_params.append(required_param)

        if missing_params:
            # Create a missing parameter request
            missing_request = MissingParameterRequest(
                intent_type=intent_result.type,
                missing_parameters=missing_params
            )

            self.logger.info(f"Missing parameters detected for {intent_result.type.value}: {missing_params}")
            return missing_request

        self.logger.info(f"All required parameters present for {intent_result.type.value}")
        return None

    def get_parameter_requirements(self, intent_type: IntentType) -> List[str]:
        """
        Get the list of required parameters for a given intent type.

        Args:
            intent_type: The intent type to check

        Returns:
            List of required parameter names
        """
        requirements = {
            IntentType.ADD_TASK: ['task_description'],
            IntentType.UPDATE_TASK: ['task_id'],
            IntentType.COMPLETE_TASK: ['task_id'],
            IntentType.DELETE_TASK: ['task_id']
        }

        return requirements.get(intent_type, [])

    def suggest_parameter_values(self, intent_type: IntentType, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Suggest possible values for missing parameters based on context.

        Args:
            intent_type: The intent type
            context: Optional context information to aid suggestions

        Returns:
            Dictionary of suggested parameter values
        """
        suggestions = {}

        if intent_type == IntentType.ADD_TASK:
            # Could suggest based on context like time of day, previous tasks, etc.
            if context and 'previous_tasks' in context:
                # For example, suggest similar priority as previous tasks
                pass

        elif intent_type in [IntentType.UPDATE_TASK, IntentType.COMPLETE_TASK, IntentType.DELETE_TASK]:
            # Could suggest possible task IDs based on context
            if context and 'available_tasks' in context:
                # List available task IDs to choose from
                task_ids = [task.get('id') for task in context['available_tasks'] if task.get('id')]
                if task_ids:
                    suggestions['task_id'] = task_ids[0]  # Suggest first available

        return suggestions

    def validate_parameter_format(self, param_name: str, param_value: Any) -> bool:
        """
        Validate that a parameter value is in the correct format.

        Args:
            param_name: Name of the parameter
            param_value: Value of the parameter

        Returns:
            True if valid, False otherwise
        """
        try:
            if param_name == 'task_id':
                # Validate that task_id is a number
                int(param_value)
                return True
            elif param_name == 'task_description':
                # Validate that task_description is a non-empty string
                return isinstance(param_value, str) and len(param_value.strip()) > 0
            elif param_name == 'priority':
                # Validate that priority is one of the allowed values
                return param_value in ['low', 'normal', 'high']
            else:
                # Default validation - just ensure it's not None/empty
                return param_value is not None and param_value != ""
        except (ValueError, TypeError):
            return False

    def validate_intent_with_context(self, intent_result: IntentResult,
                                   provided_params: Dict[str, Any],
                                   context: Optional[Dict[str, Any]] = None) -> MissingParameterRequest:
        """
        Validate intent with additional context checking.

        Args:
            intent_result: The detected intent
            provided_params: Provided parameters
            context: Additional context for validation

        Returns:
            MissingParameterRequest if validation fails
        """
        # First, validate required parameters
        missing_request = self.validate_required_parameters(intent_result, provided_params)
        if missing_request:
            return missing_request

        # Then, validate parameter formats
        invalid_params = []
        for param_name, param_value in provided_params.items():
            if not self.validate_parameter_format(param_name, param_value):
                invalid_params.append(param_name)

        if invalid_params:
            return MissingParameterRequest(
                intent_type=intent_result.type,
                missing_parameters=invalid_params,
                context="One or more parameters have invalid formats"
            )

        # Finally, if context is provided, do additional validation
        if context and intent_result.type in [IntentType.UPDATE_TASK, IntentType.COMPLETE_TASK, IntentType.DELETE_TASK]:
            task_id = provided_params.get('task_id')
            if task_id and context.get('available_tasks'):
                # Check if the task exists
                available_task_ids = [task.get('id') for task in context['available_tasks']]
                if int(task_id) not in available_task_ids:
                    return MissingParameterRequest(
                        intent_type=intent_result.type,
                        missing_parameters=['task_id'],
                        context=f"Task with ID {task_id} does not exist"
                    )

        return None  # All validations passed