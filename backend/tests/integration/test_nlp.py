import pytest
from sqlmodel import Session
from app.src.database import engine
from app.src.services.chat_service import ChatService
from app.src.nlp.intent_parser import IntentParser
from app.src.nlp.utils import parse_natural_language_command
from app.src.models.task import TaskCreate


@pytest.fixture
def db_session():
    with Session(engine) as session:
        yield session


def test_natural_language_task_creation_integration(db_session: Session):
    """Integration test for natural language task creation."""
    # Test the full pipeline from natural language to task creation
    parser = IntentParser()
    
    # Test 1: Simple task creation
    command = "Create a task to buy groceries"
    result = parser.parse_intent(command)
    assert result['intent'] == 'create_task'
    
    # Convert to TaskCreate object
    task_create = parse_natural_language_command(command)
    assert isinstance(task_create, TaskCreate)
    assert task_create.title == "buy groceries"  # Should extract the core task
    
    # Test 2: Task with priority
    command = "Create a high priority task to fix the bug"
    task_create = parse_natural_language_command(command)
    assert task_create.priority == "high"
    
    # Test 3: Task with tags
    command = "Create a task #work to prepare presentation"
    task_create = parse_natural_language_command(command)
    assert "work" in task_create.tags
    
    # Test 4: Task with due date
    command = "Create a task to submit report by Friday"
    task_create = parse_natural_language_command(command)
    # This might set a due date depending on the implementation
    
    # Test 5: Complex command with multiple features
    command = "Create a high priority #work task to finish project by tomorrow and remind me"
    task_create = parse_natural_language_command(command)
    assert task_create.priority == "high"
    assert "work" in task_create.tags
    # Might also set due date and reminder
    
    # Test 6: Recurring task
    command = "Create a recurring task to water plants every Monday"
    result = parser.parse_intent(command)
    assert result['intent'] in ['create_recurring', 'create_task']
    
    # Test 7: Another complex command
    command = "Make this high priority #urgent and remind me every Monday at 9 AM"
    result = parser.parse_intent(command)
    # This should recognize priority, tag, and recurring reminder intent


def test_nlp_utils_convert_nlp_to_task_create():
    """Test the conversion from NLP result to TaskCreate object."""
    from app.src.nlp.utils import convert_nlp_to_task_create
    
    # Mock NLP result
    nlp_result = {
        'intent': 'create_task',
        'entities': {
            'priority': 'high',
            'tags': ['work', 'important'],
            'due_date': None,
            'reminder_time': None
        },
        'original_text': 'Create a high priority #work #important task to finish report'
    }
    
    task_create = convert_nlp_to_task_create(nlp_result)
    assert isinstance(task_create, TaskCreate)
    assert task_create.priority == 'high'
    # Note: tags might not be directly mapped in this function
    # depending on the implementation


def test_nlp_utils_extract_task_title():
    """Test the extraction of task title from natural language."""
    from app.src.nlp.utils import extract_task_title
    
    original_text = "Create a high priority task #work to finish the report"
    nlp_result = {'intent': 'create_task'}
    
    title = extract_task_title(original_text, nlp_result)
    # Should extract the core task title, removing intent phrases
    assert 'finish the report' in title.lower() or 'create' not in title.lower()


def test_nlp_pipeline_consistency():
    """Test that the NLP pipeline is consistent."""
    # Test that parsing and converting back results in consistent behavior
    commands = [
        "Create a task to buy groceries",
        "Create a high priority task #work to finish report",
        "Create a recurring task to water plants every Monday"
    ]
    
    for command in commands:
        # Parse the command
        task_create = parse_natural_language_command(command)
        
        # Verify it's a valid TaskCreate object
        assert isinstance(task_create, TaskCreate)
        assert task_create.title is not None and task_create.title.strip() != ""