# Evolution of Todo - Phase III: Conversational AI Layer using OpenAI Agents SDK

This project implements a full-stack todo application with authentication and an AI-powered conversational layer as specified in Phase III of the Evolution of Todo project.

## Features

- User registration and authentication
- Todo management (create, read, update, delete)
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive web interface
- **NEW**: AI-powered chat with context-aware responses
- **NEW**: Conversation history persistence
- **NEW**: Context reconstruction from database
- **NEW**: Error handling and fallback responses for AI services

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Better Auth
- Uvicorn (ASGI server)
- OpenAI API
- **NEW**: OpenAI Agents SDK

### Frontend
- Next.js 14
- React
- TypeScript
- Axios for API calls

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables in `.env` file (defaults to SQLite for local development):
   ```
   DATABASE_URL=sqlite:///./chat_app.db
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DB_ECHO=False
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   AGENT_TEMPERATURE=0.7
   MAX_CONTEXT_TOKENS=8000
   MAX_RESPONSE_TOKENS=1000
   FALLBACK_RESPONSE=I'm having trouble responding right now. Could you try rephrasing?
   ```

4. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

**Note**: The application defaults to SQLite database for easy local development. For production, you can switch to PostgreSQL by changing the DATABASE_URL in your .env file.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Todos
- `GET /api/todos/` - Get all todos for authenticated user
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo
- `PATCH /api/todos/{id}/status` - Update todo completion status

### Chat
- `POST /api/{user_id}/chat` - Send a message and get AI-powered response with conversation context
  Request body:
  ```json
  {
    "message": "string (required)",
    "conversation_id": "string (optional, UUID format)"
  }
  ```
  Response:
  ```json
  {
    "conversation_id": "string (UUID)",
    "message": "string (AI-generated response)"
  }
  ```

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL database connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `OPENAI_API_KEY`: OpenAI API key for AI agent integration
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `AGENT_TEMPERATURE`: Creativity parameter for AI responses (default: 0.7)
- `MAX_CONTEXT_TOKENS`: Maximum tokens for conversation context (default: 8000)
- `MAX_RESPONSE_TOKENS`: Maximum tokens for AI responses (default: 1000)
- `FALLBACK_RESPONSE`: Response to use when AI service fails

### Frontend
- `NEXT_PUBLIC_API_URL`: Base URL for the backend API

## Project Structure

```
backend/
├── src/
│   ├── models/          # Data models
│   │   ├── conversation.py  # Conversation data model
│   │   ├── message.py       # Message data model
│   │   └── ai_config.py     # AI configuration model
│   ├── services/        # Business logic
│   │   ├── chat_service.py       # Chat operations
│   │   ├── conversation_service.py # Conversation management
│   │   ├── ai_agent_service.py   # AI agent integration service
│   │   ├── context_builder.py    # Conversation context building
│   │   ├── ai_error_handler.py   # Error handling utilities
│   │   └── circuit_breaker.py    # Circuit breaker pattern
│   ├── api/             # API routes
│   │   └── chat_router.py        # Chat API endpoints
│   ├── database/        # Database configuration
│   ├── config.py        # Configuration settings
│   └── main.py          # FastAPI app entry point
└── requirements.txt     # Dependencies

frontend/
├── src/
│   ├── components/  # React components
│   ├── pages/       # Next.js pages
│   ├── services/    # API services
│   ├── types/       # TypeScript types
│   └── hooks/       # React hooks
├── package.json     # Dependencies
└── next.config.js   # Next.js configuration

specs/
└── 001-ai-agents-sdk/  # Specification documents
    ├── spec.md         # Feature specification
    ├── plan.md         # Implementation plan
    ├── data-model.md   # Data model
    ├── contracts/      # API contracts
    └── tasks.md        # Implementation tasks

history/
└── prompts/           # Prompt History Records
    └── 001-ai-agents-sdk/
```

## AI Agent Integration Features

### Context-Aware AI Responses
- The AI agent receives full conversation history before generating a response
- Responses demonstrate understanding of conversation context and history
- Maintains coherent, multi-turn conversations

### Persistent Conversation Context
- Conversation context is reconstructed from database records on each request
- Maintains stateless operation without storing conversation context in server memory
- Functions properly after server restarts with access to previous conversation history

### Error Handling & Resilience
- Graceful degradation when AI service is unavailable
- Fallback responses maintain user experience during API failures
- Circuit breaker pattern for API resilience
- Comprehensive logging for debugging

### Performance & Optimization
- Context window management with token limit handling
- Conversation history caching for improved performance
- Response validation before database persistence

## Running the Application

### Running Backend
1. Set up environment variables (as described above)
2. Navigate to the backend directory: `cd backend`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `uvicorn src.main:app --reload --port 8000`
5. The application will be available at `http://localhost:8000`
6. API documentation available at `http://localhost:8000/docs`

### Running Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create `.env.local` file with API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run the development server: `npm run dev`
5. The frontend will be available at `http://localhost:3000`

### Registration and Login
1. To register a new user, send a POST request to `/api/auth/register` with:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
2. To login, send a POST request to `/api/auth/login` with:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```

### Testing the AI Chat Functionality
1. Start both backend and frontend
2. Register or login to get an access token
3. Access the frontend at `http://localhost:3000`
4. Use the chat interface to interact with the AI agent
5. The AI will remember conversation context across multiple messages in the same conversation

## Constraints

This implementation follows the Phase III+ constraints:
- Uses approved AI/agent frameworks (OpenAI Agents SDK)
- Maintains stateless architecture
- Builds upon Phase II infrastructure (Python FastAPI, SQLModel, PostgreSQL)
- Properly layered architecture following existing patterns