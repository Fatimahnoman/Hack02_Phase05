# Quickstart Guide: AI-Enhanced Chat API

## Overview
This guide explains how to set up and use the AI-enhanced chat API that leverages OpenAI Agents SDK for context-aware responses while maintaining the existing stateless architecture.

## Prerequisites
- Python 3.11+
- OpenAI API key
- Existing stateless chat API setup
- Environment variables configured for OpenAI and database

## Setup Instructions

### 1. Install AI Dependencies
```bash
pip install openai
```

### 2. Configure Environment Variables
Add the following to your `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
AGENT_TEMPERATURE=0.7
MAX_CONTEXT_TOKENS=8000
FALLBACK_RESPONSE="I'm having trouble responding right now. Could you try rephrasing?"
```

### 3. Update the Application
The AI enhancement integrates with the existing chat infrastructure. No major changes to the deployment process are required.

## API Usage

### Starting a New Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me with my todo list?"}'
```

### Continuing an Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What did I ask about earlier?",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

## Key Features

### AI-Enhanced Responses
- Responses demonstrate awareness of conversation history
- Maintains context across multiple turns
- Provides coherent, relevant answers based on previous exchanges

### Context Reconstruction
- Full conversation history is rebuilt from database on each request
- Maintains stateless architecture
- Survives server restarts

### Error Handling
- Graceful degradation when AI service is unavailable
- Fallback responses maintain user experience
- Proper error logging for troubleshooting

## Testing

### Verify AI Integration
1. Start a conversation with an initial message
2. Continue with follow-up messages that reference previous content
3. Verify the AI response shows awareness of the context

### Test Conversation Continuity
1. Send multiple messages in a conversation
2. Restart the server
3. Continue the conversation with the same conversation_id
4. Verify the AI still has context awareness

### Performance Testing
- Measure response times for AI-enhanced conversations
- Verify that the system meets performance goals (<10s for 95% of requests)
- Test concurrent conversations with AI integration

## Configuration

### Agent Settings
- `OPENAI_MODEL`: The model to use (gpt-4, gpt-3.5-turbo, etc.)
- `AGENT_TEMPERATURE`: Controls response creativity (0.0-2.0)
- `MAX_CONTEXT_TOKENS`: Maximum tokens for conversation context
- `FALLBACK_RESPONSE`: Response to use when AI service fails

### Performance Tuning
- Adjust context window size based on conversation length needs
- Tune temperature for desired response characteristics
- Monitor token usage for cost optimization