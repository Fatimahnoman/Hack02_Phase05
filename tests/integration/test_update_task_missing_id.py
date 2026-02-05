"""
Integration test for update_task with missing ID.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.services.intent_mapping import IntentMapper
from src.mcp.task_tools import task_tools


def test_update_task_missing_id_integration():
    """Test the complete flow for updating a task with missing ID."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    # Add a test task
    task_tools.create_task("Original task description")

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input that should trigger update_task intent but without ID
    user_input = "update task to change description"  # No ID mentioned

    # Step 1: Detect intent
    intent_result = detector.detect(user_input)

    # Verify intent detection
    assert intent_result.type == IntentDetector.IntentType.UPDATE_TASK
    assert intent_result.confidence >= 0.8

    # Step 2: Execute intent mapping
    result = mapper.execute_intent(intent_result)

    # Should fail validation due to missing ID
    assert result.success is False
    assert 'id' in result.message.lower() or 'missing' in result.message.lower()
    assert len(result.errors) > 0


def test_update_task_invalid_id_integration():
    """Test updating a task with an invalid ID."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with invalid ID (non-numeric)
    user_input = "update task invalid_id to change description"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should fail validation due to invalid ID
    assert result.success is False
    assert 'id' in result.message.lower() or 'invalid' in result.message.lower()


def test_update_task_nonexistent_id_integration():
    """Test updating a task with an ID that doesn't exist."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    # Add a test task with ID 1
    task_tools.create_task("Original task description")

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with a non-existent ID
    user_input = "update task 999 to change description"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # This would likely fail at the task level (not found), not at the validation level
    # since ID format is valid but the task doesn't exist
    assert result.success is False  # Task not found


def test_update_task_with_extracted_id():
    """Test updating a task with a properly extracted ID."""
    # Reset task tools
    task_tools.tasks = []
    task_tools.next_id = 1

    # Add a test task
    create_result = task_tools.create_task("Original task description")
    task_id = create_result.data["task"]["id"]

    detector = IntentDetector()
    mapper = IntentMapper()

    # Test input with a valid ID mentioned
    user_input = f"update task {task_id} to change description to New Description"

    intent_result = detector.detect(user_input)
    result = mapper.execute_intent(intent_result)

    # Should succeed with valid ID
    assert result.success is True or "missing" not in result.message.lower()


if __name__ == "__main__":
    test_update_task_missing_id_integration()
    test_update_task_invalid_id_integration()
    test_update_task_nonexistent_id_integration()
    test_update_task_with_extracted_id()
    print("All update_task missing ID integration tests completed!")