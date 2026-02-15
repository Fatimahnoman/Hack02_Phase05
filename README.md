# Evolution of Todo - Phase V: Event-Driven Microservices with Dapr

This project implements a production-ready, scalable, event-driven microservices system as specified in Phase V of the Evolution of Todo project. The system demonstrates decoupled services communicating solely via events, portable infrastructure abstraction with Dapr, and advanced user features with local (Minikube) to cloud (AKS/GKE/OKE) deployment readiness.

## Features

- User registration and authentication
- Todo management (create, read, update, delete)
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive web interface
- **NEW**: Event-driven architecture with loose coupling
- **NEW**: Dapr runtime abstraction for infrastructure services
- **NEW**: Advanced task features: recurring tasks, reminders, priorities, tags
- **NEW**: Search, filter, and sort capabilities
- **NEW**: Real-time synchronization via WebSocket
- **NEW**: Horizontal scalability and cloud-native deployment

## Tech Stack

### Backend
- Python 3.11
- FastAPI + SQLModel
- Neon Serverless PostgreSQL (via Dapr State Management)
- Dapr (Distributed Application Runtime)
- Kafka/Redpanda (via Dapr Pub/Sub)
- Better Auth
- Uvicorn (ASGI server)

### Frontend
- Next.js 14
- React
- TypeScript
- Axios for API calls

### Infrastructure
- Kubernetes (Minikube local → AKS/GKE/OKE cloud)
- Helm Charts
- Dapr Components (Pub/Sub, State Management, Secrets)
- GitHub Actions (CI/CD)

## Setup

### Prerequisites

1. Install Docker Desktop
2. Install kubectl
3. Install Helm
4. Install Dapr CLI
5. Set up Minikube

### Local Development Setup

1. Initialize Dapr:
   ```bash
   dapr init
   ```

2. Start Minikube:
   ```bash
   minikube start
   ```

3. Install Dapr to Kubernetes:
   ```bash
   dapr init -k
   ```

4. Deploy the application:
   ```bash
   helm install todo-chatbot charts/todo-chatbot/
   ```

## Architecture

### Service Components

- **Chat API**: Handles user requests and produces events
- **RecurringTaskService**: Manages recurring task creation and scheduling
- **NotificationService**: Handles reminders and notifications
- **(Optional) AuditService**: Tracks all system events
- **(Optional) WebSocketService**: Manages real-time updates

### Event-Driven Patterns

- All inter-service communication via Kafka events (abstracted through Dapr Pub/Sub)
- Fixed event schemas with Pydantic validation
- Task lifecycle events: task-created, task-updated, task-completed, task-deleted
- Reminder events for scheduled notifications
- Audit trail via task-events topic

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Todos
- `GET /api/todos/` - Get all todos for authenticated user
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo
- `PATCH /api/todos/{id}/status` - Update todo completion status

### Advanced Features
- `POST /api/todos/recurring` - Create recurring tasks
- `GET /api/todos/search` - Search, filter, and sort todos
- `PATCH /api/todos/{id}/priority` - Update task priority
- `PUT /api/todos/{id}/tags` - Add/remove tags from tasks

## Dapr Components

### State Store (PostgreSQL via Neon)
Configured in `dapr-components/statestore.yaml`

### Pub/Sub (Kafka/Redpanda)
Configured in `dapr-components/pubsub.yaml`

### Secret Store (Kubernetes)
Configured in `dapr-components/secrets.yaml`

## Environment Variables

### Backend
- `DAPR_HOST`: Dapr sidecar host (usually localhost)
- `DAPR_HTTP_PORT`: Dapr sidecar HTTP port
- `NEON_DB_CONNECTION_STRING`: Connection string retrieved via Dapr secrets
- `REDPANDA_BROKER_LIST`: Broker list retrieved via Dapr secrets

### Frontend
- `NEXT_PUBLIC_API_URL`: Base URL for the backend API

## Project Structure

```
backend/
├── chat-api/            # Main API service
│   ├── src/
│   │   ├── models/     # Data models
│   │   ├── services/   # Business logic
│   │   ├── dapr/       # Dapr client utilities
│   │   ├── events/     # Event schemas and handlers
│   │   └── api/        # API routes
│   ├── tests/
│   └── dapr-component.yaml
├── recurring-task-service/  # Recurring task management
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── dapr/
│   ├── tests/
│   └── dapr-component.yaml
├── notification-service/    # Notification management
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── dapr/
│   ├── tests/
│   └── dapr-component.yaml
└── requirements.txt     # Dependencies

frontend/
├── src/
│   ├── components/  # React components
│   ├── pages/       # Next.js pages
│   ├── services/    # API services
│   ├── types/       # TypeScript types
│   └── hooks/       # React hooks
├── package.json     # Dependencies
└── next.config.js   # Next.js configuration

dapr-components/
├── statestore.yaml      # PostgreSQL state store component
├── pubsub.yaml          # Kafka/Redpanda pub/sub component
└── secrets.yaml         # Kubernetes secrets component

charts/
└── todo-chatbot/        # Helm chart for deployment

specs/
└── 005-event-driven-microservices/  # Specification documents
    ├── spec.md         # Feature specification
    ├── plan.md         # Implementation plan
    ├── data-model.md   # Data model
    ├── dapr-components/ # Dapr component definitions
    ├── contracts/      # API contracts
    └── tasks.md        # Implementation tasks

history/
└── prompts/           # Prompt History Records
    └── 005-event-driven-microservices/
```

## Event-Driven Architecture Features

### Loose Coupling
- All inter-service communication is asynchronous via Dapr Pub/Sub
- Services can scale independently
- Failure in one service doesn't directly impact others

### Dapr Runtime Abstraction
- Infrastructure concerns abstracted through Dapr building blocks
- Portable across different platforms (local, cloud)
- Consistent patterns for state management, pub/sub, and secrets

### Advanced Task Capabilities
- Recurring tasks with configurable intervals
- Priority levels (low/medium/high)
- Tagging system (up to 5 tags per task)
- Full-text search, filtering, and sorting
- Configurable reminders with exact-time scheduling

### Scalability & Reliability
- Horizontal pod autoscaling based on load
- Built-in retries and circuit breakers via Dapr
- Event-driven processing ensures resilience
- Full audit trail via event logging

## Running the Application

### Local Development
1. Ensure prerequisites are installed (Docker, kubectl, Helm, Dapr)
2. Initialize Dapr locally: `dapr init`
3. Start Minikube: `minikube start`
4. Install Dapr to Kubernetes: `dapr init -k`
5. Deploy the application: `helm install todo-chatbot charts/todo-chatbot/`
6. Access the application: `minikube service todo-chatbot-frontend`

### Cloud Deployment
1. Configure your cloud Kubernetes cluster (AKS/GKE/OKE)
2. Install Dapr to your cluster: `dapr init -k`
3. Update Helm values for cloud-specific configurations
4. Deploy using Helm: `helm install todo-chatbot charts/todo-chatbot/`

### Registration and Login
1. To register a new user, send a POST request to `/api/auth/register` with:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
2. To login, send a POST request to `/api/auth/login` with:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```

### Testing the Event-Driven Features
1. Start the application with all services
2. Register or login to get an access token
3. Create tasks and observe event processing
4. Set up recurring tasks and reminders
5. Monitor events flowing through the system via Dapr dashboard

## Constraints

This implementation follows the Phase V+ constraints:
- Event-driven architecture with loose coupling via Dapr Pub/Sub
- All infrastructure interactions through Dapr building blocks
- No direct database or message queue connections in application code
- Horizontal scalability and cloud-native deployment patterns
- Advanced features: recurring tasks, reminders, priorities, tags, search/filter/sort
- Performance targets: <500ms task operations, ±30s reminder accuracy