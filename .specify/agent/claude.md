# Hackathon Project Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-04

## Active Technologies

- Language/Version: Python 3.11
- Primary Dependencies: anthropic, python-mcp, logging libraries
- Testing: pytest for unit and integration testing
- Target Platform: Linux server
- MCP Framework: For agent-based task management

## Project Structure

```text
src/
├── agents/
│   └── intent_detector.py    # Intent detection logic
├── services/
│   ├── intent_mapping.py     # Maps intents to actions
│   └── behavior_rules.py     # Guarded behavior implementation
├── utils/
│   └── logger.py            # Logging functionality
└── mcp/
    └── task_tools.py        # MCP tool definitions for tasks

specs/1-intent-mapping/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── intent-detection-contract.md
```

## Commands

- Run intent detection: `python -m agents.intent_detector`
- Test intent mapping: `pytest tests/intent_mapping/`
- Execute specific intent: `python -c "from services.intent_mapping import execute_intent; execute_intent(...)"`
- View available MCP tools: `mcp list-tools`

## Code Style

- Follow Python PEP 8 guidelines
- Use type hints for all function parameters and return values
- Write comprehensive docstrings for all public functions
- Log important operations with appropriate log levels
- Handle errors gracefully with informative messages

## Recent Changes

- Intent Mapping & Behavior Rules: Added intent detection and mapping system that accurately identifies user intents (add_task, list_tasks, update_task, complete_task, delete_task, help) and maps them to appropriate MCP tool calls with guarded behavior rules to prevent unauthorized actions.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->