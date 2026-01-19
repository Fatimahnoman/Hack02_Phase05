---
description: "Task list for stateless chat API foundation implementation"
---

# Tasks: Stateless Chat API Foundation for AI Todo Application

**Input**: Design documents from `/specs/001-stateless-chat-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included based on feature requirements and success criteria.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure per implementation plan
- [X] T002 Initialize Python 3.11 project with FastAPI, SQLModel, and Neon PostgreSQL dependencies
- [X] T003 [P] Configure linting (flake8, black) and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework with SQLModel
- [X] T005 [P] Configure database connection pool for Neon Serverless PostgreSQL
- [X] T006 [P] Setup API routing and middleware structure in FastAPI
- [X] T007 Create base models/entities that all stories depend on
- [X] T008 Configure error handling and logging infrastructure
- [X] T009 Setup environment configuration management for database URL
- [X] T010 Create database session management utility functions

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Chat Messages (Priority: P1) 🎯 MVP

**Goal**: Enable users to send messages to the chat API and receive responses with conversation_id and assistant message, creating new conversations when no conversation_id is provided.

**Independent Test**: Can be fully tested by sending a message via POST /api/{user_id}/chat and verifying that a response is returned with a conversation_id and assistant message.

### Tests for User Story 1 (INCLUDED - based on success criteria) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api.py
- [X] T012 [P] [US1] Integration test for new conversation creation in backend/tests/integration/api/test_new_conversation.py

### Implementation for User Story 1

- [X] T013 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [X] T014 [P] [US1] Create Message model in backend/src/models/message.py
- [X] T015 [US1] Implement ChatService in backend/src/services/chat_service.py (depends on T013, T014)
- [X] T016 [US1] Implement ConversationService in backend/src/services/conversation_service.py (depends on T013, T014)
- [X] T017 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat_router.py
- [X] T018 [US1] Add request/response validation for chat endpoint
- [X] T019 [US1] Add logging for chat operations
- [X] T020 [US1] Implement minimal placeholder assistant response logic
- [X] T021 [US1] Persist user messages in database when receiving them
- [X] T022 [US1] Persist assistant responses in database after generating them
- [X] T023 [US1] Create new conversation when no conversation_id provided

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Continue Existing Conversations (Priority: P2)

**Goal**: Allow users to continue an existing conversation by providing a conversation_id to maintain context across multiple interactions.

**Independent Test**: Can be tested by making multiple requests with the same conversation_id and verifying that the conversation history is maintained.

### Tests for User Story 2 (INCLUDED - based on success criteria) ⚠️

- [X] T024 [P] [US2] Contract test for continuing existing conversation in backend/tests/contract/test_chat_api.py
- [X] T025 [P] [US2] Integration test for conversation continuity in backend/tests/integration/api/test_conversation_continuity.py

### Implementation for User Story 2

- [X] T026 [P] [US2] Enhance Message model to support conversation history retrieval
- [X] T027 [US2] Extend ConversationService to retrieve existing conversations
- [X] T028 [US2] Update ChatService to fetch conversation history from DB on each request
- [X] T029 [US2] Modify POST /api/{user_id}/chat endpoint to reuse existing conversations when conversation_id provided
- [X] T030 [US2] Add validation for existing conversation_id
- [X] T031 [US2] Handle case where invalid conversation_id is provided (return 404)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Message Persistence (Priority: P3)

**Goal**: Ensure all messages (user and assistant) are persisted in the database and survive server restarts, meeting the stateless architecture requirement.

**Independent Test**: Can be tested by restarting the server after sending messages and verifying that conversation history is preserved.

### Tests for User Story 3 (INCLUDED - based on success criteria) ⚠️

- [X] T032 [P] [US3] Integration test for server restart conversation continuity in backend/tests/integration/api/test_server_restart.py
- [X] T033 [P] [US3] Unit test for database persistence in backend/tests/unit/models/test_message_persistence.py

### Implementation for User Story 3

- [X] T034 [P] [US3] Optimize database queries for conversation history retrieval
- [X] T035 [US3] Implement proper indexing based on data model requirements
- [X] T036 [US3] Add database transaction management for message persistence
- [X] T037 [US3] Validate stateless operation (no server-side session storage)
- [X] T038 [US3] Add database connection resilience handling
- [X] T039 [US3] Implement conversation and message validation according to data model

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T040 [P] Documentation updates including API documentation in backend/docs/
- [X] T041 Code cleanup and refactoring
- [X] T042 Performance optimization across all stories (focus on DB queries)
- [X] T043 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T044 Security hardening (input validation, SQL injection prevention)
- [X] T045 Run quickstart.md validation to ensure all functionality works as described
- [X] T046 Add comprehensive error handling for edge cases (malformed JSON, large payloads, database unavailability)
- [X] T047 Update main application entry point with all API routes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 models and services
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1/US2 for persistence validation

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
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
# Launch all tests for User Story 1 together:
Task: "Contract test for POST /api/{user_id}/chat endpoint in backend/tests/contract/test_chat_api.py"
Task: "Integration test for new conversation creation in backend/tests/integration/api/test_new_conversation.py"

# Launch all models for User Story 1 together:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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