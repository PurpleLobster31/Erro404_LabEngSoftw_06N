# Copilot Cloud Agent Onboarding Instructions

## Repository overview
- Monorepo with:
  - **Backend**: FastAPI + SQLAlchemy async + Alembic + PostGIS (`backend/`, `alembic/`).
  - **Frontend**: Angular 21 standalone app (`frontend/`).
- Main backend entrypoint: `backend/app/main.py`.
- Main backend business route: `backend/app/routers/unidades.py`.
- Backend tests: `backend/tests/test_main.py` (pytest with DB dependency override).

## Where to work
- Backend API logic: `backend/app/routers/`
- Backend schemas: `backend/app/schemas/`
- DB setup/models: `backend/database/`, `alembic/`
- Frontend app/pages/services: `frontend/src/app/`
- CI definition: `.github/workflows/ci.yml`

## Recommended workflow for agents
1. Read `.github/workflows/ci.yml`, `README.md`, `CONFIG-DE-AMBIENTE.md`, and `frontend/angular.json` before editing.
2. Keep changes scoped to the touched layer (backend vs frontend).
3. Prefer minimal, surgical diffs.
4. Run existing project commands (do not invent new tooling).

## Setup and validation commands
Run from repo root unless noted.

### Backend
- Install dependencies (working command):  
  `python -m pip install -r requirements-dev.txt`
- Run tests:  
  `python -m pytest`
- CI-style tests with coverage (requires same dependencies):  
  `python -m pytest --cov=backend.app --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml --cov-fail-under=70`

### Database / migrations
- Start DB:  
  `docker-compose up -d`
- Wait ~15s for PostGIS readiness.
- Run migrations:  
  `python -m alembic upgrade head`

### Frontend
- Install dependencies (from `frontend/`):  
  `npm ci`
- Build (internet-restricted-safe command):  
  `npm run build -- --configuration development`
- Default production build command exists but may require internet for Google Fonts:
  `npm run build`

## Known errors encountered and workarounds
These were observed while onboarding this repository.

1. **`python -m pytest` failed with `No module named pytest`**
   - Cause: Python dependencies not installed.
   - Workaround: `python -m pip install -r requirements-dev.txt`.

2. **Installing both `requirements.txt` and `requirements-dev.txt` together failed (`ResolutionImpossible`)**
   - Cause: conflicting pinned versions (e.g., `fastapi==0.115.12` vs `fastapi==0.135.3`).
   - Workaround used: install only `requirements-dev.txt` for local agent work.

3. **`npm run build` failed with `ng: not found`**
   - Cause: Node dependencies not installed.
   - Workaround: run `npm ci` in `frontend/`.

4. **`npm run build` failed in sandbox with Google Fonts fetch error (`getaddrinfo ENOTFOUND fonts.googleapis.com`)**
   - Cause: restricted/no external DNS/network to Google Fonts during CSS font inlining.
   - Workaround used: `npm run build -- --configuration development` (build succeeds without that fetch path).

5. **`python -m alembic upgrade head` failed with connection refused on `localhost:5432`**
   - Cause: Postgres/PostGIS service not running.
   - Workaround: `docker-compose up -d`, wait for readiness, then rerun migration.

6. **Frontend test script currently fails (`npm test`)**
   - Observed errors include unknown watch argument and missing target/project in Angular CLI.
   - Cause: no `test` architect target defined in `frontend/angular.json`.
   - Workaround: treat frontend automated tests as not configured yet; validate via build (`ng build`) and manual route checks.

## Codebase-specific implementation notes
- Backend DB sessions are injected via `get_db` (`backend/database/database.py`); follow this pattern in new routes.
- Geospatial queries use PostGIS geography casts for distance calculations in `backend/app/routers/unidades.py`; preserve this approach for meter-based radius logic.
- `frontend/angular.json` has `skipTests: true` across schematics; new frontend code commonly ships without generated spec files unless explicitly added.
- Frontend project uses standalone Angular components; keep that style consistent.

## Change safety checklist (for agents)
- If editing backend:
  - Run `python -m pytest`.
  - If migration/model changes were made, ensure DB migration path still works.
- If editing frontend:
  - Run `npm ci` (if needed) and `npm run build -- --configuration development`.
- If editing CI/dependencies:
  - Re-check both backend and frontend validation paths and call out any new constraints.
