# Sentinel AI Backend

Current implementation milestone: **Phase 2M — persistence foundation**.

The backend is a FastAPI modular monolith. The AI worker remains a separate process/component.

## Implemented

### Phase 2L — AI integration

- FastAPI application factory and health endpoint;
- strict violence-worker success/failure validation;
- frozen model/version contract validation;
- rolling state keyed by `(camera_id, model_version_id)`;
- frozen `score >= 0.906` + `3-of-5` criterion;
- transport-neutral JSONL replay adapter.

### Phase 2M — persistence foundation

- SQLAlchemy 2.x model layer;
- Alembic migration foundation;
- `cameras`, `models`, `model_versions`, `violence_event_policies`, `events`, and `violence_event_context`;
- idempotent frozen violence model/version/global-policy seed;
- database-backed `ModelRegistry` adapter;
- explicit violence-event persistence service.

## Important event-lifecycle boundary

Phase 2M does **not** automatically persist every `candidate_condition=True` observation. The Fighting fixture has multiple consecutive qualified observations, and duplicate/cooldown/retrigger behavior remains unresolved.

```text
validated worker observation
→ frozen rolling criterion
→ candidate condition
→ event-domain lifecycle decision (future slice)
→ explicit ViolenceEventPersistenceService call
```

## Database configuration

Environment variable: `SENTINEL_DATABASE_URL`.

Local development default:

```text
sqlite+pysqlite:///./backend/runtime/sentinel.db
```

PostgreSQL example:

```text
postgresql+psycopg://user:password@localhost:5432/sentinel
```

Do not commit database credentials.

## Update environment and run tests

```powershell
.\backend\.venv\Scripts\Activate.ps1
python -m pip install -r .\backend\requirements-dev.txt
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m unittest discover -s .\backend\tests -p "test_*.py" -v
```

## Initialize local development database

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python .\backend\scripts\init_database.py
```

This runs Alembic to `head` and seeds the immutable selected violence model/version and frozen global `0.906 / 3-of-5` policy. `cooldown_ms` remains `NULL`.

## Replay worker outputs

```powershell
python .\backend\scripts\replay_violence_worker_jsonl.py --input ".\ai_worker\runtime_work\demo-fighting-results.jsonl"
python .\backend\scripts\replay_violence_worker_jsonl.py --input ".\ai_worker\runtime_work\demo-normal-results.jsonl"
```

## Deliberately unresolved

- backend ↔ AI-worker HTTP/queue/IPC transport;
- authentication mechanism;
- event duplicate/cooldown/retrigger semantics;
- automatic event creation from rolling criterion;
- evidence persistence;
- WebSocket publication;
- acknowledgement;
- detector/tracker integration.
