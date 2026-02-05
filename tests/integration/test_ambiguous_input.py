"""
Integration test for ambiguous input handling.
"""
import pytest
from src.agents.intent_detector import IntentDetector
from src.services.intent_mapping import IntentMapper
from src.services.behavior_rules import behavior_engine


def test_ambiguous_input_detection():
    """Test that ambiguous inputs are handled gracefully."""
    detector = IntentDetector()
    mapper = IntentMapper()

    # Test inputs that could be ambiguous or unclear
    ambiguous_inputs = [
        "do something",
        "maybe later",
        "what?",
        "hmm",
        "not sure",
        "perhaps yes",
        "maybe tasks"
    ]

    for ambiguous_input in ambiguous_inputs:
        # Detect intent
        intent_result = detector.detect(ambiguous_input)

        # The detector should handle ambiguous inputs gracefully
        # Either classify as UNKNOWN or as the best possible match
        assert intent_result is not None
        assert intent_result.type is not None

        # Execute mapping
        result = mapper.execute_intent(intent_result)

        # The system should respond gracefully without crashing
        assert result is not None
        assert hasattr(result, 'success')


def test_input_with_multiple_possible_intents():
    """Test handling of inputs that could match multiple intents."""
    detector = IntentDetector()
    mapper = IntentMapper()

    # Inputs that might match multiple patterns
    multi_intent_inputs = [
        "list my completed tasks and add a new one",
        "update and delete this task",
        "help me show tasks"
    ]

    for multi_input in multi_intent_inputs:
        intent_result = detector.detect(multi_input)

        # Should pick the most dominant or first matching intent
        assert intent_result.type is not None

        result = mapper.execute_intent(intent_result)

        # Should handle gracefully without error
        assert result is not None


def test_partial_and_unclear_commands():
    """Test handling of partial or unclear commands."""
    detector = IntentDetector()
    mapper = IntentMapper()

    partial_inputs = [
        "add",
        "update",
        "complete",
        "delete",
        "task",
        "show",
        "the",
        "a"
    ]

    for partial_input in partial_inputs:
        intent_result = detector.detect(partial_input)

        # Execute mapping
        result = mapper.execute_intent(intent_result)

        # Should handle gracefully, possibly returning error about missing info
        assert result is not None


def test_low_confidence_input_handling():
    """Test handling of low-confidence detections."""
    detector = IntentDetector()

    # While our detector doesn't currently return low confidence for partial inputs,
    # we'll test how the system handles inputs that might have been low confidence
    weak_inputs = [
        "um",
        "...",
        "maybe",
        "possibly",
        "perhaps"
    ]

    for weak_input in weak_inputs:
        intent_result = detector.detect(weak_input)

        # Even low-confidence inputs should be handled gracefully
        assert intent_result.type is not None


if __name__ == "__main__":
    test_ambiguous_input_detection()
    test_input_with_multiple_possible_intents()
    test_partial_and_unclear_commands()
    test_low_confidence_input_handling()
    print("All ambiguous input handling tests completed!")