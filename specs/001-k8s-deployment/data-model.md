# Data Model: Phase 4 Cloud Native Todo Chatbot Deployment

## Kubernetes Resources

### Frontend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata**: name, namespace, labels
- **spec**:
  - replicas: 2 (minimum as per requirement)
  - selector: matchLabels
  - template:
    - metadata: labels
    - spec:
      - containers:
        - name: frontend
        - image: todo-frontend:latest
        - ports: [{containerPort: 3000}]
        - env: [{name: NEXT_PUBLIC_API_URL, value: "http://todo-chatbot-backend-service:8000"}]
        - resources: {limits: {cpu: "500m", memory: "512Mi"}, requests: {cpu: "100m", memory: "128Mi"}}
        - livenessProbe: {httpGet: {path: "/", port: 3000}, initialDelaySeconds: 30, periodSeconds: 10}
        - readinessProbe: {httpGet: {path: "/", port: 3000}, initialDelaySeconds: 5, periodSeconds: 5}

### Backend Deployment
- **apiVersion**: apps/v1
- **kind**: Deployment
- **metadata**: name, namespace, labels
- **spec**:
  - replicas: 1 (default, can be scaled as needed)
  - selector: matchLabels
  - template:
    - metadata: labels
    - spec:
      - containers:
        - name: backend
        - image: todo-backend:latest
        - ports: [{containerPort: 8000}]
        - env:
          - {name: DATABASE_URL, valueFrom: {secretKeyRef: {name: db-secret, key: url}}}
          - {name: SECRET_KEY, valueFrom: {secretKeyRef: {name: auth-secret, key: secret}}}
        - resources: {limits: {cpu: "500m", memory: "512Mi"}, requests: {cpu: "100m", memory: "256Mi"}}
        - livenessProbe: {httpGet: {path: "/health", port: 8000}, initialDelaySeconds: 30, periodSeconds: 10}
        - readinessProbe: {httpGet: {path: "/ready", port: 8000}, initialDelaySeconds: 5, periodSeconds: 5}

### Frontend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata**: name, namespace, labels
- **spec**:
  - selector: {app: frontend}
  - ports: [{protocol: TCP, port: 80, targetPort: 3000, nodePort: 30080}]
  - type: NodePort

### Backend Service
- **apiVersion**: v1
- **kind**: Service
- **metadata**: name, namespace, labels
- **spec**:
  - selector: {app: backend}
  - ports: [{protocol: TCP, port: 8000, targetPort: 8000}]
  - type: ClusterIP

### ConfigMap
- **apiVersion**: v1
- **kind**: ConfigMap
- **metadata**: name, namespace
- **data**: configuration properties for the application

### Secret
- **apiVersion**: v1
- **kind**: Secret
- **metadata**: name, namespace
- **data**: encoded sensitive information (database credentials, API keys)

## Helm Chart Structure

### Chart.yaml
- **apiVersion**: v2
- **name**: todo-chatbot
- **version**: 0.1.0
- **appVersion**: "1.0.0"
- **description**: Helm chart for deploying the Todo Chatbot application

### values.yaml
- **frontend**:
  - replicaCount: 2
  - image: {repository: "todo-frontend", tag: "latest", pullPolicy: "IfNotPresent"}
  - service: {type: "NodePort", port: 80, nodePort: 30080}
  - resources: {limits: {cpu: "500m", memory: "512Mi"}, requests: {cpu: "100m", memory: "128Mi"}}
  - env: {NEXT_PUBLIC_API_URL: "http://todo-chatbot-backend-service:8000"}

- **backend**:
  - replicaCount: 1
  - image: {repository: "todo-backend", tag: "latest", pullPolicy: "IfNotPresent"}
  - service: {type: "ClusterIP", port: 8000}
  - resources: {limits: {cpu: "500m", memory: "512Mi"}, requests: {cpu: "100m", memory: "256Mi"}}

### Templates Structure
- **backend-deployment.yaml**: Backend deployment configuration
- **frontend-deployment.yaml**: Frontend deployment configuration
- **backend-service.yaml**: Backend service configuration
- **frontend-service.yaml**: Frontend service configuration
- **_helpers.tpl**: Helm template helpers

## Docker Images

### Frontend Image
- **Base**: node:18-alpine
- **Build**: npm install, npm run build
- **Runtime**: serve built assets
- **Port**: 3000

### Backend Image
- **Base**: python:3.11-slim
- **Dependencies**: requirements.txt
- **Application**: FastAPI app served with uvicorn
- **Port**: 8000