#!/bin/bash

# Todo Chatbot Complete Deployment Script
# Orchestrates the full deployment of the Todo Chatbot application to Minikube

set -e  # Exit on any error

echo "🚀 Starting complete Todo Chatbot deployment to Minikube..."
echo "Date: $(date)"
echo ""

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

# Check prerequisites
print_status "Checking prerequisites..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed"
fi

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed"
fi

# Check if Minikube is available
if ! command -v minikube &> /dev/null; then
    print_error "Minikube is not installed"
fi

print_success "All prerequisites are available"

# Check if Minikube is running
print_status "Checking Minikube status..."
if ! minikube status &>/dev/null; then
    print_status "Starting Minikube..."
    minikube start --driver=docker --cpus=4 --memory=8192mb --disk-size=40gb
    print_success "Minikube started successfully"
else
    print_success "Minikube is already running"
fi

# Set Docker environment to use Minikube's Docker daemon
print_status "Configuring Docker to use Minikube daemon..."
eval $(minikube docker-env)
print_success "Docker configured to use Minikube"

# Build backend Docker image
print_status "Building backend Docker image..."
cd ../backend
docker build -t todo-backend:latest . --no-cache
cd ../..
print_success "Backend image built: todo-backend:latest"

# Build frontend Docker image
print_status "Building frontend Docker image..."
cd ../frontend
docker build -t todo-frontend:latest . --no-cache
cd ../..
print_success "Frontend image built: todo-frontend:latest"

# Verify images were built successfully
print_status "Verifying Docker images..."
if [[ "$(docker images -q todo-backend:latest 2> /dev/null)" == "" ]]; then
    print_error "Backend image not found"
else
    print_success "Backend image exists"
fi

if [[ "$(docker images -q todo-frontend:latest 2> /dev/null)" == "" ]]; then
    print_error "Frontend image not found"
else
    print_success "Frontend image exists"
fi

# Navigate to charts directory
cd charts/todo-chatbot

# Check if Helm release already exists
RELEASE_NAME="todo-chatbot"
if helm status $RELEASE_NAME &>/dev/null; then
    print_status "Helm release $RELEASE_NAME already exists, upgrading..."
    helm upgrade $RELEASE_NAME . --values values.yaml
else
    print_status "Installing Helm release $RELEASE_NAME..."
    helm install $RELEASE_NAME . --values values.yaml
fi

print_success "Helm chart installed/updated successfully"

# Wait for deployments to be ready
print_status "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

print_success "Deployments are ready"

# Verify deployments
print_status "Verifying deployment status..."
kubectl get deployments
kubectl get pods
kubectl get services

# Check if the required number of replicas are running
BACKEND_REPLICAS=$(kubectl get deployment todo-chatbot-backend -o jsonpath='{.status.readyReplicas}')
FRONTEND_REPLICAS=$(kubectl get deployment todo-chatbot-frontend -o jsonpath='{.status.readyReplicas}')

if [ "$BACKEND_REPLICAS" -lt 1 ]; then
    print_error "Backend deployment has $BACKEND_REPLICAS ready replicas, expected at least 1"
fi

if [ "$FRONTEND_REPLICAS" -lt 2 ]; then
    print_error "Frontend deployment has $FRONTEND_REPLICAS ready replicas, expected at least 2"
fi

print_success "Replica counts are correct: Backend=$BACKEND_REPLICAS, Frontend=$FRONTEND_REPLICAS"

# Get the frontend service URL
print_status "Getting frontend service URL..."
FRONTEND_URL=$(minikube service todo-chatbot-frontend-service --url)
echo "🌐 Frontend URL: $FRONTEND_URL"

# Run validation checks
print_status "Running validation checks..."
cd ../../scripts
chmod +x validate-deployment.sh
./validate-deployment.sh

print_success "✅ All validation checks passed!"

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Summary:"
echo "  - Helm release: $RELEASE_NAME"
echo "  - Backend deployment: $BACKEND_REPLICAS/$BACKEND_REPLICAS ready"
echo "  - Frontend deployment: $FRONTEND_REPLICAS/$FRONTEND_REPLICAS ready"
echo "  - Frontend accessible at: $FRONTEND_URL"
echo ""
echo "🔧 Next steps:"
echo "  - Test the application functionality"
echo "  - Scale frontend if needed: kubectl scale deployment todo-chatbot-frontend --replicas=3"
echo "  - Monitor resources: kubectl top pods"
echo ""
echo "🗑️  To uninstall: helm uninstall todo-chatbot"