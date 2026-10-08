<!-- SENTINEL_20261008_SCOPE:BEGIN -->
**Current academic release scope (project-lead decision, 2026-10-08):** The deliverable is the single looping virtual CCTV source -> **actual frozen violence inference** -> **operator-visible qualified alert**. See `docs/22-academic-violence-demo-scope.md` for included/excluded features, non-hardcoded runtime paths, and review gates. Older broader features retained below are historical planning, not required for the narrowed academic release. The frozen qualification in `docs/19-violence-model-and-runtime-qualification.md` remains unchanged. This note does not claim the end-to-end system is already operational.
<!-- SENTINEL_20261008_SCOPE:END -->

# Sentinel AI

Sentinel AI is an Advanced Web Technologies academic project built as a **FastAPI modular monolith + separate AI worker + React/Vite frontend**.

This repository deliberately separates:

- web/application domain behavior;
- database persistence and migrations;
- AI-worker inference;
- operator frontend behavior;
- external model/data artifacts.

The integrated development baseline is promoted through `staging` before `main`. See `docs/20-integration-baseline-and-branch-sync.md` for the current branch workflow and integration record.

## Current integrated API surface

The present implementation includes:

- `GET /api/v1/health` — process liveness;
- `GET /api/v1/health/readiness` — database/schema/migration readiness;
- camera create/list/detail/update/health routes, plus a local-only MJPEG route for the canonical virtual camera;
- event list/detail routes;
- development HTTP adapter for structured violence-worker results;
- local-only demo clip/source-control routes backed by the approved catalog and process-local controller.

The backend can use an external FFmpeg executable (if configured/available) to pace and loop approved local clips and expose a local-only MJPEG stream for the canonical camera. The canonical camera identity is protected by the camera API, and its `enabled` state gates replay. This does not complete general/production camera streaming. If FFmpeg is unavailable, source start returns an explicit unavailable response. Real media/browser playback has not yet been verified, and AI-worker source synchronization remains pending.

Database initialization idempotently seeds `DEMO-CAM-01` with canonical UUID `02b1cbc6-d4a3-5630-8c4e-27cdcc062d57` and `source_kind=file`; no schema migration is required. The controller issues an ephemeral source-session UUID on start, retains it through automatic loops and explicit restart, and clears it on stop. Replay code is implemented behind optional FFmpeg configuration; real-media verification and AI processing remain pending.

This does **not** mean the full MVP is complete. Authentication, durable acknowledgement, evidence, real-time/WebSocket delivery, general/production camera streaming, analytics, detector/tracker integration, deterministic intrusion/loitering/crowd rules, and final violence-event lifecycle policy remain separate implementation work unless later commits explicitly complete them.

## Backend setup

From the repository root on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\backend\requirements-dev.txt

$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python .\backend\scripts\init_database.py
python .\backend\scripts\check_database.py
python -m uvicorn app.main:app --app-dir .\backend --reload
```

The default local database is resolved from the repository location as:

```text
backend/runtime/sentinel.db
```

It is not tied to a developer's home directory. Override with `SENTINEL_DATABASE_URL` when required.

### Health semantics

```text
GET /api/v1/health
```

answers only whether the FastAPI process is alive.

```text
GET /api/v1/health/readiness
```

checks database connectivity, required integrated tables, and the expected Alembic revision. An uninitialized/outdated database returns HTTP `503` with a safe actionable response rather than being confused with liveness.

## Frontend setup

```powershell
cd .\frontend
npm ci
Copy-Item .env.example .env -ErrorAction SilentlyContinue
npm run dev
```

The local development API proxy is configurable with:

```dotenv
VITE_API_PROXY_TARGET=http://127.0.0.1:8000
```

The default preserves the current development behavior while allowing another machine/environment to change it without editing source.

## Violence runtime configuration

The heavy XD-Violence/model workspace remains external to Git.

Set its root on the machine that performs raw-video inference:

```powershell
$env:SENTINEL_VIOLENCE_ROOT = "<path-to-XD-Violence-workspace>"
```

Do not commit a developer-specific absolute path.

Optional path overrides are available for the frozen artifacts/environment:

```text
SENTINEL_TEMPORAL_CHECKPOINT
SENTINEL_TEMPORAL_TRAIN_SCRIPT
SENTINEL_EXTRACTOR_PYTHON
SENTINEL_EXTRACTOR_WORKER
SENTINEL_RUNTIME_WORK_DIR
```

Model identity and SHA-256 checks remain frozen; only machine-specific locations are configurable.

Generate the ignored local source map:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\create_local_source_map.ps1
```

or pass the workspace explicitly:

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\ai_worker\scripts\create_local_source_map.ps1 `
  -XDViolenceRoot "<path-to-XD-Violence-workspace>"
```

## Verification

Run the integrated verification script from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_integration.ps1
```

It uses a disposable SQLite database and runs:

1. migrations + seed;
2. database readiness;
3. backend tests;
4. AI-worker pure/unit tests;
5. frontend install, lint, and build.

Raw-video/model execution is intentionally not hidden in this script because it requires the separately qualified external workspace/GPU runtime.

## Branch synchronization

Inspect branch divergence without modifying branch history:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check_branch_sync.ps1
```

Do not force-push teammate branches merely to make them visually match `main`. After integration promotion, teammates should normally start new work from updated `main`, or merge `origin/main` into an existing feature branch if that branch must continue.
