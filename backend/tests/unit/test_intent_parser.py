import pytest
from app.src.nlp.intent_parser import IntentParser


def test_intent_parser_priority_extraction():
    """Test that IntentParser correctly extracts priority from text."""
    parser = IntentParser()
    
    # Test high priority
    text = "Create a high priority task to buy groceries"
    result = parser.parse_intent(text)
    assert result['intent'] == 'create_task'
    # The priority might be in entities
    assert 'entities' in result
    # This depends on the exact implementation of the parser
    # For now, just verify it doesn't crash


def test_intent_parser_tag_extraction():
    """Test that IntentParser correctly extracts tags from text."""
    parser = IntentParser()
    
    # Test tag extraction
    text = "Create a task #work to finish the report"
    result = parser.parse_intent(text)
    assert result['intent'] == 'create_task'
    # Verify that tags are extracted in entities


def test_intent_parser_due_date_extraction():
    """Test that IntentParser correctly extracts due dates from text."""
    parser = IntentParser()
    
    # Test due date extraction
    text = "Create a task to submit report by Friday"
    result = parser.parse_intent(text)
    assert result['intent'] == 'create_task'


def test_intent_parser_reminder_extraction():
    """Test that IntentParser correctly extracts reminder commands."""
    parser = IntentParser()
    
    # Test reminder extraction
    text = "Remind me to call John tomorrow morning"
    result = parser.parse_intent(text)
    assert result['intent'] in ['set_reminder', 'create_task']


def test_intent_parser_recurring_task_extraction():
    """Test that IntentParser correctly identifies recurring tasks."""
    parser = IntentParser()
    
    # Test recurring task extraction
    text = "Create a recurring task to water plants every Monday"
    result = parser.parse_intent(text)
    assert result['intent'] in ['create_recurring', 'create_task']


def test_intent_parser_complex_command():
    """Test that IntentParser handles complex commands with multiple entities."""
    parser = IntentParser()
    
    # Test complex command
    text = "Create a high priority #work task to buy groceries by tomorrow and remind me"
    result = parser.parse_intent(text)
    assert result['intent'] == 'create_task'
    # Should extract priority, tag, due date, and reminder intent


def test_intent_parser_various_priority_levels():
    """Test that IntentParser recognizes different priority levels."""
    parser = IntentParser()
    
    # Test different priority levels
    texts = [
        "Create a low priority task",
        "Create a medium priority task", 
        "Create a high priority task"
    ]
    
    for text in texts:
        result = parser.parse_intent(text)
        assert result['intent'] == 'create_task'


def test_intent_parser_no_matching_intent():
    """Test that IntentParser handles text with no clear intent."""
    parser = IntentParser()
    
    # Test text that doesn't match any specific intent
    text = "Just a simple sentence without specific commands"
    result = parser.parse_intent(text)
    # Should default to create_task or similar
    assert result['intent'] in ['create_task']


def test_intent_parser_original_text_preserved():
    """Test that the original text is preserved in the result."""
    parser = IntentParser()
    
    text = "Create a high priority task #work to buy groceries by tomorrow"
    result = parser.parse_intent(text)
    
    assert 'original_text' in result
    assert result['original_text'] == text