"""
Integration test for add_task with missing details.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.services.intent_mapping import IntentMapper
from src.mcp.task_tools import task_tools


def test_add_task_missing_details_integration():
    """Test the complete flow for adding a task with missing details."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input that should trigger add_task intent but without clear details
    user_input = "add a task"  # No actual description

    # Step 1: Detect intent
    intent_result = detector.detect(user_input)

    # Verify intent detection - should recognize as ADD_TASK but with no description
    assert intent_result.type == IntentDetector.IntentType.ADD_TASK
    assert intent_result.confidence >= 0.8

    # Step 2: Execute intent mapping
    result = mapper.execute_intent(intent_result)

    # Should fail execution due to missing task description
    assert result.success is False
    assert 'description' in result.message.lower() or 'required' in result.message.lower()


def test_add_task_ambiguous_details():
    """Test adding a task with ambiguous or unclear details."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with very unclear description
    user_input = "add something"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect intent but fail execution due to insufficient description
    assert intent_result.type == IntentDetector.IntentType.ADD_TASK
    assert result.success is False
    assert 'description' in result.message.lower() or 'required' in result.message.lower()


def test_add_task_vague_input():
    """Test adding a task with vague input."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test more vague input
    user_input = "add to do"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect intent but fail due to lack of specifics
    assert result.success is False


def test_add_task_with_sufficient_details():
    """Test adding a task with sufficient details to contrast."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with clear description
    user_input = "add a task to buy groceries"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should succeed with clear description
    assert result.success is True
    assert 'buy groceries' in result.message or 'added' in result.message.lower()


def test_add_task_empty_input():
    """Test adding a task with effectively empty input."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test with minimal input
    user_input = "add"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should detect as ADD_TASK but fail execution
    assert intent_result.type == IntentDetector.IntentType.ADD_TASK
    assert result.success is False


if __name__ == "__main__":
    test_add_task_missing_details_integration()
    test_add_task_ambiguous_details()
    test_add_task_vague_input()
    test_add_task_with_sufficient_details()
    test_add_task_empty_input()
    print("All add_task missing details integration tests completed!")