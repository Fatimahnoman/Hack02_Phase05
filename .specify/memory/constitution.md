<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
Modified principles: III. Container-First Architecture, IV. Reproducible and Scalable Deployment, V. Local-First Development Environment
Added sections: Core Principles (VII. AI-Assisted Generation), Additional Constraints (AI Tool Requirements)
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated  
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Runtime docs requiring updates:
  - README.md ✅ updated
Follow-up TODOs: None
-->

# Todo Chatbot Kubernetes Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development begins with a comprehensive specification document that defines requirements, architecture, and implementation tasks. No code shall be written without a corresponding specification that has been reviewed and approved. This ensures alignment between stakeholder expectations and delivered functionality.

### II. Agentic Dev Stack Workflow
Development follows a structured workflow: Write Spec → Generate Plan → Break into Tasks → Implement via AI Agent. This approach leverages AI capabilities while maintaining human oversight and ensuring systematic progress toward well-defined objectives.

### III. Container-First Architecture
All services must be designed and packaged as containers from the outset. This ensures consistent environments across development, testing, and production, while enabling scalability and portability. Containerization is not an afterthought but a foundational requirement. Dockerfiles must be generated using AI tools (Gordon or similar) with multi-stage builds where possible.

### IV. Reproducible and Scalable Deployment
Every deployment must be reproducible in any environment with identical results. Infrastructure as Code principles must be followed using tools like Helm Charts. Scaling capabilities must be built into the system architecture from the beginning. All Kubernetes resources must be defined via AI-generated configuration files.

### V. Local-First Development Environment
Development and testing should primarily occur in local environments (e.g., Minikube) to enable rapid iteration and reduce dependency on remote resources. This ensures developers can work efficiently regardless of network connectivity or cloud resource availability. Minikube must be the primary local Kubernetes environment for development.

### VI. AI-Assisted Operations
Leverage AI agents for infrastructure management, deployment automation, and operational tasks. This includes using AI for generating configuration files, troubleshooting issues, and optimizing deployments. Human operators provide oversight and final approval for critical operations.

### VII. AI-Assisted Generation (NON-NEGOTIABLE)
All code, configuration files, Dockerfiles, Kubernetes YAMLs, and Helm charts must be generated using AI tools (primarily Qwen) rather than manual coding. No handwritten deployment YAML files are allowed. All infrastructure configuration must be AI-generated to ensure consistency and efficiency.

## Additional Constraints

### Technology Stack Requirements
- Docker Desktop for containerization
- Kubernetes (Minikube) for orchestration
- Helm Charts for package management
- kubectl for cluster operations
- Qwen (Qwen3-Coder or similar) for AI-assisted development
- FastAPI backend with Next.js frontend (existing application stack)
- Docker AI Agent (Gordon) for Dockerfile generation (if available)

### Deployment Policies
- All infrastructure must be defined via AI-generated configuration
- No handwritten deployment YAML files
- Helm charts must be version-controlled and follow semantic versioning
- Resource limits must be defined for all deployments
- Health checks and readiness probes required for all services
- Container images must follow naming convention: todo-frontend:latest and todo-backend:latest
- Services must use appropriate types (NodePort/LoadBalancer for frontend, ClusterIP for backend)

### AI Tool Requirements
- Use Qwen for generating all code and configuration files
- Use kubectl-ai or similar AI-enhanced tools for kubectl commands when available
- Use Docker AI Agent (Gordon) for Dockerfile generation when available
- All YAML files (Kubernetes, Helm, Docker Compose) must be AI-generated
- Manual editing of generated files should be minimal and justified

## Development Workflow

### Pre-Development Requirements
- Specifications must detail Kubernetes resource requirements
- Helm chart structures must be planned in advance
- Local Minikube environment must be validated before deployment
- Security scanning must be integrated into the CI pipeline
- AI tool availability must be confirmed before starting implementation

### Code Review Requirements
- All Kubernetes manifests must be reviewed for security vulnerabilities
- Resource limits and requests must be verified for appropriateness
- Service exposure methods (NodePort, LoadBalancer, etc.) must be justified
- AI-generated configurations must be validated by human reviewers
- Container images must be scanned for vulnerabilities before deployment

### Quality Gates
- All services must pass health checks before deployment promotion
- Resource utilization must remain within defined thresholds
- Cross-service communication must be verified in Kubernetes environment
- Backup and recovery procedures must be tested before production deployment
- End-to-end functionality must be verified (frontend ↔ backend communication)

## Governance

This constitution supersedes all other development practices and must be followed for all Kubernetes deployment activities. Amendments require documentation of the change, approval from project stakeholders, and a migration plan for existing implementations. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.2.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2026-02-12
