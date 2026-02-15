# Implementation Plan: Phase V Part A – Intermediate & Advanced Features

**Branch**: `004-phase-v-features` | **Date**: 2026-02-15 | **Spec**: [004-phase-v-features/spec.md](spec.md)
**Input**: Feature specification from `/specs/004-phase-v-features/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan extends the Phase IV Todo Chatbot with intermediate and advanced features: priorities, tags, search/filter/sort capabilities, recurring tasks, and due date reminders. The implementation follows an event-driven architecture using Dapr building blocks to maintain loose coupling between services. The new features enhance the existing chat interface with natural language processing while maintaining backward compatibility with Phase IV functionality.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Dapr SDK, Pydantic, Celery (for background tasks)
**Storage**: PostgreSQL via Dapr State Management (Neon), Redis for temporary storage
**Testing**: pytest, Dapr integration tests, FastAPI test client
**Target Platform**: Kubernetes (Minikube local → AKS/GKE/OKE cloud)
**Project Type**: Event-driven microservices with existing monolith extension
**Performance Goals**: <500ms task operations, ±30s reminder accuracy, 1000+ events/min
**Constraints**: Event-driven architecture, Dapr abstraction compliance, natural language processing
**Scale/Scope**: Support for 10k+ tasks per user, horizontal scaling for reminder processing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Event-Driven Architecture Compliance**: All inter-service communication must be asynchronous via Kafka/Dapr Pub/Sub
**Dapr Building Blocks**: All infrastructure interactions must use Dapr sidecars (Pub/Sub, State, Secrets, Service Invocation)
**Microservices Boundaries**: Services must be independently scalable and resilient to restarts
**Security & Portability**: All secrets must be via Dapr/Kubernetes secrets, no hardcoded values
**Technology Stack**: Must use FastAPI + SQLModel + Neon PostgreSQL + Redpanda/Kafka + Dapr
**Development Discipline**: Every artifact must trace back to a validated task, no freestyle coding

**Constitution Check Result**: PASS - All principles are satisfied by the proposed architecture.

## Project Structure

### Documentation (this feature)

```text
specs/004-phase-v-features/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
├── dapr-components/     # Dapr component definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extension to existing structure)
```text
backend/
├── src/
│   ├── models/          # Extended data models with priority, tags, due dates, etc.
│   │   ├── task.py      # Enhanced Task model with priority, tags, due_date, etc.
│   │   ├── recurring_task.py  # Recurring task pattern model
│   │   └── reminder.py  # Reminder model
│   ├── services/        # Business logic for new features
│   │   ├── task_service.py      # Enhanced task operations
│   │   ├── recurring_task_service.py  # Recurring task management
│   │   ├── reminder_service.py  # Reminder scheduling and delivery
│   │   └── search_service.py    # Search, filter, sort operations
│   ├── dapr/            # Dapr client utilities
│   │   ├── client.py    # Dapr client wrapper
│   │   └── pubsub.py    # Event publishing/subscribing utilities
│   ├── events/          # Event schemas and handlers
│   │   ├── schemas.py   # Pydantic models for events
│   │   └── handlers.py  # Event processing logic
│   ├── api/             # API routes for new features
│   │   ├── task_router.py       # Extended task endpoints
│   │   └── recurring_router.py  # Recurring task endpoints
│   ├── nlp/             # Natural language processing for chat commands
│   │   └── intent_parser.py     # Intent recognition for new features
│   ├── database/        # Database configuration
│   ├── config.py        # Configuration settings
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── dapr-integration/
│   └── contract/
└── requirements.txt     # Dependencies

dapr-components/
├── statestore.yaml      # PostgreSQL state store component
├── pubsub.yaml          # Kafka/Redpanda pub/sub component
└── secrets.yaml         # Kubernetes secrets component
```

**Structure Decision**: The new features will extend the existing chat-api service rather than creating separate microservices initially. This approach allows for faster development and easier integration with the existing chat interface while maintaining the option to split into separate services later if needed. Event-driven communication will still be maintained through Dapr Pub/Sub for recurring tasks and reminders.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | | |
