# Data Model: Phase V Part A – Intermediate & Advanced Features

## Overview
This document defines the extended data models for implementing Phase V Part A features: priorities, tags, search/filter/sort, recurring tasks, and due date reminders.

## Entity Relationships

```
[User] 1----* [Task]
[Task] *----* [Tag] (Many-to-many relationship)
[Task] 1----1 [Reminder] (Optional)
[Task] 1----1 [RecurringTaskPattern] (Optional)
[RecurringTaskPattern] 1----* [Task] (Generated instances)
```

## Entity Definitions

### Task
Represents a single task with enhanced properties from Phase V features.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier for the task |
| title | String(255) | Required | Title of the task |
| description | Text | Optional | Detailed description of the task |
| user_id | UUID | Foreign Key | Owner of the task |
| priority | Enum(low, medium, high) | Default: medium | Priority level of the task |
| status | Enum(todo, in_progress, done) | Default: todo | Current status of the task |
| due_date | DateTime | Nullable | Optional due date for the task |
| created_at | DateTime | Auto-generated | Timestamp when task was created |
| updated_at | DateTime | Auto-generated | Timestamp when task was last updated |
| completed_at | DateTime | Nullable | Timestamp when task was completed |
| reminder_offset | Integer | Nullable | Minutes before due_date to send reminder |
| tags | Relationship | Many-to-many with Tag | Associated tags for the task |
| recurring_pattern_id | UUID | Foreign Key, Nullable | Reference to recurring pattern if applicable |

### Tag
Represents a tag that can be associated with multiple tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier for the tag |
| name | String(50) | Required, Unique per user | Name of the tag |
| user_id | UUID | Foreign Key | Owner of the tag |
| created_at | DateTime | Auto-generated | Timestamp when tag was created |

### RecurringTaskPattern
Defines a pattern for recurring tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier for the pattern |
| user_id | UUID | Foreign Key | Owner of the pattern |
| base_task_title | String(255) | Required | Title template for generated tasks |
| base_task_description | Text | Optional | Description template for generated tasks |
| recurrence_type | Enum(daily, weekly, monthly, custom) | Required | Type of recurrence |
| interval | Integer | Required | Interval between recurrences (e.g., every 2 weeks) |
| start_date | DateTime | Required | When the recurrence starts |
| end_date | DateTime | Nullable | When the recurrence ends (null for indefinite) |
| weekdays_mask | Integer | Optional | Bitmask for days of week (for weekly patterns) |
| created_at | DateTime | Auto-generated | Timestamp when pattern was created |
| updated_at | DateTime | Auto-generated | Timestamp when pattern was last updated |

### Reminder
Manages reminder settings and status for tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key | Unique identifier for the reminder |
| task_id | UUID | Foreign Key, Unique | Associated task |
| due_datetime | DateTime | Required | When the reminder is due |
| reminder_datetime | DateTime | Required | When the reminder should be sent |
| sent | Boolean | Default: false | Whether the reminder has been sent |
| snoozed_until | DateTime | Nullable | When the reminder is snoozed until |
| dismissed | Boolean | Default: false | Whether the reminder has been dismissed |
| created_at | DateTime | Auto-generated | Timestamp when reminder was created |
| updated_at | DateTime | Auto-generated | Timestamp when reminder was last updated |

## Validation Rules

### Task Validation
- A task can have a maximum of 5 tags
- Priority must be one of: low, medium, high
- Due date must be in the future if set
- Reminder offset must be positive if set

### Tag Validation
- Tag names must be unique per user
- Tag names must be 50 characters or less
- Tag names cannot be empty

### RecurringTaskPattern Validation
- Start date must be in the future
- End date must be after start date if specified
- Interval must be positive
- For weekly patterns, weekdays_mask must specify at least one day

### Reminder Validation
- Reminder datetime must be before due datetime
- Reminder cannot be scheduled in the past

## State Transitions

### Task Status Transitions
```
todo → in_progress → done
todo → done (direct completion)
in_progress → todo (revert)
done → todo (reopen)
```

### Reminder Status Transitions
```
created → scheduled → sent → (dismissed OR snoozed)
snoozed → rescheduled → sent
```

## Indexes for Performance

### Task Table
- Index on (user_id, priority) for priority filtering
- Index on (user_id, due_date) for due date filtering
- Index on (user_id, created_at) for chronological sorting
- Index on (user_id, status) for status filtering
- Full-text index on (title, description) for search

### Tag Table
- Index on (user_id, name) for efficient tag lookup

### RecurringTaskPattern Table
- Index on (user_id, start_date) for scheduling
- Index on (user_id, recurrence_type) for pattern queries

### Reminder Table
- Index on (task_id) for task association
- Index on (reminder_datetime, sent, dismissed) for scheduling queries

## Event-Driven Considerations

### Events Generated
- `task.created` - When a new task is created
- `task.updated` - When a task is updated
- `task.completed` - When a task is marked as done
- `task.deleted` - When a task is deleted
- `reminder.scheduled` - When a reminder is scheduled
- `reminder.sent` - When a reminder is sent
- `recurring.instance.created` - When a recurring task instance is created

These events will be published via Dapr pub/sub for consumption by other services.