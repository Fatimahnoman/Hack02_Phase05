#!/bin/bash

# Script to run the validation of the Todo Chatbot deployment
# This script executes the validation checks to ensure the deployment is working properly

echo "Running deployment validation..."
echo ""

# Navigate to the scripts directory
cd ../scripts

# Make the validation script executable
chmod +x validate-deployment.sh

# Run the validation
./validate-deployment.sh

echo ""
echo "Validation completed!"