# Sentinel AI Backend

The backend is a FastAPI modular monolith. Violence inference remains in the separate AI worker. This README documents the **implemented integrated backend boundary**; it does not claim completion of unresolved MVP subsystems.

## Implemented HTTP endpoints

| Method | Path | Current behavior |
|---|---|---|
| GET | `/api/v1/health` | FastAPI process liveness only |
| GET | `/api/v1/health/readiness` | DB connectivity/schema/Alembic readiness |
| POST | `/api/v1/cameras` | Create camera metadata |
| GET | `/api/v1/cameras` | List cameras; `enabled` filter implemented |
| GET | `/api/v1/cameras/{camera_id}` | Read one camera |
| PATCH | `/api/v1/cameras/{camera_id}` | Update camera metadata |
| GET | `/api/v1/cameras/{camera_id}/health` | Current placeholder health state (`unknown`) |
| POST | `/api/v1/ai/violence/results` | Development adapter for structured worker results |
| GET | `/api/v1/events` | List persisted events, newest first |
| GET | `/api/v1/events/{event_id}` | Read event detail |
| GET | `/api/v1/demo/clips` | List approved clip IDs/display names; local-only |
| PUT | `/api/v1/demo/source` | Select a clip while no source session is active; local-only |
| POST | `/api/v1/demo/source/start` | Delegate to replay adapter; default app returns unavailable until one is configured |
| POST | `/api/v1/demo/source/stop` | Stop process-local source controller; local-only |
| POST | `/api/v1/demo/source/restart` | Delegate restart of active clip to replay adapter; local-only |
| GET | `/api/v1/demo/source/status` | Read process-local controller status; local-only |

Pagination/filtering beyond current implemented parameters, authentication/authorization, evidence, acknowledgement persistence, realtime delivery, source-health measurement, and stream/snapshot endpoints remain incomplete unless later commits explicitly add them.

## Demo media catalog foundation

`app.demo.clip_catalog.DemoClipCatalog` reads a local `manifest.json` with schema version `1` beneath the machine-local absolute `SENTINEL_DEMO_MEDIA_ROOT`. It resolves registered relative paths beneath that root, rejects absolute/traversal/escaping paths, and exposes only `clip_id` and `display_name` through its public DTO helper. The demo API consumes this catalog.

`app.demo.controller.VirtualCameraController` owns one process-local selection/session state and exposes a callback boundary for a replay adapter. The current app has no real replay adapter: catalog listing and clip selection work when the media root is configured, while starting a source returns `SOURCE_UNAVAILABLE`. Tests use a fake adapter only for controller/API behavior.

The controller is not connected to a decoder/replay loop, operator video delivery, or AI-worker processing. The default camera-health API remains `unknown` because no mapping from `DEMO-CAM-01` to an existing persisted camera UUID is configured. The catalog/controller do not establish media provenance/redistribution permission or verify that a file can be decoded. Do not treat these routes as evidence that virtual CCTV playback is implemented.

## Why `/health` can be 200 while a DB route fails

`/api/v1/health` is intentionally a **liveness** route. It does not touch the database. Therefore it can return `200` when the FastAPI process is alive even if a new local SQLite file has not been migrated yet.

Use:

```text
GET /api/v1/health/readiness
```

for database readiness.

An uninitialized schema returns HTTP `503` with safe guidance to run the documented initializer. The readiness route does not run migrations and does not expose DB URLs or raw SQL exceptions.

## Database initialization

SQLAlchemy and Alembic are used. SQLite is supported for local development/tests; PostgreSQL remains governed by project design/ADR status.

The database URL is selected by:

```text
SENTINEL_DATABASE_URL
```

If unset, the default is derived from the repository checkout:

```text
backend/runtime/sentinel.db
```

No user home directory is hard-coded.

From the repository root:

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python .\backend\scripts\init_database.py
```

The initializer:

1. resolves the configured DB URL;
2. creates the parent directory for file-backed SQLite when needed;
3. runs `alembic upgrade head`;
4. seeds the frozen violence model/version/global policy idempotently;
5. executes a read-only readiness verification;
6. fails non-zero if the post-initialization readiness check does not pass.

Read-only check:

```powershell
python .\backend\scripts\check_database.py
```

## Start backend

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Then verify:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health/readiness
Invoke-RestMethod http://127.0.0.1:8000/api/v1/cameras
Invoke-RestMethod http://127.0.0.1:8000/api/v1/events
```

A fresh correctly initialized database should return successful camera/event responses with empty `data` arrays until records are created.

## Public camera contract

Camera create/detail currently exposes:

```json
{
  "id": "camera-uuid",
  "name": "North Entrance",
  "description": null,
  "source_kind": "file",
  "enabled": true,
  "health": {
    "state": "unknown",
    "last_frame_at": null,
    "last_health_check_at": null
  },
  "created_at": "UTC timestamp",
  "updated_at": "UTC timestamp"
}
```

`unknown` is truthful: there is no integrated source-health measurement subsystem yet. `enabled` must not be interpreted as `online`.

## Public event contract

Implemented event responses map persistence names to public API names and include camera relation, acknowledgement summary shape, evidence count shape, and violence context when present.

Acknowledgement/evidence currently report truthful empty/unavailable state; the backend does not fabricate persistence that does not exist.

## Violence worker-result boundary

`POST /api/v1/ai/violence/results` accepts the frozen structured result contract.

The backend validates:

- schema shape;
- UUID identities;
- camera existence;
- frozen model version;
- score semantics/criterion contract;
- temporal ordering;
- explicit worker failures.

The frozen integrated criterion remains:

```text
threshold = 0.906
history = latest 5 observations
qualification = at least 3 positive observations
stride = 1
```

A qualified candidate still returns:

```json
{
  "candidate_condition": true,
  "event_persisted": false,
  "event_lifecycle": "awaiting_domain_policy"
}
```

because cooldown/deduplication/episode semantics remain unresolved. This portability/readiness package intentionally does not invent that policy.

## Tests

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m unittest discover -s .\backend\tests -p "test_*.py" -v
```

For an integration-safe disposable database plus frontend/AI checks, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_integration.ps1
```
