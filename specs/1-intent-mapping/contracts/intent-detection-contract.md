# Intent Detection Contract

## Overview
Defines the contract for detecting user intents from natural language input and mapping them to specific actions.

## Intent Detection Interface

### detect_intent(input: str) -> IntentResult
Detects the user's intent from natural language input.

#### Parameters
- **input** (string, required): Natural language text input from user

#### Returns
- **IntentResult** (object):
  - **type** (string): One of ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task', 'help', 'unknown']
  - **confidence** (float): Confidence score between 0.0 and 1.0
  - **parameters** (object, optional): Additional parameters extracted from input
  - **required_parameters** (array): List of missing required parameters

#### Example Request
```json
{
  "input": "add a new task to buy groceries"
}
```

#### Example Response
```json
{
  "type": "add_task",
  "confidence": 0.95,
  "parameters": {
    "task_description": "buy groceries"
  },
  "required_parameters": []
}
```

## Intent Execution Interface

### execute_intent(intent: IntentResult) -> ExecutionResult
Executes the appropriate action based on the detected intent.

#### Parameters
- **intent** (IntentResult, required): Result from detect_intent

#### Returns
- **ExecutionResult** (object):
  - **success** (boolean): Whether the execution was successful
  - **message** (string): Human-readable result message
  - **data** (object, optional): Any returned data from the action
  - **errors** (array, optional): List of errors if execution failed

#### Example Request
```json
{
  "type": "add_task",
  "parameters": {
    "task_description": "buy groceries"
  }
}
```

#### Example Response
```json
{
  "success": true,
  "message": "Task 'buy groceries' has been added successfully",
  "data": {
    "task_id": "12345",
    "status": "created"
  }
}
```

## Error Responses

### Validation Error
Returned when required parameters are missing or invalid.

```json
{
  "success": false,
  "message": "Missing required parameter: task_description",
  "errors": [
    {
      "code": "MISSING_PARAMETER",
      "field": "task_description",
      "message": "Task description is required"
    }
  ]
}
```

### Unauthorized Action Error
Returned when the intent would perform an unauthorized action.

```json
{
  "success": false,
  "message": "This action is not permitted by your current access level",
  "errors": [
    {
      "code": "UNAUTHORIZED_ACTION",
      "message": "Attempted unauthorized system modification prevented"
    }
  ]
}
```