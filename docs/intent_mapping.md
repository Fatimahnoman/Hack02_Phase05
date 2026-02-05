# Intent Mapping & Behavior Rules

## Overview
The Intent Mapping & Behavior Rules system provides intelligent processing of natural language inputs to detect user intentions and map them to appropriate actions. The system implements guarded behavior rules to ensure safe and predictable operation.

## Features

### Intent Detection
- **add_task**: Recognizes requests to create new tasks
- **list_tasks**: Recognizes requests to view existing tasks
- **update_task**: Recognizes requests to modify tasks
- **complete_task**: Recognizes requests to mark tasks as complete
- **delete_task**: Recognizes requests to remove tasks
- **help**: Recognizes requests for assistance

### Behavior Rules
- **Guarded Execution**: Prevents unauthorized actions
- **Parameter Validation**: Ensures required data is provided
- **Safe Fallbacks**: Handles invalid inputs gracefully
- **ID Validation**: Ensures task IDs are valid

### Supported Commands

#### Adding Tasks
- "add a new task to buy groceries"
- "create a task to walk the dog"
- "make a task to finish report"

#### Listing Tasks
- "show me my tasks"
- "list my tasks"
- "what are my tasks"
- "show my completed tasks"

#### Updating Tasks
- "update task 5 to change description"
- "modify task 10 to walk the cat"

#### Completing Tasks
- "mark task 3 as complete"
- "complete task 1"
- "finish task 7"

#### Deleting Tasks
- "delete task 2"
- "remove task 4"

#### Help
- "help"
- "what can you do"

## Architecture

### Components
- **Intent Detector**: Parses natural language and detects intent
- **Intent Mapper**: Maps detected intents to MCP tool calls
- **Behavior Engine**: Enforces safety and validation rules
- **MCP Task Tools**: Executes actual task operations

### Flow
1. User input is processed by Intent Detector
2. Detected intent and parameters are validated
3. Validated intent is mapped to appropriate MCP tool
4. MCP tool executes the requested operation
5. Results are returned to user

## Configuration

The system can be configured to allow or disallow specific intent types by modifying the `AllowedActionsRule` configuration.

## Error Handling

- Invalid inputs return safe fallback responses
- Missing parameters trigger clarification requests
- Unauthorized actions are blocked with appropriate messages
- System errors are logged and safe responses returned

## Testing

The system includes:
- Contract tests for interface compliance
- Integration tests for complete workflows
- Unit tests for individual components

Run tests with: `pytest tests/`