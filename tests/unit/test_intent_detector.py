"""
Unit tests for IntentDetector.
"""
import pytest
from src.agents.intent_detector import IntentDetector, IntentType


def test_intent_detector_initialization():
    """Test that IntentDetector initializes properly."""
    detector = IntentDetector()
    assert detector.keyword_patterns is not None
    assert len(detector.keyword_patterns) > 0


def test_detect_add_task():
    """Test detection of add_task intent."""
    detector = IntentDetector()

    test_inputs = [
        "add a new task to buy groceries",
        "create a task for walking dog",
        "need to finish report",
        "must buy milk"
    ]

    for test_input in test_inputs:
        result = detector.detect(test_input)
        assert result.type == IntentType.ADD_TASK


def test_detect_list_tasks():
    """Test detection of list_tasks intent."""
    detector = IntentDetector()

    test_inputs = [
        "show me my tasks",
        "list my todos",
        "what are my tasks",
        "display my to-dos"
    ]

    for test_input in test_inputs:
        result = detector.detect(test_input)
        assert result.type == IntentType.LIST_TASKS


def test_detect_help():
    """Test detection of help intent."""
    detector = IntentDetector()

    test_inputs = [
        "help",
        "what can you do",
        "how does this work",
        "commands"
    ]

    for test_input in test_inputs:
        result = detector.detect(test_input)
        assert result.type == IntentType.HELP


def test_detect_unknown():
    """Test detection of unknown intent."""
    detector = IntentDetector()

    test_inputs = [
        "random text",
        "this does not match anything",
        "asdfghjkl"
    ]

    for test_input in test_inputs:
        result = detector.detect(test_input)
        assert result.type == IntentType.UNKNOWN


def test_empty_input():
    """Test detection with empty input."""
    detector = IntentDetector()

    result = detector.detect("")
    assert result.type == IntentType.UNKNOWN
    assert result.confidence == 0.0


def test_whitespace_input():
    """Test detection with whitespace-only input."""
    detector = IntentDetector()

    result = detector.detect("   ")
    assert result.type == IntentType.UNKNOWN
    assert result.confidence == 0.0


if __name__ == "__main__":
    test_intent_detector_initialization()
    test_detect_add_task()
    test_detect_list_tasks()
    test_detect_help()
    test_detect_unknown()
    test_empty_input()
    test_whitespace_input()
    print("All intent detector unit tests passed!")