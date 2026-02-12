---
id: 1017
title: k8s-constitution-update-phase4
stage: constitution
date: 2026-02-12
surface: agent
model: Qwen
feature: k8s-deployment
branch: 001-k8s-deployment
user: user
command: /sp.constitution
labels: ["kubernetes", "deployment", "todo-chatbot", "helm", "minikube", "constitution", "phase4", "ai-assisted"]
links:
  spec: ../spec.md
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```text
/sp.constitution # Phase IV Specification: Cloud Native Todo Chatbot Deployment on Local Kubernetes (Minikube)

## Project Overview
- Application: Todo Chatbot (from Phase 3) – Full-stack web app with frontend (likely React/Vite/Next.js), backend (likely Node.js/Express/Python FastAPI/Flask), integrated chatbot feature.
- Goal: Containerize both frontend and backend → Generate Helm chart → Deploy on local Minikube using AI-assisted tools.
- Development Rule: No manual coding. Use Qwen (Qwen3-Coder or similar) to generate all files, YAML, Dockerfiles, etc.
- Environment: Local only (Docker Desktop + Minikube). No cloud needed.
- Basic Level Functionality: App should run with at least 1 replica each for frontend & backend, services exposed (NodePort or LoadBalancer for local access), basic health checks.

## Key Requirements
1. Containerization (Docker)
   - Separate Dockerfiles for frontend and backend.
   - Use multi-stage builds where possible for smaller images.
   - Expose correct ports (e.g., frontend: 3000 or 5173, backend: 5000 or 8000 or whatever your app uses).
   - Handle environment variables (e.g., API base URL for frontend to talk to backend).
   - Use Gordon if available, else standard Dockerfiles.
   - Final images: todo-frontend:latest and todo-backend:latest.

2. Kubernetes Resources (via Helm Chart)
   - Helm chart named: todo-chatbot
   - Include:
     - Deployments: frontend-deployment, backend-deployment (start with 1 replica, later can scale).
     - Services: frontend-service (type: LoadBalancer or NodePort), backend-service (ClusterIP).
     - Optional: Ingress if time allows (but not required for basic).
     - Basic probes: readinessProbe, livenessProbe (HTTP GET on /health or root).
   - values.yaml for configurable items: replicas, image tags, ports, env vars.
   - Templates folder with deployment.yaml, service.yaml, etc.

3. Deployment Flow on Minikube
   - Start Minikube.
   - Build & load Docker images into Minikube (minikube image load).
   - Helm install the chart.
   - Access frontend via minikube service or tunnel.
   - Use kubectl-ai / kagent style prompts if tools available, else manual kubectl.

4. AI-Assisted Workflow (using Qwen instead of Claude)
   - Write spec → Ask Qwen to generate plan → Break into tasks → Generate each file one by one.
   - Iterate if output has errors.

## Assumptions about Phase 3 App
- Frontend: Runs on port 3000 (or specify your port), serves static files or dev server.
- Backend: API server on port 5000/8000, handles todo CRUD + chatbot logic.
- Frontend calls backend via relative path or env var (e.g., VITE_API_URL).
- No database in scope yet (assume in-memory or simple for now; if DB exists, mention in prompt).
- App has no auth or advanced features needed for basic deploy.

## Success Criteria
- minikube status running.
- Pods: 1 frontend pod + 1 backend pod running (no crashloop).
- Access frontend in browser via minikube IP:port.
- Todo list + chatbot works end-to-end.
```

## Response snapshot

Successfully updated the constitution file to reflect the new requirements for Phase IV: Cloud Native Todo Chatbot Deployment on Local Kubernetes (Minikube). The key changes made include:

1. Updated version from 1.1.0 to 1.2.0
2. Added a new core principle: VII. AI-Assisted Generation (NON-NEGOTIABLE) which mandates that all code, configuration files, Dockerfiles, Kubernetes YAMLs, and Helm charts must be generated using AI tools rather than manual coding
3. Enhanced the Container-First Architecture principle to specify that Dockerfiles must be generated using AI tools with multi-stage builds
4. Updated the Reproducible and Scalable Deployment principle to emphasize AI-generated configuration files
5. Added AI Tool Requirements section specifying the use of Qwen, kubectl-ai, and Docker AI Agent (Gordon)
6. Added specific deployment policies for container image naming conventions
7. Updated quality gates to include end-to-end functionality verification

The constitution now properly reflects the AI-assisted approach required for Phase IV, emphasizing the use of Qwen for generating all necessary files and configurations.

## Outcome

- ✅ Impact: Constitution updated to reflect Phase IV requirements
- 🧪 Tests: No tests required for constitution update
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Ready for implementation following new guidelines
- 🧠 Reflection: Constitution now properly guides AI-assisted development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate Dockerfiles using Qwen as specified