---
description: "Task list for Phase II Evolution of Todo project implementation"
---

# Tasks: Evolution of Todo - Phase II

**Input**: Design documents from `/specs/002-evolution-of-todo-phase-ii/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow the plan structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 [P] Initialize backend Python project with FastAPI, SQLModel, Better Auth dependencies
- [x] T003 [P] Initialize frontend Next.js project with TypeScript
- [x] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup Neon PostgreSQL connection and database configuration in backend/src/database/database.py
- [x] T006 [P] Implement authentication framework with Better Auth in backend/src/services/auth_service.py
- [x] T007 [P] Setup API routing and middleware structure in backend/src/main.py
- [x] T008 Create User model in backend/src/models/user.py
- [x] T009 Create Todo model in backend/src/models/todo.py
- [x] T010 Configure error handling and logging infrastructure in backend/src/main.py
- [x] T011 Setup environment configuration management in both backend and frontend

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to sign up and existing users to sign in using Better Auth

**Independent Test**: A new user can register with valid email and password, and an existing user can sign in with correct credentials

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement user registration endpoint in backend/src/api/auth_router.py
- [x] T013 [P] [US1] Implement user sign-in endpoint in backend/src/api/auth_router.py
- [x] T014 [US1] Implement auth middleware for protected routes in backend/src/services/auth_service.py
- [x] T015 [US1] Create signup page in frontend/src/pages/signup.tsx
- [x] T016 [US1] Create signin page in frontend/src/pages/signin.tsx
- [x] T017 [US1] Implement auth state handling hook in frontend/src/hooks/useAuth.ts
- [x] T018 [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx
- [x] T019 [US1] Create SigninForm component in frontend/src/components/auth/SigninForm.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Todo Management Core Features (Priority: P1)

**Goal**: Enable authenticated users to create, view, update, and delete their todos

**Independent Test**: An authenticated user can create, view, update, and delete todos, with all data properly persisted

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement create todo endpoint in backend/src/api/todo_router.py
- [x] T021 [P] [US2] Implement get all todos endpoint in backend/src/api/todo_router.py
- [x] T022 [P] [US2] Implement update todo endpoint in backend/src/api/todo_router.py
- [x] T023 [P] [US2] Implement delete todo endpoint in backend/src/api/todo_router.py
- [x] T024 [US2] Implement mark todo complete/incomplete endpoint in backend/src/api/todo_router.py
- [x] T025 [US2] Implement user-scoped data access enforcement in backend/src/services/todo_service.py
- [x] T026 [US2] Create TodoForm component in frontend/src/components/todos/TodoForm.tsx
- [x] T027 [US2] Create TodoList component in frontend/src/components/todos/TodoList.tsx
- [x] T028 [US2] Create TodoItem component in frontend/src/components/todos/TodoItem.tsx
- [x] T029 [US2] Create dashboard page in frontend/src/pages/dashboard.tsx
- [x] T030 [US2] Implement API service for todo operations in frontend/src/services/api.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Personal Todo Data Isolation (Priority: P2)

**Goal**: Ensure authenticated users can only access and modify their own todos

**Independent Test**: One user's todos are not accessible to another user, with proper authentication and authorization checks

### Implementation for User Story 3

- [x] T031 [US3] Enhance auth middleware to validate user ownership in backend/src/services/auth_service.py
- [x] T032 [US3] Implement user ID validation in all todo operations in backend/src/services/todo_service.py
- [x] T033 [US3] Add 403 Forbidden responses for unauthorized access attempts in backend/src/api/todo_router.py
- [x] T034 [US3] Update frontend API service to handle 403 errors appropriately in frontend/src/services/api.ts
- [x] T035 [US3] Add error messaging for unauthorized access attempts in frontend components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Responsive Web Interface (Priority: P2)

**Goal**: Provide a responsive UI that works well on both desktop and mobile devices

**Independent Test**: The interface adapts appropriately to different screen sizes with proper touch and mouse interaction optimization

### Implementation for User Story 4

- [x] T036 [US4] Create responsive layout component in frontend/src/components/layout/Layout.tsx
- [x] T037 [US4] Create responsive header component in frontend/src/components/layout/Header.tsx
- [x] T038 [US4] Implement CSS Grid/Flexbox for responsive todo list in frontend/src/components/todos/TodoList.tsx
- [x] T039 [US4] Add media queries for mobile and desktop layouts in frontend/src/components/
- [x] T040 [US4] Test UI on various device sizes and adjust as needed

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T041 [P] Add comprehensive error handling in backend/src/main.py
- [x] T042 [P] Add validation to all API endpoints in backend/src/api/
- [x] T043 [P] Add loading states for API calls in frontend/src/services/api.ts
- [x] T044 [P] Add error and empty states in frontend components
- [x] T045 [P] Add responsive design testing for all pages
- [x] T046 [P] Add frontend type definitions in frontend/src/types/index.ts
- [x] T047 [P] Add database migration scripts in backend/alembic/versions/
- [x] T048 [P] Add environment configuration for local development
- [x] T049 [P] Add API documentation with FastAPI auto-generated docs
- [x] T050 [P] Run quickstart validation across all implemented features

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
- **User Story 2 (P2)**: Depends on US1 (auth) being implemented first
- **User Story 3 (P3)**: Depends on US1 and US2 being implemented first
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all API endpoints for User Story 2 together:
Task: "Implement create todo endpoint in backend/src/api/todo_router.py"
Task: "Implement get all todos endpoint in backend/src/api/todo_router.py"
Task: "Implement update todo endpoint in backend/src/api/todo_router.py"
Task: "Implement delete todo endpoint in backend/src/api/todo_router.py"

# Launch all frontend components for User Story 2 together:
Task: "Create TodoForm component in frontend/src/components/todos/TodoForm.tsx"
Task: "Create TodoList component in frontend/src/components/todos/TodoList.tsx"
Task: "Create TodoItem component in frontend/src/components/todos/TodoItem.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Core Todo functionality)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 together
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3 and 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence