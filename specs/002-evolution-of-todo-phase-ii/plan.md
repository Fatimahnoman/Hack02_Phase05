# Implementation Plan: Evolution of Todo - Phase II

**Branch**: `002-evolution-of-todo-phase-ii` | **Date**: 2026-01-05 | **Spec**: [specs/002-evolution-of-todo-phase-ii.md](../002-evolution-of-todo-phase-ii.md)
**Input**: Feature specification from `/specs/[002-evolution-of-todo-phase-ii]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a full-stack todo application with Python REST API backend, Neon Serverless PostgreSQL database, Better Auth authentication, and Next.js frontend. The system will provide complete todo management functionality with proper user authentication and data isolation.

## Technical Context

**Language/Version**: Python 3.11 for backend, TypeScript/JavaScript for frontend
**Primary Dependencies**: FastAPI for backend API, Better Auth for authentication, SQLModel for ORM, Next.js 14+ for frontend
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for backend, Jest/React Testing Library for frontend
**Target Platform**: Web application (desktop and mobile browsers)
**Project Type**: Web (backend + frontend)
**Performance Goals**: API response time under 500ms, UI load time under 3 seconds
**Constraints**: No AI, no agents, no background workers, no future phase infrastructure
**Scale/Scope**: Individual user todo management, single-user operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Phase II: Full-stack web application allowed per constitution
- ✅ Backend: Python REST API allowed per constitution
- ✅ Database: Neon Serverless PostgreSQL allowed per constitution
- ✅ ORM/Data layer: SQLModel or equivalent allowed per constitution
- ✅ Frontend: Next.js (React, TypeScript) allowed per constitution
- ✅ Authentication: Better Auth allowed per constitution
- ✅ No AI or agent frameworks (Phase III+ requirement) - compliant
- ✅ Web frontend allowed starting Phase II - compliant
- ✅ Authentication allowed starting Phase II - compliant

## Project Structure

### Documentation (this feature)

```text
specs/002-evolution-of-todo-phase-ii/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── todo.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── todo_service.py
│   ├── api/
│   │   ├── auth_router.py
│   │   └── todo_router.py
│   ├── database/
│   │   └── database.py
│   └── main.py
├── requirements.txt
└── alembic/
    └── versions/

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignupForm.tsx
│   │   │   └── SigninForm.tsx
│   │   ├── todos/
│   │   │   ├── TodoItem.tsx
│   │   │   ├── TodoList.tsx
│   │   │   └── TodoForm.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Layout.tsx
│   ├── pages/
│   │   ├── signup.tsx
│   │   ├── signin.tsx
│   │   ├── dashboard.tsx
│   │   └── index.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── auth.ts
│   ├── hooks/
│   │   └── useAuth.ts
│   └── types/
│       └── index.ts
├── package.json
├── next.config.js
├── tsconfig.json
└── .env.local
```

**Structure Decision**: Selected Option 2: Web application structure to separate backend API from frontend Next.js application, allowing for proper API contract design and independent development.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [No violations found] | [Compliant with constitution] | [All requirements follow Phase II guidelines] |

## Backend Plan

### 1. Backend Framework Responsibility (REST API)
- Use FastAPI as the primary web framework for building the REST API
- Implement API endpoints following RESTful conventions
- Handle request validation, response formatting, and error handling
- Configure CORS middleware to allow frontend communication

### 2. API Routing and Controller Structure
- Create separate routers for authentication and todo operations
- Implement proper request/response models using Pydantic
- Structure endpoints following REST conventions:
  - POST /api/todos: Create new todo
  - GET /api/todos: Retrieve user's todos
  - PUT /api/todos/{id}: Update todo
  - DELETE /api/todos/{id}: Delete todo
  - PATCH /api/todos/{id}/status: Update completion status

### 3. Authentication Integration using Better Auth
- Integrate Better Auth for user registration and authentication
- Implement middleware to protect endpoints requiring authentication
- Handle JWT token validation and user session management
- Ensure only authenticated users can access their own data

### 4. Data Persistence using Neon PostgreSQL
- Use SQLModel as the ORM for database operations
- Connect to Neon Serverless PostgreSQL database
- Implement repository patterns for data access
- Handle database migrations using Alembic

### 5. User-to-Do Data Ownership Handling
- Implement user ID validation in all todo operations
- Ensure users can only access, modify, or delete their own todos
- Include user_id in all todo queries and filters
- Return 403 Forbidden for unauthorized access attempts

### 6. Error Handling and Validation Approach
- Implement centralized error handling middleware
- Use Pydantic for request validation
- Return appropriate HTTP status codes (400, 401, 403, 404, 500)
- Provide meaningful error messages to the frontend

## Frontend Plan

### 1. Next.js Application Structure
- Use Next.js 14+ with App Router for page routing
- Implement server-side rendering where appropriate
- Use TypeScript for type safety
- Structure components in a reusable and maintainable way

### 2. Page-Level Routing (auth pages + todo pages)
- Create pages for authentication: /signup, /signin
- Create pages for todo management: /dashboard, /todos
- Implement protected route handling with authentication checks
- Use Next.js middleware for route protection

### 3. Component Responsibilities
- Auth components: SignupForm, SigninForm for user registration/login
- Todo components: TodoItem, TodoList, TodoForm for todo operations
- Layout components: Header, Layout for consistent UI structure
- Reusable UI components for consistent design system

### 4. API Communication Strategy
- Create service layer for API communication (axios or fetch)
- Implement proper request/response handling
- Include error handling for network failures
- Add loading states for better UX

### 5. Authentication State Handling
- Implement custom hook (useAuth) for authentication state management
- Store authentication tokens securely
- Handle token expiration and refresh
- Redirect users based on authentication status

### 6. Responsive UI Strategy
- Use CSS Grid/Flexbox for responsive layouts
- Implement mobile-first design approach
- Use media queries for different screen sizes
- Test UI on various device sizes

## Database Plan

### 1. User Data Model
- User model with id, email, password hash, created_at, updated_at
- Email uniqueness constraint
- Password stored with proper hashing
- Integration with Better Auth system

### 2. Todo Data Model
- Todo model with id, title, description, completed status, user_id, created_at, updated_at
- Title as required field
- Completed status as boolean with default false
- Timestamps for creation and updates

### 3. Relationship between User and Todo
- Foreign key relationship from Todo.user_id to User.id
- Cascade delete for todos when user is deleted
- Index on user_id for efficient queries

### 4. Migration or Schema Management Approach
- Use Alembic for database migrations
- Create initial migration for user and todo tables
- Version control for schema changes
- Environment-specific configuration for Neon PostgreSQL

## Integration Plan

### 1. Frontend ↔ Backend Communication Flow
- REST API communication using JSON format
- Proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Consistent API response structure
- Error response handling

### 2. Auth Token/Session Flow
- JWT token exchange during authentication
- Token storage in browser (securely)
- Token inclusion in API request headers
- Token refresh mechanism

### 3. Local Development Setup
- Separate environment configurations for local, staging, production
- Docker setup for consistent local development
- Environment variables for API URLs and database connections
- Development server configuration for both frontend and backend