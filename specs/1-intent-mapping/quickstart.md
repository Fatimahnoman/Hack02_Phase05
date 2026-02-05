# Quickstart: Intent Mapping & Behavior Rules

## Setup

1. Ensure you have Python 3.11+ installed
2. Install required dependencies:
   ```bash
   pip install anthropic python-mcp
   ```

## Running the Intent Mapper

1. Initialize the intent detector:
   ```python
   from agents.intent_detector import IntentDetector

   detector = IntentDetector()
   ```

2. Map user input to intents:
   ```python
   user_message = "add a new task to buy groceries"
   intent = detector.detect(user_message)
   print(f"Detected intent: {intent.type}")
   ```

3. Execute appropriate MCP tool based on intent:
   ```python
   from services.intent_mapping import execute_intent

   result = execute_intent(intent)
   print(f"Result: {result}")
   ```

## Testing

Run the full test suite:
```bash
pytest tests/intent_mapping/
```

Run specific intent detection tests:
```bash
pytest tests/intent_detection/test_basic_intents.py
```

## Configuration

The behavior rules are configured in the service layer and include:
- Validation of required parameters before tool execution
- Guarded execution to prevent unauthorized system changes
- Proper error handling and logging