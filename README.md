# Evolution of Todo - Phase II

This project implements a full-stack todo application with authentication as specified in Phase II of the Evolution of Todo project.

## Features

- User registration and authentication
- Todo management (create, read, update, delete)
- Mark todos as complete/incomplete
- User-specific data isolation
- Responsive web interface

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- Better Auth
- Uvicorn (ASGI server)

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

3. Set up your database connection in `src/config.py`

4. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

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

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL database connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

### Frontend
- `NEXT_PUBLIC_API_URL`: Base URL for the backend API

## Project Structure

```
backend/
├── src/
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   ├── api/         # API routes
│   ├── database/    # Database configuration
│   └── config.py    # Configuration settings
└── requirements.txt # Dependencies

frontend/
├── src/
│   ├── components/  # React components
│   ├── pages/       # Next.js pages
│   ├── services/    # API services
│   ├── types/       # TypeScript types
│   └── hooks/       # React hooks
├── package.json     # Dependencies
└── next.config.js   # Next.js configuration
```

## Constraints

This implementation follows the Phase II constraints:
- No AI or agents
- No background jobs
- No real-time features
- No advanced analytics
- Uses only allowed technologies per constitution