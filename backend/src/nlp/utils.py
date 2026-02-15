from typing import Dict, Any, Optional
from ..models.task import TaskCreate
from ..nlp.intent_parser import IntentParser


def convert_nlp_to_task_create(nlp_result: Dict[str, Any]) -> TaskCreate:
    """Convert NLP result to a TaskCreate object."""
    # Extract the main task content from the original text
    original_text = nlp_result.get('original_text', '')
    
    # Remove intent-specific phrases to get the core task title
    title = extract_task_title(original_text, nlp_result)
    
    # Prepare the task data
    task_data = {
        "title": title,
        "description": "",
        "priority": "medium",  # Default priority
        "user_id": 1  # Default user_id - would come from auth in real app
    }
    
    # Apply extracted entities
    entities = nlp_result.get('entities', {})
    
    # Set priority if mentioned
    if 'priority' in entities:
        task_data['priority'] = entities['priority']
    
    # Set tags if mentioned
    if 'tags' in entities and entities['tags']:
        task_data['tags'] = entities['tags']
    
    # Set due date if mentioned
    if 'due_date' in entities:
        task_data['due_date'] = entities['due_date']
    
    # Set reminder time if mentioned
    if 'reminder_time' in entities:
        # Calculate reminder offset based on due date and reminder time
        # This is a simplified approach
        task_data['reminder_offset'] = 60  # Default to 1 hour before
    
    return TaskCreate(**task_data)


def extract_task_title(original_text: str, nlp_result: Dict[str, Any]) -> str:
    """Extract the core task title from the original text by removing intent-specific phrases."""
    text = original_text.lower()
    
    # Remove common intent phrases
    phrases_to_remove = [
        'create a', 'create', 'make a', 'make', 'add a', 'add', 
        'set', 'make it', 'make this', 'set as', 'set to',
        'high priority', 'medium priority', 'low priority',
        'by ', 'on ', 'before ',
        'remind me', 'reminder to', 'remind about',
        'every ', 'daily', 'weekly', 'monthly'
    ]
    
    # Remove tags
    import re
    text = re.sub(r'#\w+', '', text)
    
    # Remove common phrases
    for phrase in phrases_to_remove:
        text = text.replace(phrase, '')
    
    # Clean up extra spaces
    title = ' '.join(text.split()).strip()
    
    # If the title is empty or too short, use the original text
    if not title or len(title) < 3:
        # Extract the main content by removing the intent parts
        intent = nlp_result.get('intent', '')
        if intent == 'create_task':
            # Just return the original text if it's a simple create task
            title = original_text.strip()
        else:
            # For other intents, try to extract the core task
            title = original_text.strip()
    
    return title


def parse_natural_language_command(command: str) -> TaskCreate:
    """Parse a natural language command and return a TaskCreate object."""
    parser = IntentParser()
    nlp_result = parser.parse_intent(command)
    
    return convert_nlp_to_task_create(nlp_result)