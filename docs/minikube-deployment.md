# Todo Chatbot Deployment Quickstart Guide

This guide provides instructions for quickly deploying the Todo Chatbot application to a local Minikube cluster.

## Prerequisites

- Docker Desktop installed and running
- Minikube installed (tested with version 1.28+)
- kubectl installed
- Helm 3.x installed
- Git (if cloning from repository)

## Quick Deployment Steps

### 1. Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=8192mb --disk-size=40gb
```

### 2. Set Docker environment to Minikube

```bash
eval $(minikube docker-env)
```

### 3. Build Docker images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..
```

### 4. Deploy using Helm

```bash
# Navigate to charts directory
cd charts/todo-chatbot

# Install the Helm chart
helm install todo-chatbot . --values values.yaml
```

### 5. Verify deployment

```bash
# Check if pods are running
kubectl get pods

# Check if services are available
kubectl get services

# Wait for deployments to be ready
kubectl wait --for=condition=ready pod -l app=backend --timeout=180s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=180s
```

### 6. Access the application

```bash
# Get the frontend service URL
minikube service todo-chatbot-frontend-service --url
```

## Scaling the Frontend

The frontend is configured with 2 replicas by default for high availability. To scale further:

```bash
# Scale frontend to 3 replicas
kubectl scale deployment todo-chatbot-frontend --replicas=3

# Verify the scaling
kubectl get deployment todo-chatbot-frontend
```

## Health Monitoring

The deployments include health checks:

- **Backend**: Health check at `/health`, readiness at `/ready`
- **Frontend**: Health check at `/`

To check the status of health probes:

```bash
# Check pod status and restart counts
kubectl get pods

# View logs for any issues
kubectl logs -l app=backend
kubectl logs -l app=frontend
```

## Troubleshooting

### Common Issues

1. **Images not found**: Make sure to run `eval $(minikube docker-env)` before building images
2. **Service not accessible**: Check if the NodePort is available and not blocked by firewall
3. **Pods in CrashLoopBackOff**: Check logs with `kubectl logs <pod-name>`

### Useful Commands

```bash
# Check all resources
kubectl get all

# Check deployment status
kubectl get deployments
kubectl describe deployment <deployment-name>

# Check service status
kubectl get services
kubectl describe service <service-name>

# Check pod logs
kubectl logs -l app=backend
kubectl logs -l app=frontend

# Check resource usage
kubectl top pods

# Port forward for direct access (alternative to NodePort)
kubectl port-forward service/todo-chatbot-frontend-service 8080:80
```

## Uninstall

To remove the Todo Chatbot deployment:

```bash
helm uninstall todo-chatbot
```

## Validation

Run the validation script to ensure everything is working correctly:

```bash
bash scripts/final-validation.sh
```

This will check all components and confirm that the deployment meets all requirements.