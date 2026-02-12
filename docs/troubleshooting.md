# Todo Chatbot Deployment Troubleshooting Guide

This guide provides solutions to common issues encountered when deploying the Todo Chatbot application to Minikube using Helm.

## Common Deployment Issues

### 1. Images Not Found in Minikube

**Problem**: Pods are stuck in `ImagePullBackOff` or `ErrImagePull` status.

**Solution**:
- Ensure you've built the Docker images using Minikube's Docker daemon:
  ```bash
  # Configure Docker client to use Minikube's Docker daemon
  eval $(minikube docker-env)
  
  # Build backend
  cd backend
  docker build -t todo-backend:latest .
  
  # Build frontend
  cd ../frontend
  docker build -t todo-frontend:latest .
  ```
- Verify the images exist in Minikube:
  ```bash
  docker images | grep todo
  ```

### 2. Minikube Not Starting

**Problem**: `minikube start` fails with various errors.

**Solutions**:
- Try deleting and recreating the cluster:
  ```bash
  minikube delete --profile=todo-chatbot
  minikube start --profile=todo-chatbot --driver=docker
  ```
- If using a specific driver, try a different one:
  ```bash
  minikube start --profile=todo-chatbot --driver=docker
  ```
- Increase allocated resources:
  ```bash
  minikube start --profile=todo-chatbot --cpus=4 --memory=8192mb --disk-size=40gb
  ```

### 3. Service Not Accessible

**Problem**: Cannot access the frontend service via NodePort.

**Solutions**:
- Check if the service is running:
  ```bash
  kubectl get services
  ```
- Get the service URL:
  ```bash
  minikube service todo-chatbot-frontend-service --url
  ```
- Verify the NodePort is in the valid range (30000-32767):
  ```bash
  kubectl describe service todo-chatbot-frontend-service
  ```

### 4. Pods Stuck in Pending State

**Problem**: Pods remain in `Pending` state for a long time.

**Solutions**:
- Check if there are enough resources:
  ```bash
  kubectl describe nodes
  ```
- Check for resource constraints in the deployment:
  ```bash
  kubectl describe pod <pod-name>
  ```
- Adjust resource requests/limits in `values.yaml` if needed.

## Health and Readiness Issues

### 1. Liveness/Readiness Probes Failing

**Problem**: Pods are restarting repeatedly due to probe failures.

**Solutions**:
- Check pod logs:
  ```bash
  kubectl logs <pod-name>
  ```
- Verify the probe endpoints exist and respond correctly
- Adjust probe parameters (initialDelaySeconds, periodSeconds, etc.) in the deployment templates

### 2. Application Not Responding

**Problem**: The application is running but not responding to requests.

**Solutions**:
- Check if the backend service is accessible from the frontend:
  ```bash
  kubectl exec -it <frontend-pod> -- curl -v http://todo-chatbot-backend-service:8000/health
  ```
- Verify environment variables are set correctly:
  ```bash
  kubectl describe pod <pod-name>
  ```

## Scaling Issues

### 1. Scaling Not Working

**Problem**: Scaling the frontend deployment doesn't increase pod count.

**Solutions**:
- Verify the deployment name:
  ```bash
  kubectl get deployments
  ```
- Manually scale:
  ```bash
  kubectl scale deployment todo-chatbot-frontend --replicas=3
  ```
- Check for resource constraints preventing new pods from starting.

## Resource Management Issues

### 1. Out of Memory Errors

**Problem**: Pods are being killed due to memory constraints.

**Solutions**:
- Increase memory limits in `values.yaml`:
  ```yaml
  frontend:
    resources:
      limits:
        memory: "1Gi"  # Increased from 512Mi
  backend:
    resources:
      limits:
        memory: "1Gi"  # Increased from 512Mi
  ```
- Check current resource usage:
  ```bash
  kubectl top pods
  ```

### 2. CPU Throttling

**Problem**: Application performance is degraded due to CPU limitations.

**Solutions**:
- Increase CPU limits in `values.yaml`:
  ```yaml
  frontend:
    resources:
      limits:
        cpu: "1000m"  # Increased from 500m
  backend:
    resources:
      limits:
        cpu: "1000m"  # Increased from 500m
  ```

## Network and Service Issues

### 1. Service Discovery Problems

**Problem**: Frontend cannot reach backend service.

**Solutions**:
- Verify service exists:
  ```bash
  kubectl get svc
  ```
- Test connectivity from frontend pod:
  ```bash
  kubectl exec -it <frontend-pod> -- nslookup todo-chatbot-backend-service
  kubectl exec -it <frontend-pod> -- curl -v http://todo-chatbot-backend-service:8000
  ```
- Check if the service name matches the environment variable in the frontend deployment.

## Debugging Commands

### Useful kubectl Commands

- Get all resources in the current namespace:
  ```bash
  kubectl get all
  ```
- Get detailed information about a resource:
  ```bash
  kubectl describe <resource-type> <resource-name>
  ```
- View logs from all pods with a specific label:
  ```bash
  kubectl logs -l app=backend
  ```
- Execute commands inside a pod:
  ```bash
  kubectl exec -it <pod-name> -- /bin/sh
  ```
- Watch resource status in real-time:
  ```bash
  kubectl get pods --watch
  ```

### Useful Helm Commands

- Check release status:
  ```bash
  helm status todo-chatbot
  ```
- Get release manifest:
  ```bash
  helm get manifest todo-chatbot
  ```
- Rollback to previous version:
  ```bash
  helm rollback todo-chatbot
  ```
- Check for configuration issues:
  ```bash
  helm lint charts/todo-chatbot/
  ```

## Performance Issues

### 1. Slow Response Times

**Problem**: Application responses are slower than expected.

**Solutions**:
- Check resource utilization:
  ```bash
  kubectl top nodes
  kubectl top pods
  ```
- Verify database connection settings
- Check for network latency between services
- Consider increasing resource limits

### 2. High Resource Usage

**Problem**: Application is consuming more resources than expected.

**Solutions**:
- Profile the application to identify bottlenecks
- Optimize queries and reduce unnecessary operations
- Adjust resource requests to more accurately reflect actual usage

## Getting Help

If you encounter an issue not covered in this guide:

1. Check the Kubernetes and Helm documentation
2. Look at the events for more details:
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```
3. Share the output of `kubectl describe` for the problematic resource
4. Consider reaching out to your team or community forums with specific error messages and logs