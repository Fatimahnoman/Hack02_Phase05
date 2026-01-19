# API Contract: AI-Enhanced Chat API

## Overview
The API contract remains unchanged from the original stateless chat API. The AI enhancement occurs internally without modifying the public interface.

## Endpoints

### POST /api/{user_id}/chat

**Description**: Accepts user messages and returns AI-generated responses with conversation context awareness.

**Request**:
```json
{
  "message": "string (required)",
  "conversation_id": "string (optional, UUID format)"
}
```

**Response**:
```json
{
  "conversation_id": "string (UUID)",
  "message": "string (AI-generated response)"
}
```

**Status Codes**:
- 200: Success - AI response generated
- 400: Bad request - Invalid conversation_id format
- 404: Not found - Conversation does not exist
- 422: Validation error - Missing required fields
- 500: Internal server error - AI service unavailable

## Behavior Changes (Internal)

### With AI Integration:
- The agent receives full conversation history before generating a response
- Responses demonstrate awareness of previous conversation turns
- Context is reconstructed from database on each request
- Maintains stateless operation

### Original Contract Preserved:
- Same request/response structure
- Same error handling patterns
- Same authentication patterns
- Same performance characteristics