# Quickstart Guide: Stateless Chat API

## Overview
This guide explains how to set up and run the stateless chat API that persists conversations in a database while operating without server-side session storage.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance (or SQLite for development)
- Environment variables configured for database connection

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
cd backend
```

### 2. Install Dependencies
Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file with the following variables:
```env
DATABASE_URL=sqlite:///./chat_app.db
# For Neon Serverless PostgreSQL:
# DATABASE_URL=postgresql://username:password@host:port/database_name
DB_ECHO=true
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
MAX_MESSAGE_LENGTH=1000
ALLOWED_ORIGINS=*
```

### 4. Initialize Database
Run the database initialization:
```bash
python -c "from backend.src.database import create_db_and_tables; create_db_and_tables()"
```

### 5. Start the Server
```bash
uvicorn backend.src.main:app --reload --port 8000
```

## API Usage

### Starting a New Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help me?"}'
```

### Continuing an Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more about this topic",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

## Key Features

### Stateless Operation
- No server-side session storage
- All conversation state maintained in the database
- Server restarts do not affect conversation continuity

### Conversation Management
- Automatic creation of new conversations when no conversation_id provided
- Seamless continuation of existing conversations when conversation_id provided
- Persistent message history stored in database

### Error Handling
- 404 responses for invalid conversation IDs
- Proper validation of input parameters
- Comprehensive error messaging

## Testing

### Run Unit Tests
```bash
pytest backend/tests/unit/
```

### Run Integration Tests
```bash
pytest backend/tests/integration/
```

### Run Contract Tests
```bash
pytest backend/tests/contract/
```

### Test Conversation Continuity
1. Send a message to create a conversation
2. Restart the server
3. Send another message with the same conversation_id
4. Verify that the conversation continues properly

## Development

### Running the Application in Development Mode
```bash
export DEBUG=true
uvicorn backend.src.main:app --reload --port 8000
```

### Running with Different Databases
For development, you can use SQLite (default):
```
DATABASE_URL=sqlite:///./chat_app.db
```

For production, use PostgreSQL:
```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

## Troubleshooting

### Common Issues
- **Database Connection Errors**: Verify DATABASE_URL is correctly set
- **Invalid UUID Format**: Ensure conversation_id follows UUID format when provided
- **Empty Message Errors**: Message field is required and cannot be empty