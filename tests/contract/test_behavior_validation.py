"""
Contract test for behavior validation functionality.
"""
import pytest
from src.models.intent_result import IntentResult, IntentType
from src.services.behavior_rules import (
    AuthorizedActionsRule, ParameterValidationRule, IdValidationRule,
    ValidationResult, behavior_engine
)


def test_authorized_actions_rule_contract():
    """Test the authorized actions rule contract."""
    rule = AuthorizedActionsRule()

    # Test authorized intent
    intent_result = IntentResult(IntentType.ADD_TASK)
    validation_result = rule.validate(intent_result, {})
    assert validation_result.is_valid is True

    # Test unauthorized intent
    class MockIntentType:
        CUSTOM_INTENT = "custom_intent"

    # Actually test with an intent that should not be allowed
    # We'll use a mock approach since all our intents are allowed by default
    unauthorized_intent = type('MockIntent', (), {'value': 'malicious_action'})()
    # Instead, we'll test the rule directly with parameters
    fake_intent = type('FakeIntent', (), {'value': 'malicious_action'})()

    # Actually, we need to create a different approach since all our defined intents are allowed
    # The test would work if we tried to execute an unauthorized intent type
    # But since our default list includes all of them, let's modify the test to work differently
    custom_allowed_intents = [IntentType.HELP]  # Only help is allowed
    custom_rule = AuthorizedActionsRule(allowed_intents=custom_allowed_intents)

    # Test allowed intent
    intent_result = IntentResult(IntentType.HELP)
    validation_result = custom_rule.validate(intent_result, {})
    assert validation_result.is_valid is True

    # Test denied intent
    intent_result = IntentResult(IntentType.ADD_TASK)
    validation_result = custom_rule.validate(intent_result, {})
    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0


def test_parameter_validation_rule_contract():
    """Test the parameter validation rule contract."""
    rule = ParameterValidationRule()

    # Test with all required parameters present
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {'task_description': 'Buy groceries'}
    validation_result = rule.validate(intent_result, params)
    assert validation_result.is_valid is True

    # Test with missing required parameters
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {}
    validation_result = rule.validate(intent_result, params)
    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0


def test_id_validation_rule_contract():
    """Test the ID validation rule contract."""
    rule = IdValidationRule()

    # Test with valid ID
    intent_result = IntentResult(IntentType.UPDATE_TASK)
    params = {'task_id': '5'}
    validation_result = rule.validate(intent_result, params)
    assert validation_result.is_valid is True

    # Test with invalid ID
    intent_result = IntentResult(IntentType.UPDATE_TASK)
    params = {'task_id': 'invalid'}
    validation_result = rule.validate(intent_result, params)
    assert validation_result.is_valid is False
    assert len(validation_result.errors) > 0


def test_behavior_engine_contract():
    """Test the behavior engine contract."""
    # Test that the engine validates correctly
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {'task_description': 'Buy groceries'}

    validation_result = behavior_engine.validate_intent_execution(intent_result, params)
    assert validation_result.is_valid is True

    # Test with missing required parameters
    intent_result = IntentResult(IntentType.ADD_TASK, required_parameters=['task_description'])
    params = {}

    validation_result = behavior_engine.validate_intent_execution(intent_result, params)
    assert validation_result.is_valid is False


def test_validation_result_structure():
    """Test that validation result has correct structure."""
    result = ValidationResult(is_valid=True)
    assert hasattr(result, 'is_valid')
    assert hasattr(result, 'errors')
    assert hasattr(result, 'safe_fallback')
    assert result.is_valid is True
    assert isinstance(result.errors, list)


if __name__ == "__main__":
    test_authorized_actions_rule_contract()
    test_parameter_validation_rule_contract()
    test_id_validation_rule_contract()
    test_behavior_engine_contract()
    test_validation_result_structure()
    print("All behavior validation contract tests passed!")