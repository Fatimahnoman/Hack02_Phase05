#!/bin/bash
# Test script to verify chatbot task operations work correctly

echo "Testing ChatBot Task Operations"
echo "==============================="

echo ""
echo "1. Testing Chat endpoint for task creation..."

# First, let's get an access token for a valid user
echo "Getting access token..."
TOKEN=$(curl -s -X POST http://127.0.0.1:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"NewUserPassword123!"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Using token: ${TOKEN:0:20}..."

echo ""
echo "2. Testing chatbot to create a task..."
curl -X POST http://127.0.0.1:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Please create a new task titled \"ChatBot Test Task\" with description \"This task was created via the chatbot interface\""}'

echo ""
echo ""
echo "3. Testing chatbot to list tasks..."
curl -X POST http://127.0.0.1:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Please list all my tasks"}'

echo ""
echo ""
echo "4. Testing chatbot to update a task..."
curl -X POST http://127.0.0.1:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Please update the task \"ChatBot Test Task\" to have the description \"This task was updated via the chatbot interface\""}'

echo ""
echo ""
echo "5. Testing chatbot to complete a task..."
curl -X POST http://127.0.0.1:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Please mark the task \"ChatBot Test Task\" as completed"}'

echo ""
echo ""
echo "6. Testing chatbot to delete a task..."
curl -X POST http://127.0.0.1:8001/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"Please delete the task titled \"ChatBot Test Task\""}'

echo ""
echo "Test completed!"