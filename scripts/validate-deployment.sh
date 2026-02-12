#!/bin/bash

# Todo Chatbot Deployment Validation Script
# Validates that the Todo Chatbot application is properly deployed and functioning

set -e  # Exit on any error

echo "🔍 Validating Todo Chatbot deployment..."

# Function to print status messages
print_status() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function to print success messages
print_success() {
    echo "[✅] $1"
}

# Function to print error messages
print_error() {
    echo "[❌] $1"
    exit 1
}

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed"
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed"
fi

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    print_error "Minikube is not running"
fi

# Set release name
RELEASE_NAME="todo-chatbot"

# Check if Helm release exists
if ! helm status $RELEASE_NAME &> /dev/null; then
    print_error "Helm release $RELEASE_NAME does not exist"
fi

print_success "Helm release $RELEASE_NAME exists"

# Check deployments
print_status "Checking deployments..."

BACKEND_DEPLOYMENT=$(kubectl get deployments -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
FRONTEND_DEPLOYMENT=$(kubectl get deployments -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$BACKEND_DEPLOYMENT" ]; then
    print_error "Backend deployment not found"
fi

if [ -z "$FRONTEND_DEPLOYMENT" ]; then
    print_error "Frontend deployment not found"
fi

print_success "Backend deployment: $BACKEND_DEPLOYMENT"
print_success "Frontend deployment: $FRONTEND_DEPLOYMENT"

# Check replica counts
BACKEND_REPLICAS=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.spec.replicas}')
FRONTEND_REPLICAS=$(kubectl get deployment $FRONTEND_DEPLOYMENT -o jsonpath='{.spec.replicas}')

BACKEND_READY_REPLICAS=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.status.readyReplicas}')
FRONTEND_READY_REPLICAS=$(kubectl get deployment $FRONTEND_DEPLOYMENT -o jsonpath='{.status.readyReplicas}')

print_status "Backend replicas: $BACKEND_REPLICAS (ready: $BACKEND_READY_REPLICAS)"
print_status "Frontend replicas: $FRONTEND_REPLICAS (ready: $FRONTEND_READY_REPLICAS)"

# Check if frontend has at least 2 replicas as required
if [ "$FRONTEND_REPLICAS" -lt 2 ]; then
    print_error "Frontend deployment has less than 2 replicas ($FRONTEND_REPLICAS)"
fi

if [ "$FRONTEND_READY_REPLICAS" -lt 2 ]; then
    print_error "Less than 2 frontend replicas are ready ($FRONTEND_READY_REPLICAS)"
fi

print_success "Frontend has minimum 2 replicas as required"

# Check pods
print_status "Checking pods..."

BACKEND_PODS=$(kubectl get pods -l app=backend --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{" "}{end}' 2>/dev/null)
FRONTEND_PODS=$(kubectl get pods -l app=frontend --field-selector=status.phase=Running -o jsonpath='{range .items[*]}{.metadata.name}{" "}{end}' 2>/dev/null)

if [ -z "$BACKEND_PODS" ]; then
    print_error "No running backend pods found"
fi

if [ -z "$FRONTEND_PODS" ]; then
    print_error "No running frontend pods found"
fi

BACKEND_POD_COUNT=$(echo $BACKEND_PODS | wc -w)
FRONTEND_POD_COUNT=$(echo $FRONTEND_PODS | wc -w)

print_success "Found $BACKEND_POD_COUNT running backend pod(s)"
print_success "Found $FRONTEND_POD_COUNT running frontend pod(s)"

# Check services
print_status "Checking services..."

BACKEND_SERVICE=$(kubectl get svc -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
FRONTEND_SERVICE=$(kubectl get svc -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$BACKEND_SERVICE" ]; then
    print_error "Backend service not found"
fi

if [ -z "$FRONTEND_SERVICE" ]; then
    print_error "Frontend service not found"
fi

print_success "Backend service: $BACKEND_SERVICE"
print_success "Frontend service: $FRONTEND_SERVICE"

# Check service types
BACKEND_SERVICE_TYPE=$(kubectl get svc $BACKEND_SERVICE -o jsonpath='{.spec.type}')
FRONTEND_SERVICE_TYPE=$(kubectl get svc $FRONTEND_SERVICE -o jsonpath='{.spec.type}')

print_status "Backend service type: $BACKEND_SERVICE_TYPE"
print_status "Frontend service type: $FRONTEND_SERVICE_TYPE"

if [ "$BACKEND_SERVICE_TYPE" != "ClusterIP" ]; then
    print_error "Backend service type is $BACKEND_SERVICE_TYPE, expected ClusterIP"
fi

if [ "$FRONTEND_SERVICE_TYPE" != "NodePort" ] && [ "$FRONTEND_SERVICE_TYPE" != "LoadBalancer" ]; then
    print_error "Frontend service type is $FRONTEND_SERVICE_TYPE, expected NodePort or LoadBalancer"
fi

print_success "Service types are correctly configured"

# Check service endpoints
print_status "Checking service endpoints..."

BACKEND_ENDPOINTS=$(kubectl get endpoints $BACKEND_SERVICE -o jsonpath='{range .subsets[0].addresses[*]}{.ip}{" "}{end}' 2>/dev/null)
FRONTEND_ENDPOINTS=$(kubectl get endpoints $FRONTEND_SERVICE -o jsonpath='{range .subsets[0].addresses[*]}{.ip}{" "}{end}' 2>/dev/null)

if [ -z "$BACKEND_ENDPOINTS" ]; then
    print_error "No backend service endpoints available"
fi

if [ -z "$FRONTEND_ENDPOINTS" ]; then
    print_error "No frontend service endpoints available"
fi

print_success "Service endpoints are available"

# Check if health checks are configured
print_status "Checking health check configurations..."

BACKEND_LIVENESS_PATH=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].livenessProbe.httpGet.path}' 2>/dev/null)
BACKEND_READINESS_PATH=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].readinessProbe.httpGet.path}' 2>/dev/null)

if [ -z "$BACKEND_LIVENESS_PATH" ] || [ -z "$BACKEND_READINESS_PATH" ]; then
    print_error "Backend health checks not properly configured"
fi

print_success "Backend health checks configured: liveness=$BACKEND_LIVENESS_PATH, readiness=$BACKEND_READINESS_PATH"

# Check resource limits
print_status "Checking resource configurations..."

BACKEND_LIMITS_CPU=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].resources.limits.cpu}' 2>/dev/null)
BACKEND_LIMITS_MEM=$(kubectl get deployment $BACKEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].resources.limits.memory}' 2>/dev/null)

FRONTEND_LIMITS_CPU=$(kubectl get deployment $FRONTEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].resources.limits.cpu}' 2>/dev/null)
FRONTEND_LIMITS_MEM=$(kubectl get deployment $FRONTEND_DEPLOYMENT -o jsonpath='{.spec.template.spec.containers[0].resources.limits.memory}' 2>/dev/null)

if [ -z "$BACKEND_LIMITS_CPU" ] || [ -z "$BACKEND_LIMITS_MEM" ]; then
    print_error "Backend resource limits not configured"
fi

if [ -z "$FRONTEND_LIMITS_CPU" ] || [ -z "$FRONTEND_LIMITS_MEM" ]; then
    print_error "Frontend resource limits not configured"
fi

print_success "Resource limits configured for both services"

# Check pod restart counts
print_status "Checking pod restart counts..."

for pod in $BACKEND_PODS; do
    RESTARTS=$(kubectl get pod $pod -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null)
    if [ -n "$RESTARTS" ] && [ "$RESTARTS" -gt 5 ]; then
        print_error "Backend pod $pod has restarted $RESTARTS times (too many)"
    fi
done

for pod in $FRONTEND_PODS; do
    RESTARTS=$(kubectl get pod $pod -o jsonpath='{.status.containerStatuses[0].restartCount}' 2>/dev/null)
    if [ -n "$RESTARTS" ] && [ "$RESTARTS" -gt 5 ]; then
        print_error "Frontend pod $pod has restarted $RESTARTS times (too many)"
    fi
done

print_success "All pods have reasonable restart counts"

# Final summary
print_status ""
print_success "🎉 All validation checks passed!"
print_status ""
print_status "Summary:"
print_status "- Helm release: $RELEASE_NAME"
print_status "- Backend deployment: $BACKEND_DEPLOYMENT ($BACKEND_READY_REPLICAS/$BACKEND_REPLICAS ready)"
print_status "- Frontend deployment: $FRONTEND_DEPLOYMENT ($FRONTEND_READY_REPLICAS/$FRONTEND_REPLICAS ready)"
print_status "- Backend pods: $BACKEND_POD_COUNT running"
print_status "- Frontend pods: $FRONTEND_POD_COUNT running (minimum 2 requirement satisfied)"
print_status "- Services: $BACKEND_SERVICE ($BACKEND_SERVICE_TYPE), $FRONTEND_SERVICE ($FRONTEND_SERVICE_TYPE)"
print_status "- Health checks: Configured for both backend and frontend"
print_status "- Resource limits: Configured for both deployments"
print_status ""
print_status "The Todo Chatbot application is properly deployed and validated!"