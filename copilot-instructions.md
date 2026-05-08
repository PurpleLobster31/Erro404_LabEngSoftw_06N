# Copilot Instructions for this Repository

Purpose
-------
This file tells GitHub Copilot (the coding assistant) what to expect in this repository, what is implemented today, and what remains out-of-scope. Use this file as a single authoritative summary when making changes, implementing missing features, or writing tests.

Quick overview
--------------
- Backend: Python FastAPI app under [backend/app/main.py](backend/app/main.py#L1) with routers in [backend/app/routers/](backend/app/routers/). Database models and migration support exist under `backend/database` and top-level `alembic/`.
- Frontend: Angular application in [frontend/src/](frontend/src/) with pages under [frontend/src/app/pages/](frontend/src/app/pages/).
- Docs: Requirements, use-cases, and architecture are in the [docs/](docs/) folder (examples: [docs/UC001.md](docs/UC001.md#L1), [docs/UC004.md](docs/UC004.md#L1)).
- Tests: Basic tests are present at [tests/test_main.py](tests/test_main.py#L1).

Scope (what this project currently contains)
-------------------------------------------
- REST endpoints and router structure for Atendimento(s), Paciente(s) and Unidade(s) appear implemented in the backend routers. Follow the existing router patterns when adding endpoints.
- Alembic is configured for database migrations; migration scripts are in `alembic/versions/`.
- An Angular frontend skeleton with pages for attendance, units and profile is present; it connects to an API-like backend structure (but may not be fully integrated or complete).

Known gaps and assumptions
--------------------------
- Not every requirement in the documentation is necessarily implemented — several Use Cases (UCs) in `docs/` may be design artifacts or partially implemented. Treat each UC in `docs/` as the truth for desired behavior unless a corresponding router/schema and tests already prove otherwise.
- Do not assume business rules not stated in `docs/`. If a UC is ambiguous, add a short issue or a TODO in code and ask for clarification.
- Authentication/authorization: there is no explicit authentication layer visible in the top-level listing. If UCs require auth, implement it behind clear feature flags and tests.
- Frontend-backend integration: the frontend is a standalone Angular app. Some API endpoints the frontend expects may be missing or have different shapes; verify each endpoint used by the UI before implementing changes.

Developer guidance for Copilot
-----------------------------
- When implementing new endpoints, follow existing patterns in [backend/app/routers/](backend/app/routers/) and use Pydantic schemas placed under [backend/app/schemas/](backend/app/schemas/).
- Keep database schema changes consistent with Alembic: add a migration under `alembic/versions/` and update `backend/database/models.py` accordingly.
- Add tests for every non-trivial behavior: use `tests/` and follow the style in `tests/test_main.py`.
- Write small, focused commits and include a test that demonstrates the new behavior or fixes a failing test.
- If you change an API contract expected by the frontend, update the frontend types under [frontend/src/app/](frontend/src/app/) and, if applicable, add a migration or compatibility layer in the backend.

How to run and test locally
---------------------------
- Recommended: start with docker-compose if present to get DB and services up quickly:

```bash
docker-compose up --build
```

- Or run backend directly (typical for FastAPI projects):

```bash
# from repo root
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

- Run tests with pytest:

```bash
pytest -q
```

Where to look first when asked to implement a UC or requirement
-------------------------------------------------------------
1. Open the UC file in `docs/` (for example, [docs/UC001.md](docs/UC001.md#L1)) and confirm the expected behavior.
2. Search for existing backend routers and schemas that might already implement parts of the UC ([backend/app/routers/](backend/app/routers/), [backend/app/schemas/](backend/app/schemas/)).
3. If models need changes, update `backend/database/models.py` and create an Alembic migration in `alembic/versions/`.
4. Add or update tests under `tests/` that assert the UC behavior before implementing the full feature (TDD first when feasible).
5. Implement the feature, run tests, and adjust the frontend types/pages if the API surface changes.

Style and conventions
---------------------
- Follow existing code style in the project: mirror function and variable naming used in `backend/` and `frontend/`.
- Keep API endpoints RESTful and versioned if adding breaking changes (e.g., `/api/v1/...`).
- Keep migrations small and focused. Use descriptive names for migration files.

Suggested next tasks (high value, small scope)
---------------------------------------------
- Run the test suite and fix any failing tests to get a green baseline.
- Select a single UC from `docs/` that is not covered by tests and implement it end-to-end (backend API + tests + update frontend types). Document the steps in the PR.
- Add CI (GitHub Actions) if missing to run `pytest` and linting on each PR.

Notes for reviewers
-------------------
- Check that new endpoints include pydantic schemas and tests.
- Verify Alembic migration files are present and consistent with models for DB-changing PRs.

If anything in `docs/` contradicts actual code, prefer adding a clarifying test and a short note in the code base (`# TODO: clarify UC004 input behavior`) before making large assumptions.

Contact
-------
If you want me to implement a specific UC, say which `docs/UCxxx.md` to implement and whether to do backend-only or end-to-end (backend + frontend + tests). I will follow this file as the implementation guide.

---
Generated by Copilot assistant to guide contributors and automation in this workspace.
