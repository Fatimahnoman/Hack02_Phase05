---
description: "Task list for intent mapping and behavior rules implementation"
---

# Tasks: Intent Mapping & Behavior Rules

**Input**: Design documents from `/specs/1-intent-mapping/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included based on the feature specification requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/agents/, src/services/, src/utils/, src/mcp/
- [X] T002 Initialize Python project with anthropic and python-mcp dependencies
- [X] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create intent detection base classes in src/agents/intent_detector.py
- [X] T005 [P] Create behavior rules base framework in src/services/behavior_rules.py
- [X] T006 [P] Setup logging infrastructure in src/utils/logger.py
- [X] T007 Create intent result data structures in src/models/intent_result.py
- [X] T008 Configure error handling and validation framework
- [X] T009 Setup MCP tool integration framework

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Intent Detection and Action Mapping (Priority: P1) 🎯 MVP

**Goal**: Implement core intent detection system that accurately identifies user intents and maps them to appropriate MCP tools

**Independent Test**: Send various user messages and verify that the correct MCP tool is called based on the detected intent.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Contract test for intent detection in tests/contract/test_intent_detection.py
- [X] T011 [P] [US1] Integration test for add_task intent in tests/integration/test_add_task_flow.py
- [X] T012 [P] [US1] Integration test for list_tasks intent in tests/integration/test_list_tasks_flow.py
- [X] T013 [P] [US1] Integration test for help intent in tests/integration/test_help_flow.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create IntentType enum in src/models/intent_type.py
- [X] T015 [P] [US1] Create IntentParameter model in src/models/intent_parameter.py
- [X] T016 [US1] Implement keyword-based intent detection logic in src/agents/intent_detector.py
- [X] T017 [US1] Implement action mapping service in src/services/intent_mapping.py
- [X] T018 [US1] Connect intent detector to MCP task tools in src/mcp/task_tools.py
- [X] T019 [US1] Add validation for required parameters in src/services/intent_mapping.py
- [X] T020 [US1] Add logging for intent detection operations in src/utils/logger.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Guarded Behavior and Safe Fallbacks (Priority: P2)

**Goal**: Implement guarded behavior to limit actions to approved capabilities and provide safe fallbacks for invalid input

**Independent Test**: Send unsupported intents and ambiguous inputs to verify that the bot responds appropriately without causing system changes.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T021 [P] [US2] Contract test for behavior validation in tests/contract/test_behavior_validation.py
- [X] T022 [P] [US2] Integration test for unsupported intent handling in tests/integration/test_unsupported_intent.py
- [X] T023 [P] [US2] Integration test for ambiguous input handling in tests/integration/test_ambiguous_input.py

### Implementation for User Story 2

- [X] T024 [P] [US2] Create BehaviorRule model in src/models/behavior_rule.py
- [X] T025 [P] [US2] Create ValidationError model in src/models/validation_error.py
- [X] T026 [US2] Implement guarded execution logic in src/services/behavior_rules.py
- [X] T027 [US2] Add safe fallback response mechanism in src/services/intent_mapping.py
- [X] T028 [US2] Implement unauthorized action prevention in src/services/behavior_rules.py
- [X] T029 [US2] Add error response formatting in src/services/intent_mapping.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Missing Data Handling (Priority: P3)

**Goal**: Implement system to request missing information when needed for task completion

**Independent Test**: Provide partial information for actions that require specific data and verify that the bot asks for missing details.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US3] Contract test for missing data validation in tests/contract/test_missing_data_validation.py
- [X] T031 [P] [US3] Integration test for update_task with missing ID in tests/integration/test_update_task_missing_id.py
- [X] T032 [P] [US3] Integration test for add_task with missing details in tests/integration/test_add_task_missing_details.py

### Implementation for User Story 3

- [X] T033 [P] [US3] Create MissingParameterRequest model in src/models/missing_parameter_request.py
- [X] T034 [P] [US3] Create ParameterValidator service in src/services/parameter_validator.py
- [X] T035 [US3] Implement missing data detection logic in src/services/intent_mapping.py
- [X] T036 [US3] Add clarification request mechanism in src/agents/intent_detector.py
- [X] T037 [US3] Update MCP tools to validate required parameters in src/mcp/task_tools.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Documentation updates in docs/
- [X] T039 Code cleanup and refactoring across all components
- [X] T040 [P] Performance optimization for intent detection in src/agents/intent_detector.py
- [X] T041 [P] Additional unit tests in tests/unit/
- [X] T042 Security hardening for input validation
- [X] T043 Run quickstart.md validation
- [X] T044 Update agent context with new functionality in .specify/agent/claude.md

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 components
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds upon US1/US2 components

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
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for intent detection in tests/contract/test_intent_detection.py"
Task: "Integration test for add_task intent in tests/integration/test_add_task_flow.py"

# Launch all models for User Story 1 together:
Task: "Create IntentType enum in src/models/intent_type.py"
Task: "Create IntentParameter model in src/models/intent_parameter.py"
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