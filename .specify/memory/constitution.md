<!-- SYNC IMPACT REPORT
Version change: 1.2.0 → 2.0.0
Modified principles: All principles have been replaced with Phase V principles
Added sections: Event-Driven Architecture, Dapr Runtime Abstraction, Scalable Microservices, Security & Portability, Performance & Observability, Advanced Features
Removed sections: Previous container-first and AI-assisted generation principles
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
Runtime docs requiring updates:
  - README.md ✅ updated
Follow-up TODOs: None
-->

# Todo Chatbot Event-Driven Microservices Constitution

## Purpose & Vision

This constitution defines the unbreakable architectural, technical, and philosophical foundation for Phase V.  
The goal is to evolve the Phase IV Todo Chatbot into a **production-ready, scalable, event-driven microservices system** that demonstrates:
- Decoupled services communicating solely via events
- Portable infrastructure abstraction with Dapr
- Advanced user features (recurring tasks, reminders, priorities, tags, search/filter/sort)
- Local (Minikube) → Cloud (AKS/GKE/OKE) deployment readiness

All development follows the Agentic Dev Stack:  
Specify → Plan → Tasks → Implement (via Claude Code / AI agents).  
No manual coding. Every line of code must trace back to a validated task.

**Hierarchy of Truth**  
Constitution > Specify > Plan > Tasks > Code

## Core Architectural Principles (Non-Negotiable)

### I. Event-Driven First – Loose Coupling
All inter-service communication MUST be asynchronous via Kafka events (or Dapr Pub/Sub abstraction).  
Direct HTTP calls between services are forbidden except via Dapr Service Invocation.

### II. Dapr as the Runtime Abstraction Layer
Use Dapr sidecars for ALL infrastructure interactions:
- Pub/Sub (Kafka/Redpanda)
- State Management (PostgreSQL/Neon)
- Jobs API (exact-time reminders – preferred over cron bindings)
- Secrets (Kubernetes secretstores)
- Service Invocation (retries, discovery, mTLS)
No direct libraries (kafka-python, psycopg2, etc.) in application code.

### III. Scalable & Production-Grade Microservices
Break features into independent services:
- Chat API (producer + core logic)
- RecurringTaskService
- NotificationService
- (Optional: AuditService, WebSocketService)
Services must be horizontally scalable and restart-resilient.

### IV. Security & Portability by Design
All secrets (Neon creds, Redpanda creds, API keys) via Dapr Secrets or Kubernetes Secrets – never env vars or code.  
Configuration must be YAML-driven (Dapr components) for easy swap (Kafka → RabbitMQ, Neon → other DB).

### V. Performance, Reliability & Observability
Async Python everywhere. Target <500ms task ops, exact reminder timing (±30s).  
Built-in retries, circuit breakers (via Dapr).  
Full audit trail via task-events topic.  
Observability: logs, metrics, tracing enabled (Dapr defaults + kubectl).

### VI. Development Discipline
Agentic workflow only: No freestyle coding.  
Every code artifact references a task ID and constitution principle.  
90%+ test coverage target for new features.  
Local-first validation (Minikube + Redpanda Docker) before cloud.

## Technology Stack Constraints (Fixed – No Deviations)

- Backend: FastAPI + SQLModel (Phase IV base)
- Database: Neon PostgreSQL (via Dapr State where possible)
- Messaging: Kafka-compatible (Redpanda preferred – serverless cloud or Strimzi self-hosted)
- Runtime: Dapr (full building blocks)
- Orchestration: Kubernetes (Minikube local → AKS/GKE/OKE cloud)
- CI/CD: GitHub Actions
- Deployment: Helm charts (extend Phase IV)
- Monitoring/Logging: kubectl logs + Dapr metrics (Prometheus optional)

### Explicit Prohibitions
- Polling loops for reminders/recurring (use Dapr Jobs API or event triggers)
- Direct Kafka client libraries in app code
- Hardcoded URLs, connection strings, or secrets
- Monolithic blocking operations
- Vendor lock-in (Dapr abstraction mandatory)

## Key Domain Rules & Constraints

- Recurring Tasks: Max 10 future instances, auto-create next on completion event
- Reminders: Exact-time scheduling (Dapr Jobs API), remind offset configurable, in-chat delivery (stub)
- Priorities: low/medium/high enum
- Tags: max 5 per task, filterable/searchable
- Search/Filter/Sort: full-text, paginated, indexed queries
- Events: Fixed schemas (Pydantic validated) – task-events, reminders, task-updates
- Real-time Sync: Broadcast via task-updates topic + WebSocket

## Non-Functional Targets

- Task CRUD latency: <500 ms
- Reminder accuracy: within ±30 seconds
- Event throughput: 1000+ events/min (partitioned)
- Restart resilience: No data loss on pod restarts
- Multi-cloud portability: Swap Kafka/DB via YAML only

## Development Workflow

### Pre-Development Requirements
- Specifications must detail event schemas and service boundaries
- Dapr component configurations must be planned in advance
- Local Minikube + Dapr environment must be validated before deployment
- Event-driven architecture patterns must be verified in design
- Dapr sidecar configurations must follow security best practices

### Code Review Requirements
- All services must communicate only via Dapr building blocks
- Event schemas must be validated with Pydantic models
- Service boundaries must align with domain responsibilities
- Dapr component configurations must be reviewed for security
- Microservice scalability patterns must be verified

### Quality Gates
- All services must pass integration tests with Dapr sidecars
- Event processing must maintain data consistency
- Cross-service communication must be verified via pub/sub
- Failure scenarios must be tested (sidecar down, network partitions)
- End-to-end functionality must be verified across all services

## Governance

This constitution supersedes all other development practices and must be followed for all event-driven microservices activities. Amendments require documentation of the change, approval from project stakeholders, and a migration plan for existing implementations. All pull requests and code reviews must verify compliance with these principles.

Any deviation requires explicit update to this constitution (via speckit.plan proposal).  
All agents MUST reference constitution principles in every decision/output.

**Version**: 2.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-15
