# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application, which consists of a frontend and backend service with integrated chatbot functionality.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Minikube (for local deployment)

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
# First build and load Docker images into Minikube
eval $(minikube docker-env)
cd backend && docker build -t todo-backend:latest . && cd ..
cd frontend && docker build -t todo-frontend:latest . && cd ..

# Install the chart
helm install todo-chatbot . --values values.yaml
```

## Configuration

The following table lists the configurable parameters of the Todo Chatbot chart and their default values.

### Frontend Configuration

| Parameter                      | Description                                     | Default                          |
| ------------------------------ | ----------------------------------------------- | -------------------------------- |
| `frontend.replicaCount`       | Number of frontend replicas (minimum 2 for HA)   | `2`                              |
| `frontend.image.repository`   | Frontend image repository                        | `todo-frontend`                  |
| `frontend.image.pullPolicy`   | Frontend image pull policy                       | `IfNotPresent`                   |
| `frontend.image.tag`          | Frontend image tag                               | `latest`                         |
| `frontend.service.type`       | Frontend service type                            | `NodePort`                       |
| `frontend.service.port`       | Frontend service port                            | `80`                             |
| `frontend.service.nodePort`   | Frontend service nodePort (when type is NodePort) | `30080`                         |
| `frontend.resources.limits`   | CPU/Memory resource limits for frontend          | `{"cpu": "500m", "memory": "512Mi"}` |
| `frontend.resources.requests` | CPU/Memory resource requests for frontend        | `{"cpu": "100m", "memory": "128Mi"}` |
| `frontend.env.NEXT_PUBLIC_API_URL` | Environment variable for backend API URL    | `"http://todo-chatbot-backend-service:8000"`  |

### Backend Configuration

| Parameter                      | Description                                     | Default                          |
| ------------------------------ | ----------------------------------------------- | -------------------------------- |
| `backend.replicaCount`        | Number of backend replicas                       | `1`                              |
| `backend.image.repository`    | Backend image repository                         | `todo-backend`                   |
| `backend.image.pullPolicy`    | Backend image pull policy                        | `IfNotPresent`                   |
| `backend.image.tag`           | Backend image tag                                | `latest`                         |
| `backend.service.type`        | Backend service type                             | `ClusterIP`                      |
| `backend.service.port`        | Backend service port                             | `8000`                           |
| `backend.resources.limits`    | CPU/Memory resource limits for backend           | `{"cpu": "500m", "memory": "512Mi"}` |
| `backend.resources.requests`  | CPU/Memory resource requests for backend         | `{"cpu": "100m", "memory": "256Mi"}` |

### Health Check Configuration

| Parameter                      | Description                                     | Default                          |
| ------------------------------ | ----------------------------------------------- | -------------------------------- |
| `config.healthCheckPath`      | Path for backend health checks                   | `/health`                        |
| `config.readinessCheckPath`   | Path for backend readiness checks                | `/ready`                         |
| `config.livenessInitialDelay` | Initial delay for liveness probes (seconds)      | `30`                             |
| `config.readinessInitialDelay`| Initial delay for readiness probes (seconds)     | `5`                              |

## Scaling

The frontend is configured with 2 replicas by default for high availability. To scale further:

```bash
kubectl scale deployment todo-chatbot-frontend --replicas=3
```

## Health Monitoring

The deployments include liveness and readiness probes:
- Backend: `/health` and `/ready` endpoints
- Frontend: Root path `/` for both liveness and readiness

## Uninstalling the Chart

To uninstall/delete the `todo-chatbot` deployment:

```bash
helm delete todo-chatbot
```

## Local Development with Minikube

For local development, deploy the chart to Minikube:

1. Start Minikube:
   ```bash
   minikube start --driver=docker --cpus=4 --memory=8192mb
   ```

2. Build and load Docker images:
   ```bash
   eval $(minikube docker-env)
   cd backend && docker build -t todo-backend:latest . && cd ..
   cd frontend && docker build -t todo-frontend:latest . && cd ..
   ```

3. Install the Helm chart:
   ```bash
   helm install todo-chatbot charts/todo-chatbot/ --values charts/todo-chatbot/values.yaml
   ```

4. Access the frontend:
   ```bash
   minikube service todo-chatbot-frontend-service --url
   ```