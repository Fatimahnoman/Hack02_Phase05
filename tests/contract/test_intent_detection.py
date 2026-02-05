"""
Contract test for intent detection functionality.
"""
import pytest
from src.agents.intent_detector import IntentDetector, IntentType


def test_intent_detection_contract():
    """Test that intent detection works as expected for each intent type."""
    detector = IntentDetector()

    # Test add_task intent
    result = detector.detect("add a new task to buy groceries")
    assert result.type == IntentType.ADD_TASK
    assert result.confidence >= 0.8
    assert hasattr(result.parameters, 'task_description')

    # Test list_tasks intent
    result = detector.detect("show me my tasks")
    assert result.type == IntentType.LIST_TASKS
    assert result.confidence >= 0.8

    # Test update_task intent
    result = detector.detect("update task 5 to change description")
    assert result.type == IntentType.UPDATE_TASK
    assert result.confidence >= 0.8

    # Test complete_task intent
    result = detector.detect("mark task 3 as complete")
    assert result.type == IntentType.COMPLETE_TASK
    assert result.confidence >= 0.8

    # Test delete_task intent
    result = detector.detect("delete task 2")
    assert result.type == IntentType.DELETE_TASK
    assert result.confidence >= 0.8

    # Test help intent
    result = detector.detect("help me")
    assert result.type == IntentType.HELP
    assert result.confidence >= 0.8

    # Test unknown intent
    result = detector.detect("random text that doesn't match anything")
    assert result.type == IntentType.UNKNOWN
    assert result.confidence < 0.5


def test_intent_detection_edge_cases():
    """Test edge cases for intent detection."""
    detector = IntentDetector()

    # Empty input
    result = detector.detect("")
    assert result.type == IntentType.UNKNOWN

    # None input
    result = detector.detect("   ")
    assert result.type == IntentType.UNKNOWN

    # Mixed case
    result = detector.detect("ADD A NEW TASK")
    assert result.type == IntentType.ADD_TASK

    # Plural forms
    result = detector.detect("show my todos")
    assert result.type == IntentType.LIST_TASKS


if __name__ == "__main__":
    test_intent_detection_contract()
    test_intent_detection_edge_cases()
    print("All contract tests passed!")