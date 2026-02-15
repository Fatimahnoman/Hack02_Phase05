---

description: "Task list template for feature implementation"
---

# Tasks: Phase V Part A – Intermediate & Advanced Features

**Input**: Design documents from `/specs/004-phase-v-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Event-driven microservices**: `chat-api/`, `recurring-task-service/`, `notification-service/`, etc.
- **Dapr components**: `dapr-components/` at repository root
- **Tests**: `tests/` in each service directory
- Paths shown below assume microservices structure - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Dapr component definitions from dapr-components/
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure with Dapr setup

- [X] T001 Create project structure per implementation plan with Dapr components
- [X] T002 [P] Update requirements.txt with new dependencies (Dapr SDK, Pydantic, Celery)
- [X] T003 [P] Set up Dapr component definitions for Pub/Sub, State, and Secrets
- [X] T004 Configure local Minikube and Dapr runtime environment
- [X] T005 [P] Update Dockerfile to include new dependencies for Phase V features

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T006 [P] Update Task model with priority, due_date, reminder_offset fields in src/models/task.py
- [X] T007 [P] Create Tag model with many-to-many relationship to Task in src/models/tag.py
- [X] T008 Create RecurringTaskPattern model in src/models/recurring_task.py
- [X] T009 Create Reminder model in src/models/reminder.py
- [X] T010 [P] Update database schema with new indexes for performance in src/database/schema.sql
- [X] T011 [P] Implement Dapr client utilities for state management in src/dapr/client.py
- [X] T012 [P] Implement Dapr pub/sub utilities for event handling in src/dapr/pubsub.py
- [X] T013 Create event schemas using Pydantic models in src/events/schemas.py
- [X] T014 [P] Set up event handlers for task lifecycle events in src/events/handlers.py
- [X] T015 Update existing task service to handle new fields in src/services/task_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Set Task Priorities and Tags (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign priorities and tags to tasks with medium as default priority

**Independent Test**: Can be fully tested by creating tasks with different priorities and tags, verifying they appear correctly in the UI and that default priority is applied when none is specified.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T016 [P] [US1] Contract test for POST /tasks with priority and tags in tests/contract/test_task_creation.py
- [X] T017 [P] [US1] Unit test for Task model validation with priority and tags in tests/unit/test_task_model.py

### Implementation for User Story 1

- [X] T018 [P] [US1] Update Task model with priority enum and default in src/models/task.py
- [X] T019 [P] [US1] Create Tag model with validation rules in src/models/tag.py
- [X] T020 [P] [US1] Create TagService for managing tags in src/services/tag_service.py
- [X] T021 [US1] Update TaskService to handle tags and priority in src/services/task_service.py
- [X] T022 [US1] Update POST /tasks endpoint to accept priority and tags in src/api/task_router.py
- [X] T023 [US1] Update GET /tasks endpoint to return priority and tags in src/api/task_router.py
- [X] T024 [US1] Update PUT /tasks/{id} endpoint to modify priority and tags in src/api/task_router.py
- [X] T025 [US1] Add validation for max 5 tags per task in src/services/task_service.py
- [X] T026 [US1] Add validation for priority enum values in src/models/task.py
- [X] T027 [US1] Create GET /tags endpoint in src/api/task_router.py
- [X] T028 [US1] Create POST /tags endpoint in src/api/task_router.py
- [X] T029 [US1] Add database indexes for priority and tags in src/database/schema.sql

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Search, Filter, and Sort Tasks (Priority: P2)

**Goal**: Enable users to search, filter, and sort tasks by various criteria

**Independent Test**: Can be fully tested by creating multiple tasks with different priorities, tags, and due dates, then applying various search, filter, and sort combinations to verify results match expectations.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US2] Contract test for GET /tasks with filters in tests/contract/test_task_filters.py
- [X] T031 [P] [US2] Contract test for GET /tasks/search endpoint in tests/contract/test_task_search.py
- [X] T032 [P] [US2] Integration test for search functionality in tests/integration/test_search.py

### Implementation for User Story 2

- [X] T033 [P] [US2] Create SearchService for full-text search in src/services/search_service.py
- [X] T034 [US2] Update TaskService to support filtering by priority, tags, due dates in src/services/task_service.py
- [X] T035 [US2] Update TaskService to support sorting by various fields in src/services/task_service.py
- [X] T036 [US2] Implement GET /tasks/search endpoint with full-text search in src/api/task_router.py
- [X] T037 [US2] Enhance GET /tasks endpoint with filtering and sorting parameters in src/api/task_router.py
- [X] T038 [US2] Add PostgreSQL full-text search indexes in src/database/schema.sql
- [X] T039 [US2] Add database indexes for filtering performance in src/database/schema.sql
- [X] T040 [US2] Implement pagination for search results in src/services/search_service.py
- [X] T041 [US2] Add search validation and sanitization in src/services/search_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create Recurring Tasks (Priority: P3)

**Goal**: Enable users to create recurring tasks with various patterns

**Independent Test**: Can be fully tested by creating recurring tasks with different patterns (daily, weekly, monthly) and verifying that new instances are created according to the specified pattern.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚀️

- [X] T042 [P] [US3] Contract test for POST /recurring-patterns endpoint in tests/contract/test_recurring_patterns.py
- [X] T043 [P] [US3] Integration test for recurring task generation in tests/integration/test_recurring_tasks.py
- [X] T044 [P] [US3] Unit test for RecurringTaskPattern validation in tests/unit/test_recurring_pattern.py

### Implementation for User Story 3

- [X] T045 [P] [US3] Create RecurringTaskService for managing recurring patterns in src/services/recurring_task_service.py
- [X] T046 [US3] Implement POST /recurring-patterns endpoint in src/api/recurring_router.py
- [X] T047 [US3] Implement GET /recurring-patterns endpoint in src/api/recurring_router.py
- [X] T048 [US3] Create recurring task scheduler using Dapr pub/sub in src/services/recurring_task_service.py
- [X] T049 [US3] Implement logic to auto-create next task instance on completion in src/services/recurring_task_service.py
- [X] T050 [US3] Create event handler for recurring task instance creation in src/events/handlers.py
- [X] T051 [US3] Add validation for recurrence patterns in src/models/recurring_task.py
- [X] T052 [US3] Implement recurrence pattern validation in src/services/recurring_task_service.py
- [X] T053 [US3] Add database indexes for recurring task performance in src/database/schema.sql

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Set Due Dates & Receive Reminders (Priority: P4)

**Goal**: Enable users to set due dates for tasks and receive timely reminders

**Independent Test**: Can be fully tested by creating tasks with due dates and reminder settings, then verifying that reminders are delivered at the appropriate time.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T054 [P] [US4] Contract test for reminder endpoints in tests/contract/test_reminders.py
- [X] T055 [P] [US4] Integration test for reminder scheduling in tests/integration/test_reminders.py
- [X] T056 [P] [US4] Unit test for Reminder model validation in tests/unit/test_reminder.py

### Implementation for User Story 4

- [X] T057 [P] [US4] Create ReminderService for managing reminders in src/services/reminder_service.py
- [X] T058 [US4] Update Task model to support due_date and reminder_offset in src/models/task.py
- [X] T059 [US4] Create Reminder model with status tracking in src/models/reminder.py
- [X] T060 [US4] Implement reminder scheduling using Dapr pub/sub in src/services/reminder_service.py
- [X] T061 [US4] Implement GET /reminders/upcoming endpoint in src/api/task_router.py
- [X] T062 [US4] Implement POST /reminders/{id}/snooze endpoint in src/api/task_router.py
- [X] T063 [US4] Implement POST /reminders/{id}/dismiss endpoint in src/api/task_router.py
- [X] T064 [US4] Create event handler for reminder delivery in src/events/handlers.py
- [X] T065 [US4] Add validation for due dates and reminder offsets in src/models/task.py
- [X] T066 [US4] Add database indexes for reminder scheduling performance in src/database/schema.sql
- [X] T067 [US4] Implement timezone handling for due dates and reminders in src/utils/timezone.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Natural Language Processing for New Features (Priority: P5)

**Goal**: Enable users to use natural language to set priorities, tags, due dates, and recurring patterns

**Independent Test**: Can be fully tested by sending various natural language commands to the chatbot and verifying that the appropriate task properties are set correctly.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T068 [P] [US5] Unit test for intent parser with new features in tests/unit/test_intent_parser.py
- [X] T069 [P] [US5] Integration test for natural language task creation in tests/integration/test_nlp.py
- [X] T070 [P] [US5] Contract test for chat API with NLP commands in tests/contract/test_chat_nlp.py

### Implementation for User Story 5

- [X] T071 [P] [US5] Create IntentParser for recognizing priority/tag/due date commands in src/nlp/intent_parser.py
- [X] T072 [US5] Update existing chat service to use IntentParser for new features in src/services/chat_service.py
- [X] T073 [US5] Implement date/time parsing for natural language in src/nlp/intent_parser.py
- [X] T074 [US5] Implement recurring pattern parsing from natural language in src/nlp/intent_parser.py
- [X] T075 [US5] Add validation for parsed natural language commands in src/nlp/intent_parser.py
- [X] T076 [US5] Update chat router to handle NLP-enhanced task creation in src/api/chat_router.py
- [X] T077 [US5] Create utility functions for converting NLP to API calls in src/nlp/utils.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T078 [P] Documentation updates in docs/ including new API endpoints
- [X] T079 Code cleanup and refactoring
- [X] T080 Performance optimization across all stories with event processing efficiency
- [X] T081 [P] Additional unit tests (if requested) in tests/unit/
- [X] T082 Security hardening with Dapr security best practices
- [X] T083 Run quickstart.md validation with full event-driven flow
- [X] T084 [P] Helm chart updates for multi-service deployment
- [X] T085 Update existing chat interface to support new features
- [X] T086 Add comprehensive error handling for all new features
- [X] T087 Add logging for all new features with distributed tracing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs priority/tags data)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Depends on US1-US4 (needs all features to parse)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before Dapr integration
- Dapr integration before endpoints
- Event publishers/consumers as needed
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /tasks with priority and tags in tests/contract/test_task_creation.py"
Task: "Unit test for Task model validation with priority and tags in tests/unit/test_task_model.py"

# Launch all models for User Story 1 together:
Task: "Update Task model with priority enum and default in src/models/task.py"
Task: "Create Tag model with validation rules in src/models/tag.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Ensure all infrastructure interactions go through Dapr building blocks
- All secrets must be handled via Dapr secrets management
- Event schemas must be validated with Pydantic models