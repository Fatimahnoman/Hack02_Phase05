# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., FastAPI, SQLModel, Dapr SDK or NEEDS CLARIFICATION]
**Storage**: [if applicable, e.g., PostgreSQL via Dapr State, Kafka via Dapr Pub/Sub or N/A]
**Testing**: [e.g., pytest, Dapr integration tests or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Kubernetes, Minikube, AKS/GKE/OKE or NEEDS CLARIFICATION]
**Project Type**: [event-driven microservices - determines source structure]
**Performance Goals**: [domain-specific, e.g., <500ms task ops, 1000+ events/min or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., ±30s reminder accuracy, event-driven architecture or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, horizontal scaling, multi-cloud or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Event-Driven Architecture Compliance**: All inter-service communication must be asynchronous via Kafka/Dapr Pub/Sub
**Dapr Building Blocks**: All infrastructure interactions must use Dapr sidecars (Pub/Sub, State, Secrets, Service Invocation)
**Microservices Boundaries**: Services must be independently scalable and resilient to restarts
**Security & Portability**: All secrets must be via Dapr/Kubernetes secrets, no hardcoded values
**Technology Stack**: Must use FastAPI + SQLModel + Neon PostgreSQL + Redpanda/Kafka + Dapr
**Development Discipline**: Every artifact must trace back to a validated task, no freestyle coding

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
├── dapr-components/     # Dapr component definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── dapr/
│   └── clients/
├── events/
└── cli/

tests/
├── contract/
├── integration/
├── dapr-integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Event-driven microservices
chat-api/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   └── dapr/
├── tests/
└── dapr-component.yaml

recurring-task-service/
├── src/
│   ├── models/
│   ├── services/
│   └── dapr/
├── tests/
└── dapr-component.yaml

notification-service/
├── src/
│   ├── models/
│   ├── services/
│   └── dapr/
├── tests/
└── dapr-component.yaml
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above, ensuring alignment with event-driven architecture and Dapr integration]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., direct Kafka client] | [specific requirement] | [Dapr abstraction insufficient for this case] |
| [e.g., hardcoded secrets] | [specific constraint] | [Dapr/K8s secrets approach not viable] |
