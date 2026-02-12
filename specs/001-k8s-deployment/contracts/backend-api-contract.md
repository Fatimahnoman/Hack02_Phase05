# Todo Chatbot API Contract

## Overview
This document specifies the API contract for the Todo Chatbot backend service that the frontend will communicate with.

## Base URL
The backend service will be accessible at the URL specified by the NEXT_PUBLIC_API_URL environment variable, which defaults to `http://todo-chatbot-backend-service:8000` within the Kubernetes cluster.

## Endpoints

### Health Checks
- `GET /health` - Returns health status of the backend service
- `GET /ready` - Returns readiness status of the backend service

### Todo Operations
- `GET /api/todos/` - Retrieve all todos for the authenticated user
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/{id}` - Retrieve a specific todo by ID
- `PUT /api/todos/{id}` - Update a specific todo by ID
- `DELETE /api/todos/{id}` - Delete a specific todo by ID
- `PATCH /api/todos/{id}/status` - Update the completion status of a specific todo

### Chat Operations
- `POST /api/{user_id}/chat` - Send a message to the chatbot and receive a response

## Request/Response Examples

### Get All Todos
- Request: `GET /api/todos/`
- Response (200):
```json
[
  {
    "id": 1,
    "title": "Sample Todo",
    "description": "A sample todo item",
    "completed": false,
    "created_at": "2026-02-12T10:00:00Z",
    "updated_at": "2026-02-12T10:00:00Z"
  }
]
```

### Create Todo
- Request: `POST /api/todos/`
- Body:
```json
{
  "title": "New Todo",
  "description": "A new todo item"
}
```
- Response (201):
```json
{
  "id": 2,
  "title": "New Todo",
  "description": "A new todo item",
  "completed": false,
  "created_at": "2026-02-12T10:00:00Z",
  "updated_at": "2026-02-12T10:00:00Z"
}
```

### Chat Endpoint
- Request: `POST /api/user123/chat`
- Body:
```json
{
  "message": "What are my todos?"
}
```
- Response (200):
```json
{
  "conversation_id": "uuid-string",
  "message": "You have 2 todos: 'Sample Todo' and 'New Todo'"
}
```

## Error Responses
All error responses follow the format:
```json
{
  "detail": "Error message"
}
```

## Environment Variables
The frontend service must have the following environment variable configured:
- `NEXT_PUBLIC_API_URL`: The base URL for the backend API (e.g., `http://todo-chatbot-backend-service:8000`)