# Tasks: Resolución inicial del cubo de Rubik

**Input**: Design documents from `/specs/001-rubik-solver-mvp/`

**Prerequisites**: [plan.md](./plan.md) (required), [spec.md](./spec.md) (required for user stories), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/http-api.yaml](./contracts/http-api.yaml), [quickstart.md](./quickstart.md)

**Tests**: No se generan tareas de tests por adelantado porque la especificación no exige TDD explícito; las validaciones se ejecutarán en la fase de pulido y en la implementación final de cada historia.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Los paths siguen la estructura definida en [plan.md](./plan.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicializar la base técnica full-stack y el armazón del repositorio

- [X] T001 Create the planned folder structure for `backend/src/`, `backend/tests/`, `frontend/src/`, `frontend/tests/`, and feature subfolders described in `specs/001-rubik-solver-mvp/plan.md`
- [X] T002 Initialize the frontend workspace with Vue 3 + TypeScript + Vite + Vuetify + Pinia + Vue Router in `frontend/package.json`, `frontend/tsconfig.json`, and `frontend/vite.config.ts`
- [X] T003 [P] Initialize the backend workspace with FastAPI, Pydantic, Uvicorn, MongoDB driver, and pytest dependencies in `backend/requirements.txt` and `backend/requirements-dev.txt`
- [X] T004 [P] Create shared local environment templates for frontend and backend in `frontend/.env.example` and `backend/.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Construir la infraestructura común que bloquea todas las historias

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create the FastAPI application bootstrap, dependency wiring, and route registration in `backend/src/api/main.py`, `backend/src/api/dependencies.py`, and `backend/src/api/routes/__init__.py`
- [X] T006 [P] Create the frontend application shell, router bootstrap, and Vuetify provider in `frontend/src/main.ts`, `frontend/src/app/router/index.ts`, `frontend/src/app/providers/AppProviders.vue`, and `frontend/src/app/vuetify/index.ts`
- [X] T007 [P] Create shared backend domain/value-object foundations for `User`, `Game`, `Cube`, and `CubeStateStep` in `backend/src/domain/user/entities.py`, `backend/src/domain/game/entities.py`, and `backend/src/domain/cube/entities.py`
- [X] T008 [P] Create MongoDB configuration, client factory, and repository base wiring in `backend/src/infrastructure/persistence/config.py`, `backend/src/infrastructure/persistence/mongo_client.py`, and `backend/src/infrastructure/persistence/base.py`
- [X] T009 [P] Create the frontend HTTP client, DTO mappers, and application port contracts in `frontend/src/infrastructure/http/apiClient.ts`, `frontend/src/infrastructure/mappers/`, and `frontend/src/application/ports/`
- [X] T010 Implement shared error/result handling and Pinia store registration in `frontend/src/stores/index.ts`, `frontend/src/application/use_cases/result.ts`, and `backend/src/api/schemas/error.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in priority order

---

## Phase 3: User Story 1 - Registrar o reutilizar jugador (Priority: P1) 🎯 MVP

**Goal**: Permitir crear o reutilizar la sesión de un jugador por `username` y actualizar su `fullname` sin duplicados

**Independent Test**: Enviar un `username` nuevo con `fullname` válido crea el jugador; reenviar el mismo `username` con otro `fullname` reutiliza el mismo registro y actualiza el nombre visible

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement the `User` repository and normalized username persistence with the constraints "`username` debe ser único y normalizado", "`fullname` no puede estar vacío", and "`score` no puede ser negativo" in `backend/src/infrastructure/persistence/user_repository.py`
- [X] T012 [P] [US1] Implement the user upsert request/response schemas matching `PUT /users/{username}` in `backend/src/api/schemas/user.py`
- [X] T013 [US1] Implement the idempotent register-or-update player use case in `backend/src/application/use_cases/register_player.py`
- [X] T014 [US1] Expose the `PUT /users/{username}` endpoint and error mapping in `backend/src/api/routes/users.py`
- [X] T015 [P] [US1] Create the player-session feature UI contract in `frontend/src/features/player-session/components/RegistrationForm.vue` and `frontend/src/features/player-session/composables/useRegistrationForm.ts`
- [X] T016 [US1] Implement the frontend player store and register-player application action in `frontend/src/stores/playerStore.ts` and `frontend/src/application/use_cases/registerPlayer.ts`
- [X] T017 [US1] Compose the registration flow into the main solver view and show active-session feedback in `frontend/src/presentation/pages/SolverPage.vue`

**Checkpoint**: User Story 1 should let the user create or reuse a session without duplicates

---

## Phase 4: User Story 2 - Definir el estado inicial del cubo (Priority: P1)

**Goal**: Permitir capturar manualmente el estado inicial del cubo y validarlo en tiempo real antes de resolver

**Independent Test**: Pintar todas las casillas con una distribución válida habilita el inicio; dejar huecos, romper el conteo o introducir un estado irresoluble lo bloquea con errores específicos

### Implementation for User Story 2

- [X] T018 [P] [US2] Implement the frontend cube domain model and helpers for a cube with faces `u`, `d`, `f`, `b`, `l`, `r` where "Cada cara debe contener exactamente 9 stickers" and "Deben existir exactamente 9 stickers por color permitido" in `frontend/src/domain/cube/cubeState.ts` and `frontend/src/domain/cube/cubeColors.ts`
- [X] T019 [P] [US2] Implement backend cube validation services enforcing "Deben existir las 6 caras", "Cada cara debe contener exactamente 9 stickers", "Deben existir exactamente 9 stickers por color permitido", and "La orientación de centros y la disposición de piezas deben describir un cubo físicamente resoluble" in `backend/src/domain/cube/validation.py`
- [X] T020 [P] [US2] Create the cube editor feature components for palette, net, and validation summary in `frontend/src/features/cube-editor/components/ColorPalette.vue`, `frontend/src/features/cube-editor/components/CubeNet.vue`, and `frontend/src/features/cube-editor/components/CubeValidationSummary.vue`
- [X] T021 [US2] Implement the cube editor store with selected color, sticker updates, derived validation state, and `canResolve` gating in `frontend/src/stores/cubeEditorStore.ts`
- [X] T022 [US2] Compose the cube editor workflow and single-screen layout in `frontend/src/features/cube-editor/components/CubeEditor.vue` and `frontend/src/presentation/pages/SolverPage.vue`
- [X] T023 [US2] Add backend request schema validation for the cube payload used by game creation in `backend/src/api/schemas/cube.py` and `backend/src/api/schemas/game.py`

**Checkpoint**: User Story 2 should allow valid cube entry and block invalid starts with actionable feedback

---

## Phase 5: User Story 3 - Resolver y reproducir la solución paso a paso (Priority: P2)

**Goal**: Crear la partida, resolver el cubo, persistir cada movimiento y permitir la reproducción paso a paso con resumen final

**Independent Test**: Con sesión activa y cubo válido, iniciar la resolución crea la partida, devuelve pasos ordenados, permite navegar reproducir/pausar y muestra el total de movimientos; si el cubo ya está resuelto, el total es `0`

### Implementation for User Story 3

- [X] T024 [P] [US3] Implement the `Game`, `Cube`, and `CubeStateStep` repositories with the constraints "`userId` debe apuntar a un `User` existente", "`idCube` debe apuntar a un `Cube` existente", "`score` debe ser `0` o mayor", "`currentStep` debe mantenerse entre `0` y `score`", and "`movement` debe comenzar en 1 y avanzar de uno en uno" in `backend/src/infrastructure/persistence/game_repository.py`, `backend/src/infrastructure/persistence/cube_repository.py`, and `backend/src/infrastructure/persistence/solution_step_repository.py`
- [X] T025 [P] [US3] Implement the solver port and adapter contracts for standard move notation (`R`, `U'`, `F2`, etc.) in `backend/src/application/ports/cube_solver.py` and `backend/src/infrastructure/solver/rubik_solver_adapter.py`
- [X] T026 [US3] Implement the create-game-and-solve use case, including zero-move solved cubes and explicit irrecoverable solver errors, in `backend/src/application/use_cases/create_game.py`
- [X] T027 [US3] Expose `POST /games`, `GET /games/{gameId}`, `GET /games/{gameId}/steps`, and `GET /games/{gameId}/steps/{movement}` in `backend/src/api/routes/games.py`
- [X] T028 [P] [US3] Implement frontend solution/player domain types and DTO mappers in `frontend/src/domain/solution/solutionStep.ts` and `frontend/src/infrastructure/mappers/gameMappers.ts`
- [X] T029 [P] [US3] Implement the game and solution stores, including ordered steps, bounded navigation, autoplay state, and total-move summary in `frontend/src/stores/gameStore.ts` and `frontend/src/stores/solutionStore.ts`
- [X] T030 [P] [US3] Create the solution player UI components for playback controls, highlighted current step, and cube-state preview in `frontend/src/features/solution-player/components/SolutionPlayer.vue` and `frontend/src/features/solution-player/components/CubeStatePreview.vue`
- [X] T031 [US3] Integrate the resolve action, step navigation, and final movement summary into `frontend/src/presentation/pages/SolverPage.vue` and `frontend/src/application/use_cases/requestSolution.ts`

**Checkpoint**: User Story 3 should complete the end-to-end solve-and-playback flow independently

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cerrar huecos compartidos, accesibilidad y validación final

- [X] T032 [P] Add accessible labels, color-count helpers, and keyboard-friendly status messaging across `frontend/src/features/cube-editor/components/` and `frontend/src/features/solution-player/components/`
- [X] T033 [P] Add global SCSS tokens for high-contrast Rubik colors and single-screen layout refinements in `frontend/src/styles/tokens.scss` and `frontend/src/styles/main.scss`
- [X] T034 Document local run/setup instructions for the implemented structure in `frontend/README.md` and `backend/README.md`
- [X] T035 Run the end-to-end manual validation scenarios from `specs/001-rubik-solver-mvp/quickstart.md` and update any mismatches in `specs/001-rubik-solver-mvp/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational completion
  - **US1** starts first as MVP identity flow
  - **US2** starts after Foundational and can proceed in parallel with the tail of US1 if team capacity allows
  - **US3** depends on the completion of US1 and US2 because it requires both an active player flow and a validated cube flow
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - independent from US1 at implementation level, but both together enable the main solve flow
- **User Story 3 (P2)**: Depends on US1 and US2 because the solver request must include a valid user session and a valid cube state

### Within Each User Story

- Persistence/contracts before use cases where applicable
- Domain/state models before UI orchestration
- Stores/application actions before page composition
- API endpoints after schemas and use cases
- Final integration after backend and frontend support are both in place

### Parallel Opportunities

- **Setup**: T003 and T004 can run in parallel after T001/T002 planning is understood
- **Foundational**: T006, T007, T008, and T009 can run in parallel
- **US1**: T011, T012, and T015 can run in parallel; T016 waits for backend contract stability
- **US2**: T018, T019, and T020 can run in parallel; T021 depends on T018/T020; T023 depends on T019
- **US3**: T024, T025, T028, T029, and T030 can be split across backend/frontend tracks; T031 waits for T026/T027/T029/T030
- **Polish**: T032, T033, and T034 can run in parallel before T035

---

## Parallel Example: User Story 2

```bash
# Backend/frontend cube foundations in parallel:
Task: "T018 Implement the frontend cube domain model in frontend/src/domain/cube/cubeState.ts and frontend/src/domain/cube/cubeColors.ts"
Task: "T019 Implement backend cube validation services in backend/src/domain/cube/validation.py"
Task: "T020 Create the cube editor feature components in frontend/src/features/cube-editor/components/"
```

## Parallel Example: User Story 3

```bash
# Backend persistence/solver and frontend playback foundations in parallel:
Task: "T024 Implement the Game, Cube, and CubeStateStep repositories in backend/src/infrastructure/persistence/"
Task: "T025 Implement the solver port and adapter in backend/src/application/ports/cube_solver.py and backend/src/infrastructure/solver/rubik_solver_adapter.py"
Task: "T029 Implement the game and solution stores in frontend/src/stores/gameStore.ts and frontend/src/stores/solutionStore.ts"
Task: "T030 Create the solution player UI components in frontend/src/features/solution-player/components/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate player registration/reuse independently

### Incremental Delivery

1. Deliver **US1** to establish session identity
2. Deliver **US2** to enable valid cube capture and validation
3. Deliver **US3** to connect solver, persistence, and playback
4. Finish with accessibility, styling, and quickstart verification

### Suggested MVP Scope

Para una demo mínima funcional del producto, el mejor corte es **US1 + US2**: jugador registrado/reutilizado y cubo válido preparado para resolver. El primer incremento completo de valor de negocio end-to-end es **US1 + US2 + US3**.
