# Research Summary: Phase V Part A – Intermediate & Advanced Features

## Overview
This document summarizes research conducted for implementing Phase V Part A features: priorities, tags, search/filter/sort, recurring tasks, and due date reminders in the Todo Chatbot system.

## Key Decisions

### 1. Natural Language Processing for Task Enhancement
**Decision**: Implement intent recognition for priority, tag, due date, and recurring task commands using rule-based parsing combined with ML classification.

**Rationale**: The existing chat interface needs to support natural language commands like "Make this high priority #work" and "Remind me every Monday at 9 AM". A hybrid approach combining rule-based parsing for structured elements (times, dates, tags) with ML classification for intent recognition provides accuracy and flexibility.

**Alternatives considered**:
- Pure rule-based parsing: Less flexible for varied user expressions
- Third-party NLP services: Higher cost and latency concerns
- Simple keyword matching: Insufficient for complex commands

### 2. Task Model Extension Approach
**Decision**: Extend the existing Task model with nullable fields for priority, tags, due date, and reminder settings rather than creating separate related tables.

**Rationale**: This maintains simplicity and avoids complex joins while keeping all task-related data in one place. The fields are frequently accessed together, making this approach more efficient.

**Alternatives considered**:
- Separate related tables: More normalized but requires joins
- JSON column for metadata: Flexible but harder to query efficiently

### 3. Tags Implementation
**Decision**: Implement tags as a separate table with a many-to-many relationship to tasks, limited to 5 tags per task as specified.

**Rationale**: This allows for efficient querying by tags and maintains data integrity. Storing tags separately prevents duplication and allows for tag-based statistics.

**Alternatives considered**:
- Array field in Task model: Simpler but less efficient for queries
- Comma-separated string: Not normalized and harder to query

### 4. Search and Filter Implementation
**Decision**: Use PostgreSQL full-text search capabilities combined with standard WHERE clauses for filtering and ORDER BY clauses for sorting.

**Rationale**: Leverages database capabilities for efficient search and filtering. PostgreSQL's full-text search is robust and performs well for the required functionality.

**Alternatives considered**:
- Elasticsearch: Overkill for this use case and adds complexity
- In-memory search: Would not scale well with large datasets

### 5. Recurring Tasks Implementation
**Decision**: Implement recurring tasks with a separate RecurringTaskPattern model that generates Task instances based on the pattern.

**Rationale**: This maintains separation between recurring patterns and actual tasks while allowing for proper tracking of individual task completions. The pattern generates new task instances as needed.

**Alternatives considered**:
- Calculating recurring tasks on-demand: Would be inefficient for long-running patterns
- Storing all future instances: Would consume excessive storage

### 6. Reminder System Architecture
**Decision**: Use Dapr's pub/sub for event-driven reminder notifications and leverage Dapr's state management for tracking reminder status.

**Rationale**: Aligns with the event-driven architecture mandated by the constitution. Dapr provides reliable messaging and state management with built-in retry mechanisms.

**Alternatives considered**:
- Cron jobs: Doesn't fit the event-driven architecture
- Polling mechanism: Prohibited by constitution and inefficient

### 7. Event Schema Design
**Decision**: Create standardized event schemas using Pydantic models for all task-related events (creation, update, completion, deletion).

**Rationale**: Ensures consistency and validation across all services. Pydantic models provide automatic validation and serialization.

**Alternatives considered**:
- Unstructured JSON: Lacks validation and consistency
- Custom validation: Reinventing existing solutions

## Technical Challenges Identified

### 1. Timezone Handling
Challenge: Managing due dates and reminders across different timezones.
Solution: Store all datetimes in UTC and convert to user's timezone for display/processing.

### 2. Natural Language Date Parsing
Challenge: Accurately parsing various date/time formats from natural language.
Solution: Use libraries like dateutil and duckling for robust parsing.

### 3. Recurring Task Edge Cases
Challenge: Handling complex recurrence patterns and exceptions.
Solution: Start with basic patterns (daily, weekly, monthly) and expand as needed.

## Architecture Considerations

### Event-Driven Design
All new features will emit events through Dapr pub/sub to maintain loose coupling. For example:
- Creating a task with a due date triggers a "reminder_scheduled" event
- Completing a recurring task instance triggers a "next_instance_created" event

### Dapr Integration
All infrastructure interactions will use Dapr building blocks:
- State management for task persistence
- Pub/sub for event communication
- Secrets for configuration
- Service invocation for inter-service communication

### Performance Optimization
- Indexes on priority, tags, due dates for efficient filtering
- Full-text search indexes for search functionality
- Caching for frequently accessed data