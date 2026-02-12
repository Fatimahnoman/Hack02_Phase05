# Phase 4 Detailed Specification (/sp.specify)

## 1. Application Architecture Details
- **Frontend framework**: Next.js (React-based, using built-in Turbopack bundler)
- **Backend framework**: Python FastAPI (selected over Node.js/Express for better async support and automatic API docs)
- **Frontend port**: Container port 3000, exposed via NodePort service
- **Backend port**: Container port 8000, exposed via ClusterIP service
- **Communication**: Frontend calls backend via environment variable NEXT_PUBLIC_API_URL set to "http://todo-chatbot-backend-service:8000"
- **Components**: 
  - Frontend: Next.js app with React components for todo management and chat interface
  - Backend: FastAPI app handling todo CRUD operations and chatbot logic
  - Chatbot: Integrated into backend as API endpoints
- **Environment variables needed**:
  - Frontend: NEXT_PUBLIC_API_URL (for backend API calls)
  - Backend: DATABASE_URL, SECRET_KEY, OPENAI_API_KEY (if using external LLM)
- **Health check paths**: 
  - Backend: /health for liveness, /ready for readiness
  - Frontend: / for both liveness and readiness (basic health check)

## 2. Containerization Requirements
- **Frontend Dockerfile**:
  - Build context: ./frontend
  - Multi-stage: Build stage (Node.js 18-alpine with dependencies and build), Runtime stage (serve built assets)
  - Image name: todo-frontend:latest
  - Exposed port: 3000
  - CMD: ["npm", "start"] or equivalent to serve built app
- **Backend Dockerfile**:
  - Build context: ./backend
  - Multi-stage: Build stage (Python 3.11-slim with dependencies), Runtime stage (copy dependencies and app code)
  - Image name: todo-backend:latest
  - Exposed port: 8000
  - CMD: ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
- **Build contexts**: ./frontend and ./backend directories respectively
- **Volumes**: None required for basic deployment

## 3. Kubernetes / Helm Chart Specification
- **Chart name**: todo-chatbot
- **Chart version**: 0.1.0
- **Required resources**:
  - Deployments: frontend-deployment, backend-deployment
  - Services: frontend-service (NodePort), backend-service (ClusterIP)
  - ConfigMaps: Optional for environment configuration
- **Default replicas**: 1 for both frontend and backend
- **Service types**:
  - Frontend: NodePort (for local Minikube access)
  - Backend: ClusterIP (internal communication only)
- **Probes**:
  - Backend liveness: HTTP GET /health on port 8000, initialDelaySeconds: 30, periodSeconds: 10
  - Backend readiness: HTTP GET /ready on port 8000, initialDelaySeconds: 5, periodSeconds: 5
  - Frontend liveness: HTTP GET / on port 3000, initialDelaySeconds: 30, periodSeconds: 10
  - Frontend readiness: HTTP GET / on port 3000, initialDelaySeconds: 5, periodSeconds: 5
- **Labels and selectors**: app: frontend/backend with release name as additional selector
- **Environment variables injection**: Via values.yaml using downward API or direct value injection
- **ConfigMaps**: For non-sensitive configuration values

## 4. Minikube-Specific Deployment Details
- **Minikube start**: minikube start --driver=docker --cpus=4 --memory=8192mb --disk-size=40gb
- **Image loading**: minikube image load todo-frontend:latest && minikube image load todo-backend:latest
- **Helm install**: helm install todo-chatbot ./charts/todo-chatbot/ --values ./charts/todo-chatbot/values.yaml
- **Access methods**:
  - Frontend: minikube service todo-chatbot-frontend-service --url
  - Backend: Internal to cluster via service name
- **Scaling example**: kubectl scale deployment todo-chatbot-frontend --replicas=2

## 5. Fallbacks and Constraints
- **No Gordon/kubectl-ai/kagent**: Use standard docker build, kubectl apply, helm install
- **Local only**: No cloud dependencies, all resources local to Minikube
- **No persistent DB**: Assume in-memory storage for todos/chat state (for simplicity)
- **Basic level**: No Ingress, monitoring (Prometheus/Grafana), autoscaling (HPA), persistent volumes
- **Security**: Basic setup, no advanced RBAC or network policies required
- **Networking**: Standard ClusterIP and NodePort services only

## 6. Success Validation Steps
- **Check pods**: kubectl get pods (should show both frontend and backend pods running)
- **Check services**: kubectl get services (should show both services with valid endpoints)
- **Check deployments**: kubectl get deployments (should show desired and current replicas matching)
- **View logs**: kubectl logs -l app=backend and kubectl logs -l app=frontend
- **Access frontend**: Use minikube service command to get URL and access in browser
- **Test functionality**: Verify todo list operations and chatbot functionality work end-to-end

## 7. Prompting Guidelines for Next Steps
- **For Dockerfiles**: "Generate optimized multi-stage Dockerfile for [frontend/backend] based on Phase 4 spec, using [appropriate base image]"
- **For Helm templates**: "Generate Kubernetes [resource type] template for Helm chart based on Phase 4 spec, with proper labels, selectors, and environment variable injection"
- **For values.yaml**: "Generate Helm values.yaml with configurable parameters for replicas, image tags, ports, and environment variables based on Phase 4 spec"
- **Iteration rules**: If generated artifact has errors, provide specific error message and ask for correction with context: "Fix the [specific issue] in [file name] while maintaining compliance with Phase 4 spec"