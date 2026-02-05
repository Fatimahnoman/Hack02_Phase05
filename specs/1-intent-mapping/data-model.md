# Data Model: Intent Mapping & Behavior Rules

## Intent Types
- **add_task**: Represents user request to create a new task
  - fields: task_description (required), priority (optional), due_date (optional)
  - validation: task_description must be non-empty string

- **list_tasks**: Represents user request to view existing tasks
  - fields: None required
  - validation: No validation needed

- **update_task**: Represents user request to modify existing task
  - fields: task_id (required), updates (required dict)
  - validation: task_id must be valid, updates must contain valid fields

- **complete_task**: Represents user request to mark task as completed
  - fields: task_id (required)
  - validation: task_id must be valid

- **delete_task**: Represents user request to remove a task
  - fields: task_id (required)
  - validation: task_id must be valid

- **help**: Represents user request for assistance
  - fields: None required
  - validation: No validation needed

- **unknown**: Represents unrecognized user input
  - fields: original_input (for logging)
  - validation: Always triggered when no other intent matches

## Action Mapping
- **Intent-Tool Link**: Links detected intents to specific MCP tool calls
  - fields: intent_type, mcp_tool_name, parameter_mapping
  - validation: Must have valid MCP tool reference

## Guarded Behavior Rule
- **Authorized Actions**: Defines allowed MCP tools and parameters
  - fields: allowed_tools, restricted_parameters, validation_rules
  - validation: Prevents execution of unauthorized operations

## Log Entry
- **Intent Log**: Records detected intents and actions taken
  - fields: timestamp, user_input, detected_intent, mcp_tool_called, result_status
  - validation: Timestamp must be current, intent must be valid type