"""
Contract test for missing data validation functionality.
"""
import pytest
from src.models.intent_result import IntentResult, IntentType
from src.services.intent_mapping import IntentMapper
from src.services.behavior_rules import ParameterValidationRule, IdValidationRule, ValidationResult


def test_parameter_validation_rule_contract():
    """Test the parameter validation rule contract."""
    rule = ParameterValidationRule()

    # Test with all required parameters present
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {'task_description': 'Buy groceries'}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is True
    assert len(validation_result.errors) == 0
    assert validation_result.safe_fallback is None

    # Test with missing required parameters
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0
    assert validation_result.safe_fallback is not None

    # Test with partial parameters
    intent_result = IntentResult(IntentType.UPDATE_TASK, required_parameters=['task_id', 'description'])
    params = {'task_id': 1}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0
    assert 'description' in validation_result.errors[0]


def test_id_validation_rule_contract():
    """Test the ID validation rule contract."""
    rule = IdValidationRule()

    # Test with valid integer ID
    intent_result = IntentResult(IntentType.UPDATE_TASK)
    params = {'task_id': 5}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is True

    # Test with string that represents an integer
    params = {'task_id': '10'}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is True

    # Test with invalid ID
    params = {'task_id': 'invalid_id'}
    validation_result = rule.validate(intent_result, params)

    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0


def test_intent_mapper_missing_data_handling():
    """Test that intent mapper properly handles missing data."""
    mapper = IntentMapper()

    # Test ADD_TASK with missing description
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    intent_result.parameters.__dict__['task_description'] = None

    result = mapper.execute_intent(intent_result)

    assert result.success is False
    assert 'description' in result.message.lower() or 'required' in result.message.lower()

    # Test UPDATE_TASK with missing ID
    intent_result = IntentResult(IntentType.UPDATE_TASK, required_parameters=['task_id'])
    intent_result.parameters.__dict__['task_id'] = None

    result = mapper.execute_intent(intent_result)

    assert result.success is False
    assert 'id' in result.message.lower() or 'required' in result.message.lower()

    # Test COMPLETE_TASK with missing ID
    intent_result = IntentResult(IntentType.COMPLETE_TASK, required_parameters=['task_id'])
    intent_result.parameters.__dict__['task_id'] = None

    result = mapper.execute_intent(intent_result)

    assert result.success is False
    assert 'id' in result.message.lower() or 'required' in result.message.lower()


def test_validation_result_structure():
    """Test that validation result has correct structure."""
    result = ValidationResult(is_valid=True)
    assert hasattr(result, 'is_valid')
    assert hasattr(result, 'errors')
    assert hasattr(result, 'safe_fallback')
    assert result.is_valid is True
    assert isinstance(result.errors, list)
    assert result.safe_fallback is None


def test_behavior_rules_integration_with_missing_data():
    """Test behavior rules work correctly with missing data scenarios."""
    from src.services.behavior_rules import behavior_engine

    # Test validation with missing required parameter
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {}  # Missing required parameter

    validation_result = behavior_engine.validate_intent_execution(intent_result, params)

    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0 or validation_result.safe_fallback is not None


if __name__ == "__main__":
    test_parameter_validation_rule_contract()
    test_id_validation_rule_contract()
    test_intent_mapper_missing_data_handling()
    test_validation_result_structure()
    test_behavior_rules_integration_with_missing_data()
    print("All missing data validation contract tests passed!")