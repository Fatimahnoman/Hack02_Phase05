#!/bin/bash

# Todo Chatbot Deployment Script for Minikube
# This script automates the deployment of the Todo Chatbot application to Minikube

set -e  # Exit on any error

echo "🚀 Starting Todo Chatbot deployment to Minikube..."

# Function to print status messages
print_status() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Check if Minikube is running
print_status "Checking Minikube status..."
if ! minikube status &>/dev/null; then
    print_status "Starting Minikube..."
    minikube start --driver=docker --cpus=4 --memory=8192mb --disk-size=40gb
else
    print_status "Minikube is already running"
fi

# Set Docker environment to use Minikube's Docker daemon
print_status "Configuring Docker to use Minikube daemon..."
eval $(minikube docker-env)

# Build backend Docker image
print_status "Building backend Docker image..."
cd ../backend
docker build -t todo-backend:latest . --no-cache
cd ../..

# Build frontend Docker image
print_status "Building frontend Docker image..."
cd ../frontend
docker build -t todo-frontend:latest . --no-cache
cd ../..

# Verify images were built successfully
print_status "Verifying Docker images..."
if [[ "$(docker images -q todo-backend:latest 2> /dev/null)" == "" ]]; then
    echo "❌ Backend image not found"
    exit 1
else
    print_status "✅ Backend image found"
fi

if [[ "$(docker images -q todo-frontend:latest 2> /dev/null)" == "" ]]; then
    echo "❌ Frontend image not found"
    exit 1
else
    print_status "✅ Frontend image found"
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

print_status "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

print_status "Checking deployment status..."
kubectl get deployments
kubectl get pods
kubectl get services

# Get the frontend service URL
print_status "Getting frontend service URL..."
FRONTEND_URL=$(minikube service todo-chatbot-frontend-service --url)
echo "🌐 Frontend URL: $FRONTEND_URL"

print_status "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Access the frontend at: $FRONTEND_URL"
echo "2. Verify backend connectivity by checking logs: kubectl logs -l app=backend"
echo "3. Test the application functionality"
echo ""
echo "🔧 To scale frontend: kubectl scale deployment todo-chatbot-frontend --replicas=3"
echo "🗑️  To uninstall: helm uninstall todo-chatbot"