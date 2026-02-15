# API Contracts: Task Management with Phase V Features

## Overview
This document defines the API contracts for the extended task management functionality including priorities, tags, search/filter/sort, recurring tasks, and due date reminders.

## Base URL
`/api/v1`

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Common Error Responses
All endpoints may return:
- `401 Unauthorized` - Invalid or missing authentication token
- `403 Forbidden` - User not authorized to access the resource
- `422 Unprocessable Entity` - Invalid request data
- `500 Internal Server Error` - Unexpected server error

---

## Task Management Endpoints

### GET /tasks
Retrieve a list of tasks with filtering, sorting, and pagination capabilities.

#### Query Parameters
- `priority` (optional) - Filter by priority (low, medium, high)
- `tag` (optional) - Filter by tag name (can be repeated for multiple tags)
- `due_date_from` (optional) - Filter tasks with due date >= this date (ISO 8601 format)
- `due_date_to` (optional) - Filter tasks with due date <= this date (ISO 8601 format)
- `without_due_date` (optional) - If true, include only tasks without due dates
- `status` (optional) - Filter by status (todo, in_progress, done)
- `sort_by` (optional) - Sort by field (due_date, priority, created_at, title) - default: created_at
- `sort_order` (optional) - Sort order (asc, desc) - default: desc
- `page` (optional) - Page number for pagination - default: 1
- `limit` (optional) - Number of items per page - default: 20, max: 100

#### Response (200 OK)
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "priority": "high",
      "status": "todo",
      "due_date": "2023-12-31T10:00:00Z",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z",
      "completed_at": "2023-12-01T10:00:00Z",
      "tags": [
        {
          "id": "uuid-string",
          "name": "work"
        }
      ],
      "reminder_offset": 60
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

### POST /tasks
Create a new task with optional priority, tags, due date, and reminder settings.

#### Request Body
```json
{
  "title": "Task title",
  "description": "Task description",
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z",
  "reminder_offset": 60,
  "tags": ["work", "important"],
  "recurring_pattern": {
    "recurrence_type": "weekly",
    "interval": 1,
    "start_date": "2023-12-01T00:00:00Z",
    "end_date": "2024-12-01T00:00:00Z",
    "weekdays_mask": 62  // bitmask for Mon-Fri
  }
}
```

#### Response (201 Created)
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "priority": "medium",
  "status": "todo",
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "tags": [
    {
      "id": "uuid-string",
      "name": "work"
    }
  ],
  "reminder_offset": 60,
  "recurring_pattern_id": "uuid-string"
}
```

### GET /tasks/{id}
Retrieve a specific task by ID.

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "priority": "high",
  "status": "todo",
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "completed_at": "2023-12-01T10:00:00Z",
  "tags": [
    {
      "id": "uuid-string",
      "name": "work"
    }
  ],
  "reminder_offset": 60
}
```

### PUT /tasks/{id}
Update an existing task.

#### Request Body
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2023-12-31T10:00:00Z",
  "reminder_offset": 120,
  "tags": ["work", "urgent"]
}
```

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated task description",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2023-12-31T10:00:00Z",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-02T10:00:00Z",
  "completed_at": null,
  "tags": [
    {
      "id": "uuid-string",
      "name": "work"
    },
    {
      "id": "uuid-string",
      "name": "urgent"
    }
  ],
  "reminder_offset": 120
}
```

### DELETE /tasks/{id}
Delete a specific task.

#### Response (204 No Content)

---

## Search Endpoints

### GET /tasks/search
Search tasks by title and description with full-text search capabilities.

#### Query Parameters
- `q` (required) - Search query string
- `priority` (optional) - Filter by priority (low, medium, high)
- `tag` (optional) - Filter by tag name (can be repeated for multiple tags)
- `status` (optional) - Filter by status (todo, in_progress, done)
- `sort_by` (optional) - Sort by field (relevance, due_date, priority, created_at, title) - default: relevance
- `sort_order` (optional) - Sort order (asc, desc) - default: desc
- `page` (optional) - Page number for pagination - default: 1
- `limit` (optional) - Number of items per page - default: 20, max: 100

#### Response (200 OK)
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "priority": "high",
      "status": "todo",
      "due_date": "2023-12-31T10:00:00Z",
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z",
      "tags": [
        {
          "id": "uuid-string",
          "name": "work"
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "pages": 1
  },
  "search_info": {
    "query": "meeting",
    "took_ms": 15
  }
}
```

---

## Tag Management Endpoints

### GET /tags
Retrieve a list of tags for the authenticated user.

#### Response (200 OK)
```json
{
  "tags": [
    {
      "id": "uuid-string",
      "name": "work",
      "usage_count": 15
    },
    {
      "id": "uuid-string",
      "name": "personal",
      "usage_count": 8
    }
  ]
}
```

### POST /tags
Create a new tag for the authenticated user.

#### Request Body
```json
{
  "name": "important"
}
```

#### Response (201 Created)
```json
{
  "id": "uuid-string",
  "name": "important",
  "usage_count": 0
}
```

---

## Recurring Task Endpoints

### GET /recurring-patterns
Retrieve a list of recurring task patterns for the authenticated user.

#### Response (200 OK)
```json
{
  "patterns": [
    {
      "id": "uuid-string",
      "base_task_title": "Team Meeting",
      "base_task_description": "Weekly team sync",
      "recurrence_type": "weekly",
      "interval": 1,
      "start_date": "2023-12-01T00:00:00Z",
      "end_date": "2024-12-01T00:00:00Z",
      "weekdays_mask": 62,
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  ]
}
```

### POST /recurring-patterns
Create a new recurring task pattern.

#### Request Body
```json
{
  "base_task_title": "Team Meeting",
  "base_task_description": "Weekly team sync",
  "recurrence_type": "weekly",
  "interval": 1,
  "start_date": "2023-12-01T00:00:00Z",
  "end_date": "2024-12-01T00:00:00Z",
  "weekdays_mask": 62
}
```

#### Response (201 Created)
```json
{
  "id": "uuid-string",
  "base_task_title": "Team Meeting",
  "base_task_description": "Weekly team sync",
  "recurrence_type": "weekly",
  "interval": 1,
  "start_date": "2023-12-01T00:00:00Z",
  "end_date": "2024-12-01T00:00:00Z",
  "weekdays_mask": 62,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

---

## Reminder Management Endpoints

### GET /reminders/upcoming
Retrieve a list of upcoming reminders for the authenticated user.

#### Query Parameters
- `hours_ahead` (optional) - Number of hours ahead to look for reminders - default: 24

#### Response (200 OK)
```json
{
  "reminders": [
    {
      "id": "uuid-string",
      "task_id": "uuid-string",
      "task_title": "Submit report",
      "due_datetime": "2023-12-01T15:00:00Z",
      "reminder_datetime": "2023-12-01T14:00:00Z",
      "sent": false,
      "snoozed_until": null,
      "dismissed": false,
      "created_at": "2023-12-01T10:00:00Z",
      "updated_at": "2023-12-01T10:00:00Z"
    }
  ]
}
```

### POST /reminders/{id}/snooze
Snooze a specific reminder.

#### Request Body
```json
{
  "minutes": 30
}
```

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "task_id": "uuid-string",
  "due_datetime": "2023-12-01T15:00:00Z",
  "reminder_datetime": "2023-12-01T14:30:00Z",  // Updated time
  "sent": false,
  "snoozed_until": "2023-12-01T14:30:00Z",
  "dismissed": false,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:30:00Z"
}
```

### POST /reminders/{id}/dismiss
Dismiss a specific reminder.

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "task_id": "uuid-string",
  "due_datetime": "2023-12-01T15:00:00Z",
  "reminder_datetime": "2023-12-01T14:00:00Z",
  "sent": false,
  "snoozed_until": null,
  "dismissed": true,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:30:00Z"
}
```