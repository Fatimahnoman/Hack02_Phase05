# Implementation Plan: Conversational AI Layer using OpenAI Agents SDK

**Branch**: `001-ai-agents-sdk` | **Date**: 2026-01-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-agents-sdk/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of OpenAI Agents SDK integration to enhance the existing chat API with context-aware AI responses. The system will reconstruct conversation context from database messages and feed it to the AI agent for coherent, multi-turn conversations. The integration maintains the stateless architecture by fetching conversation history from the database on each request before invoking the agent.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Neon Serverless PostgreSQL driver
**Storage**: Neon Serverless PostgreSQL database (existing)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web API backend extension
**Performance Goals**: Under 10 seconds for 95% of agent responses
**Constraints**: Text-only responses (no tool usage), must maintain stateless operation, conversation context built from database records
**Scale/Scope**: Support concurrent chat requests with AI processing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase Compliance**: The feature aligns with Phase III+ requirements as it implements:
- AI and agent frameworks (permitted in Phase III+ according to constitution)
- Building upon Phase II infrastructure (Python FastAPI, SQLModel, PostgreSQL)
- Maintaining existing architecture patterns

**Constitution Compliance Check**:
- ✅ Uses approved AI/agent frameworks for Phase III+ (OpenAI Agents SDK)
- ✅ Builds upon Phase II infrastructure (Python/REST API, SQLModel, PostgreSQL)
- ✅ No unauthorized technologies from other phases
- ✅ Maintains stateless architecture as required
- ✅ Properly layered architecture following existing patterns

**Post-Design Check**:
- ✅ Data model aligns with AI integration requirements
- ✅ API contract maintains backward compatibility
- ✅ Implementation approach maintains phase compliance
- ✅ No introduction of unauthorized technologies

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-agents-sdk/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py      # Conversation data model (existing)
│   │   └── message.py           # Message data model (existing)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py      # Enhanced with agent integration
│   │   ├── conversation_service.py # Conversation management (existing)
│   │   ├── ai_agent_service.py  # New: AI agent integration service
│   │   └── context_builder.py   # New: Conversation context building
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat_router.py       # Updated to use AI agent service
│   └── main.py                  # FastAPI app entry point (existing)
└── tests/
    ├── unit/
    │   ├── models/
    │   ├── services/
    │   │   ├── test_ai_agent_service.py
    │   │   └── test_context_builder.py
    │   └── api/
    ├── integration/
    │   └── api/
    │       └── test_ai_chat_integration.py
    └── conftest.py
```

**Structure Decision**: Extending existing Option 2: Web application with backend-only structure to add AI capabilities. The enhancement maintains existing architecture while adding AI-specific services (ai_agent_service.py and context_builder.py) that integrate with the existing chat service and router.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
