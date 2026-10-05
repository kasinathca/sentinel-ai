# Sentinel AI Backend

Backend work is on `gouri/backend-domain`. The application is a FastAPI modular monolith; violence inference remains in the separate AI worker. This README describes the implemented REST and structured-result boundary. It does not claim full raw-video, evidence, acknowledgement, authentication, or real-time integration.

## Implemented HTTP endpoints

| Method | Path | Behavior |
|---|---|---|
| GET | `/api/v1/health` | Service liveness |
| POST | `/api/v1/cameras` | Create camera with optional description |
| GET | `/api/v1/cameras` | List cameras; currently supports `enabled` filter |
| GET | `/api/v1/cameras/{camera_id}` | Read one camera |
| PATCH | `/api/v1/cameras/{camera_id}` | Update name, description, source kind, or enabled |
| GET | `/api/v1/cameras/{camera_id}/health` | Read current health; `unknown` until health measurements exist |
| POST | `/api/v1/ai/violence/results` | Development HTTP adapter for structured worker results |
| GET | `/api/v1/events` | List persisted events, newest first |
| GET | `/api/v1/events/{event_id}` | Read event details |

The API paths are current implementation endpoints, not a decision that HTTP is the permanent AI-worker transport. Pagination/filtering beyond `enabled` for cameras and default event listing remain incomplete.

## Public response contracts

Camera create/detail shape:

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

Camera list omits create/update timestamps, as described in the API specification. There is no camera source-health tracker yet; enabled cameras remain `unknown`, and disabled does not mean offline.

Event shape:

```json
{
  "id": "event-uuid",
  "event_type": "violence_fighting",
  "camera": {"id": "camera-uuid", "name": "North Entrance"},
  "occurred_at": "UTC timestamp",
  "created_at": "UTC timestamp",
  "requires_attention": true,
  "severity": null,
  "status": null,
  "acknowledgement": {
    "acknowledged": false,
    "acknowledged_by": [],
    "first_acknowledged_at": null
  },
  "evidence": {"available_count": 0, "pending_count": 0, "failed_count": 0},
  "context": {
    "model_version": {"id": "model-version-uuid", "name": "violence-model", "version": "MODEL-VIO-BIGRU-ATTN-XD-V1"},
    "output_label": "fighting",
    "score": 0.95,
    "event_threshold": 0.906,
    "score_semantics": "model-specific score",
    "window_started_at": "UTC timestamp",
    "window_ended_at": "UTC timestamp"
  }
}
```

The response mapper translates database names (`event_type_code`, `severity_code`, `lifecycle_status_code`, `score_value`, `event_threshold_snapshot`) to public API names. Acknowledgement and evidence values are truthful empty state because those subsystems do not exist in persistence yet.

## Worker-result integration boundary

`POST /api/v1/ai/violence/results` accepts `application/json`. It is a development integration adapter over the transport-neutral validation/criterion service.

Required successful observation:

```json
{
  "schema_version": "1",
  "job_id": "11111111-1111-4111-8111-111111111111",
  "correlation_id": "22222222-2222-4222-8222-222222222222",
  "camera_id": "33333333-3333-4333-8333-333333333333",
  "window": {
    "started_at": "2026-09-12T07:00:00Z",
    "ended_at": "2026-09-12T07:00:01Z"
  },
  "status": "success",
  "model": {
    "model_version_id": "6d22f83d-17f8-5ecf-9f0f-246fa326ec72",
    "task": "violence_fighting"
  },
  "result": {
    "label": "fighting",
    "score": 0.95,
    "score_semantics": "uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like"
  }
}
```

All IDs are UUIDs. Timestamps must include a timezone; window end must follow window start. Camera ID must already exist. Extra or malformed fields are rejected. `job_id` correlates one worker job; `correlation_id` is carried through to event context when a domain event is later created.

Explicit worker failure is represented with `status: "failed"` and `error: {"code":"INFERENCE_FAILED","message":"..."}` (code must be in the worker contract). A failure is an error, never a negative Fighting score.

Expected outcomes:

- A Normal sequence below `0.906` never reports `candidate_condition=true`; history still advances for valid observations.
- A Fighting/qualifying sequence can report a candidate once 3 of the latest 5 worker scores meet `>= 0.906`; W1 observations and stride 1 are expected.
- The exact frozen model version is `6d22f83d-17f8-5ecf-9f0f-246fa326ec72` (`MODEL-VIO-BIGRU-ATTN-XD-V1`).
- Every candidate response currently returns `event_persisted: false` and `event_lifecycle: "awaiting_domain_policy"`. Consecutive candidates cannot flood the event table because automatic persistence is intentionally held at the candidate/event boundary.
- Unknown model/version or contract mismatch is rejected; out-of-order windows return conflict; unknown camera returns not found. Invalid input returns HTTP 422. Worker transport/auth policy is not finalized.

The frozen threshold (`0.906`), criterion (3 of latest 5), W1, and model identity must not be altered for integration tests.

## Database and migration

SQLAlchemy and Alembic are used. SQLite remains supported for local development and tests; PostgreSQL is still proposed in the source documents. Migration `20261005_0002` adds nullable `cameras.description`, which is present in the database design. Frozen model/version and global policy seeding is idempotent. The project DB engine is set by `SENTINEL_DATABASE_URL`; the default is `backend/runtime/sentinel.db`.

Initialize/migrate and seed:

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python .\backend\scripts\init_database.py
```

Start the backend:

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m uvicorn app.main:app --app-dir .\backend --reload
```

Run backend tests:

```powershell
$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m unittest discover -s .\backend\tests -p "test_*.py" -v
```

Send a worker message by saving the example JSON above and using:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/ai/violence/results" -ContentType "application/json" -Body (Get-Content .\worker-result.json -Raw)
```

The first four positive observations are history warm-up; the fifth observation can produce the initial complete 3-of-5 candidate. Further qualifying observations remain candidates and do not insert additional events.

## Compatibility check with Aaditi's frontend branch

Read-only comparison was performed against `origin/aaditi/frontend-operator-ui` (`frontend/src/services/eventService.js`, `cameraService.js`, `Dashboard.jsx`, `EventDetails.jsx`, `EventCard.jsx`, and `CameraCard.jsx`). Event and camera resource fields consumed by the components now match the DTOs above. The operator page still contains mock-only acknowledgement behavior and must not claim persisted acknowledgement until the auth/user decision is made.

Service-layer integration can replace mock results with `fetch`/Axios calls and unwrap `response.data`:

| Current frontend service | Backend request | Returned value |
|---|---|---|
| `getEvents()` | `GET /api/v1/events` | response `data` array |
| `getEventById(id)` | `GET /api/v1/events/{id}` | response `data` event |
| `getCameras()` | `GET /api/v1/cameras` | response `data` array |
| `getCameraById(id)` | `GET /api/v1/cameras/{id}` | response `data` camera |
| `acknowledgeEvent(id)` | **Not available yet** | Requires auth identity and acknowledgement persistence |

Field compatibility checked against the frontend source:

| Frontend field | Backend field/state | Result |
|---|---|---|
| `event.event_type` | `event_type` | Matches |
| `event.camera.id/name` | relation-backed `camera.id/name` | Matches |
| `occurred_at`, `created_at`, `requires_attention`, `severity`, `status` | same public names | Matches; severity/status truthfully null when unset |
| `acknowledgement.*` | empty, unacknowledged object | Shape matches; persistence/action unavailable pending auth identity |
| `evidence.available_count/pending_count/failed_count` | all zero | Shape matches; no evidence rows/jobs exist |
| `context` | violence context object | Matches public `score`/`event_threshold` names |
| `camera.description/source_kind/enabled` | same public names | Matches |
| `camera.health.state/last_frame_at/last_health_check_at` | `unknown`/null/null | Shape matches; no health measurement exists |

No React component needs to know database column names. The current camera monitoring mock cannot become a real stream because stream/snapshot/source management is not implemented.

## Handoff status

### Implemented

- Existing Phase 2L/2M AI contract, criterion, persistence, model registry, seed, and migrations.
- Camera CRUD routes with documented DTO, optional description, and truthful unknown health response.
- Event list/detail public DTO with nested camera relation and mapped violence context.
- Strict typed worker-result HTTP adapter using deterministic contract fixtures.
- API tests for health, camera CRUD/validation/health, event DTO/order/not-found, worker invalid/unknown model/failure/normal/candidate sequences.

### Requires a project decision or later subsystem

- **Event episode lifecycle:** cooldown, duplicate suppression, close/retrigger rules remain unresolved. Candidate evaluations are not persisted automatically. Proposed options must be approved by the team before implementation.
- **Acknowledgement:** API specification requires authenticated user. No accepted auth mechanism/user registry exists in this persistence phase; no fake user or acknowledgement route/state has been introduced. Proposed integration: resolve authenticated principal to a persisted user ID, then add transaction-safe `event_acknowledgements` persistence and the documented POST/GET routes after the team confirms identity and idempotency semantics.
- **Evidence:** evidence storage/job state and endpoints are absent. Event summary is zero counts; no fake pending/available states.
- **Health:** no measurement tracker exists; state stays unknown.
- **Worker transport/security:** this HTTP route is a current development adapter. Architecture still marks permanent worker transport and internal worker authentication as TBD.
- **Pagination, event filters, enable/disable convenience routes, and standardized error envelope:** not implemented.

### Kasi's AI worker handoff

The backend does **not** need `best_model.pt`, MMAction2, the exact I3D extractor environment, or raw XD-Violence assets to accept already-produced observations. The backend boundary is `POST /api/v1/ai/violence/results`, JSON, with the schema above, exact frozen model version ID, an existing configured camera UUID, unique-per-observation job UUID, correlation UUID, timezone-aware sample window, and score semantics string. Success returns the validated score, positive flag, rolling-history counts, `candidate_condition`, frozen snapshots, `event_persisted=false`, and lifecycle status. Invalid contract/model is 422, unknown camera is 404, out-of-order is 409, worker failure is 422. These codes reflect this development adapter; final transport/auth response conventions remain open.

On the qualified runtime machine, Kasi should start the exact persistent extractor worker, load the already-qualified temporal model and extractor, run the approved Normal and Fighting fixtures, send each W1 structured result to this adapter, and verify Normal yields no candidates while Fighting reaches the frozen 3-of-5 candidate. Because lifecycle policy is unresolved, verify candidate/DB state only; expect no automatic event rows. This is the later raw-video E2E slice and has not been run here.

### Branch record

This handoff describes `gouri/backend-domain`. Implementation and tests were verified at commit `59af81c` (API, migration, and tests); the documentation-only handoff update follows it.

Verification completed for this implementation: backend suite **29 passed**; AI-worker contract/unit suite **15 passed**; disposable SQLite Alembic bootstrap reached `20261005_0002` and a second initialization remained safe, with one model version and one policy seeded.
