# Stateless Chat API Documentation

## Overview
The Stateless Chat API provides a way to conduct conversations with an AI assistant while maintaining statelessness. All conversation data is persisted in the database, ensuring continuity across server restarts.

## API Endpoints

### POST /api/{user_id}/chat
Initiates or continues a conversation with the AI assistant.

#### Parameters
- `user_id` (path): Unique identifier for the user (required)

#### Request Body
```json
{
  "message": "string (required)",
  "conversation_id": "string (optional, UUID format)"
}
```

#### Request Body Fields
- `message`: The message content to send to the assistant (required, 1-1000 characters)
- `conversation_id`: Existing conversation ID to continue a conversation (optional, UUID format)

#### Response
```json
{
  "conversation_id": "string (UUID)",
  "message": "string"
}
```

#### Response Fields
- `conversation_id`: The conversation ID (newly created or existing)
- `message`: The assistant's response message

#### Status Codes
- `200`: Success
- `400`: Bad request (invalid conversation_id format)
- `404`: Conversation not found (when invalid conversation_id provided)
- `422`: Validation error (missing required fields, invalid format)
- `500`: Internal server error

#### Examples

**Start a new conversation:**
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help me?"}'
```

**Continue an existing conversation:**
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more about this topic",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

## Architecture

### Stateless Design
- No server-side session storage
- All conversation state maintained in the database
- Server restarts do not affect conversation continuity
- Each request fetches necessary data from the database

### Data Model
- **Conversation**: Represents a unique chat thread between a user and the assistant
  - id: UUID (primary key)
  - user_id: String (user identifier)
  - created_at: DateTime
  - updated_at: DateTime

- **Message**: Contains the content of a communication
  - id: UUID (primary key)
  - conversation_id: UUID (foreign key)
  - role: String (user or assistant)
  - content: String (message content)
  - timestamp: DateTime

## Environment Variables
- `DATABASE_URL`: Database connection string
- `DB_POOL_SIZE`: Database connection pool size (default: 5)
- `DB_MAX_OVERFLOW`: Maximum overflow connections (default: 10)
- `MAX_MESSAGE_LENGTH`: Maximum message length (default: 1000)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS