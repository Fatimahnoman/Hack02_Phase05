# Quickstart Guide: Phase V Part A Features

## Overview
This guide provides instructions for getting started with the new Phase V features: priorities, tags, search/filter/sort, recurring tasks, and due date reminders.

## Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Dapr installed and initialized
- PostgreSQL database (Neon recommended)
- Node.js and npm (for frontend)

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Initialize Dapr
```bash
dapr init
```

### 3. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
DAPR_HOST=localhost
DAPR_HTTP_PORT=3500
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run Database Migrations
```bash
cd backend
python -m src.database.migrate
```

### 6. Start the Backend Service
```bash
cd backend
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3501 -- uvicorn src.main:app --reload --port 8000
```

### 7. Start the Frontend (if applicable)
```bash
cd frontend
npm install
npm run dev
```

## Using Phase V Features

### Setting Task Priorities
Create a task with a specific priority:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Critical Bug Fix",
    "description": "Fix the authentication issue",
    "priority": "high"
  }'
```

### Adding Tags to Tasks
Create a task with tags:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare presentation",
    "description": "Slides for quarterly review",
    "tags": ["work", "presentation", "important"]
  }'
```

### Searching Tasks
Search tasks by content:
```bash
curl "http://localhost:8000/api/v1/tasks/search?q=presentation&priority=high" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Filtering and Sorting Tasks
Get tasks filtered by priority and sorted by due date:
```bash
curl "http://localhost:8000/api/v1/tasks?priority=high&sort_by=due_date&sort_order=asc" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Creating Recurring Tasks
Create a weekly recurring task:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "description": "Weekly team sync meeting",
    "recurring_pattern": {
      "recurrence_type": "weekly",
      "interval": 1,
      "start_date": "2023-12-01T00:00:00Z",
      "weekdays_mask": 31  // Mon-Fri
    }
  }'
```

### Setting Due Dates and Reminders
Create a task with a due date and reminder:
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Submit quarterly report",
    "description": "Annual financial report",
    "due_date": "2023-12-15T17:00:00Z",
    "reminder_offset": 1440  // 24 hours in minutes
  }'
```

## Natural Language Commands
The system supports natural language processing for task creation. Examples:
- "Create a task 'Buy groceries' with high priority and tag it #shopping"
- "Set a reminder for 'Doctor appointment' on Friday at 3 PM"
- "Create a recurring task 'Water plants' every Monday"

## Event-Driven Architecture
The system uses Dapr pub/sub for event-driven communication:
- Task creation triggers `task.created` event
- Due date setting schedules `reminder.scheduled` event
- Recurring task completion triggers `recurring.instance.created` event

Monitor events using Dapr dashboard:
```bash
dapr dashboard
```

## Testing the Features
Run the test suite to verify all features work correctly:
```bash
cd backend
pytest tests/ -v
```

## Troubleshooting
- If Dapr sidecar isn't starting, ensure Dapr is properly initialized
- If database migrations fail, check your database connection settings
- If reminders aren't working, verify Dapr pub/sub component is configured correctly
- For authentication issues, ensure your JWT token is valid and not expired

## Next Steps
- Explore the API documentation at `/docs`
- Review the data model for advanced queries
- Set up monitoring and observability with Dapr
- Deploy to Kubernetes with the provided Helm charts