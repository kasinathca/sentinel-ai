---
title: "Sentinel AI — API and Integration Contract Specification"
document_id: "SEN-API"
version: "0.2.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
backend: "FastAPI"
api_style: "PROPOSED: REST-style HTTP + WebSocket event channel"
worker_transport: "TBD"
last_updated: "2026-09-12"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "frontend-backend HTTP contract"
  - "real-time event contract"
  - "backend-AI-worker logical contract"
  - "request and response schemas"
  - "error envelope"
  - "pagination"
  - "API naming conventions"
  - "contract versioning"
---

# Sentinel AI — API and Integration Contract Specification

> **Document purpose**
>
> This document defines the proposed API contracts for Sentinel AI.
>
> Once baselined, it shall be the authoritative source for:
>
> - frontend ↔ FastAPI HTTP interfaces;
> - frontend ↔ backend real-time messages;
> - backend ↔ AI worker logical payload contracts;
> - validation rules;
> - error structure;
> - pagination;
> - idempotency expectations;
> - resource naming;
> - request/response examples.
>
> This document exists specifically to prevent:
>
> - frontend developers inventing fields;
> - backend developers renaming fields without coordination;
> - AI workers sending undocumented payloads;
> - coding assistants creating endpoints based on guesswork.
>
> **Important:** The endpoint paths in this draft are `PROPOSED` until team baseline approval.
> Authentication mechanism and backend ↔ AI-worker transport remain `TBD`.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for integration contracts.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `01-vision-and-scope.md`
3. `02-srs.md`
4. `03-use-case-specification.md`
5. `04-system-architecture.md`
6. `06-database-design.md`
7. accepted ADRs

If an endpoint or field is not present in the baselined API contract, it shall not be invented silently.

## 0.2 Contract status vocabulary

| Status | Meaning |
|---|---|
| `CONFIRMED` | Accepted and frozen |
| `PROPOSED` | Candidate contract awaiting approval |
| `TBD` | Unresolved |
| `DEPRECATED` | Still accepted temporarily but being replaced |
| `REMOVED` | No longer valid |

## 0.3 API version

Proposed external API base:

```text
/api/v1
```

Status: `PROPOSED`.

## 0.4 Content type

Primary HTTP API content type:

```text
application/json
```

Media endpoints may return `image/*`, `video/*`, or a protected media-access redirect according to evidence-storage design.

## 0.5 Date/time format

Proposed:

```text
ISO 8601 / RFC 3339 timestamp strings
```

Example:

```text
2026-08-20T06:22:15.423Z
```

Server/API timestamps should represent UTC.

---

# 1. API Design Principles

## 1.1 Resource-oriented naming

Use plural nouns:

```text
/cameras
/zones
/rules
/events
/models
```

Avoid verb-heavy routes such as:

```text
/createCamera
/getEvents
/doAcknowledge
```

## 1.2 HTTP semantics

Recommended:

```text
GET     retrieve
POST    create/action
PATCH   partial update
DELETE  only where hard deletion is actually allowed
```

## 1.3 Stable public identifiers

Public identifiers should use stable UUID-style values.

## 1.4 DTO separation

API schemas are contracts; they are not automatically identical to ORM/database columns.

## 1.5 No hidden fields

Frontend code shall not rely on undocumented backend serialization.

## 1.6 No silent response drift

Renaming, removing, or changing field meaning is a contract change.

---

# 2. Authentication Contract

Authentication mechanism: `TBD`.

Potential implementations:

- cookie/session;
- bearer token;
- JWT;
- other approved method.

Each protected endpoint is marked with authentication and authorization expectations.

Proposed distinction:

```text
401 Unauthorized
```

for absent/invalid authentication.

```text
403 Forbidden
```

for authenticated users lacking permission.

---

# 3. Standard Error Envelope

```json
{
  "error": {
    "code": "CAMERA_NOT_FOUND",
    "message": "Camera was not found.",
    "details": {},
    "request_id": "uuid-or-correlation-id"
  }
}
```

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `error.code` | string | Yes | Stable machine-readable code |
| `error.message` | string | Yes | Safe human-readable message |
| `error.details` | object | No | Structured validation/context |
| `error.request_id` | string | No | Trace/correlation identifier |

The error response shall not expose stack traces, SQL, passwords, tokens, camera credentials, or sensitive filesystem paths.

---

# 4. Success Envelope

Single resource:

```json
{
  "data": {
    "id": "..."
  }
}
```

Collection:

```json
{
  "data": [],
  "meta": {}
}
```

Status: `PROPOSED`.

---

# 5. Pagination Contract

Proposed MVP style:

```text
limit
cursor
```

Example:

```text
GET /api/v1/events?limit=50&cursor=<opaque>
```

Response:

```json
{
  "data": [],
  "meta": {
    "limit": 50,
    "next_cursor": "opaque-or-null",
    "has_more": false
  }
}
```

Rules:

- exact default/max limit: `TBD`;
- cursor is opaque;
- client must not infer DB structure;
- malformed cursor is rejected.

---

# 6. Common Data Types

## 6.1 Identifier

```json
"1b63dd0d-6338-4388-bf5b-38e5a46ba51b"
```

## 6.2 Normalized coordinate

```json
0.4238102
```

Proposed domain:

```text
0.0 <= value <= 1.0
```

## 6.3 Timestamp

```json
"2026-08-20T06:22:15.423Z"
```

## 6.4 Duration

Proposed API unit:

```text
integer milliseconds
```

Example:

```json
30000
```

No threshold values in examples are requirements.

---

# 7. Health Endpoint

## 7.1 `GET /api/v1/health`

**Status:** `PROPOSED`

Response:

```json
{
  "data": {
    "status": "ok",
    "service": "sentinel-api",
    "version": "0.1.0"
  }
}
```

Must not expose secrets.

---

# 8. Readiness Endpoint

## 8.1 `GET /api/v1/health/readiness`

**Status:** `PROPOSED`

```json
{
  "data": {
    "status": "degraded",
    "components": {
      "database": "ok",
      "ai_worker": "unavailable",
      "evidence_storage": "ok"
    }
  }
}
```

---

# 9. Authentication Endpoints

Exact auth mechanism is unresolved.

If local application auth is selected, proposed:

```text
POST /api/v1/auth/login
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

All remain `TBD_CONTRACT`.

Example `/auth/me` response:

```json
{
  "data": {
    "id": "user-uuid",
    "display_name": "Operator",
    "roles": ["operator"]
  }
}
```

---

# 10. Camera Resource

```json
{
  "id": "camera-uuid",
  "name": "North Entrance",
  "description": "Primary entrance camera",
  "source_kind": "file",
  "enabled": true,
  "health": {
    "state": "healthy",
    "last_frame_at": "2026-08-20T06:22:15.423Z",
    "last_health_check_at": "2026-08-20T06:22:16.000Z"
  },
  "created_at": "2026-08-20T05:00:00.000Z",
  "updated_at": "2026-08-20T05:00:00.000Z"
}
```

`source_locator` may be omitted from normal operator responses.

Credentials shall never be returned.

---

# 11. Create Camera

## `POST /api/v1/cameras`

**Status:** `PROPOSED`  
**Authentication:** Required  
**Authorization:** Administrator / `TBD`

Request:

```json
{
  "name": "North Entrance",
  "description": "Primary entrance camera",
  "source_kind": "file",
  "source": {
    "locator": "/data/samples/entrance.mp4",
    "credential_ref": null
  },
  "enabled": true
}
```

Potential `source_kind` values are not baselined. Only implemented values may be accepted.

Response `201`:

```json
{
  "data": {
    "id": "camera-uuid",
    "name": "North Entrance",
    "description": "Primary entrance camera",
    "source_kind": "file",
    "enabled": true,
    "health": {
      "state": "unknown",
      "last_frame_at": null,
      "last_health_check_at": null
    },
    "created_at": "2026-08-20T05:00:00.000Z",
    "updated_at": "2026-08-20T05:00:00.000Z"
  }
}
```

Errors:

```text
INVALID_CAMERA_CONFIGURATION
UNAUTHENTICATED
FORBIDDEN
CAMERA_NAME_CONFLICT
VALIDATION_ERROR
```

---

# 12. List Cameras

## `GET /api/v1/cameras`

Query parameters:

```text
enabled
health_state
limit
cursor
```

Response:

```json
{
  "data": [
    {
      "id": "camera-uuid",
      "name": "North Entrance",
      "description": null,
      "source_kind": "file",
      "enabled": true,
      "health": {
        "state": "healthy",
        "last_frame_at": "2026-08-20T06:22:15.423Z",
        "last_health_check_at": "2026-08-20T06:22:16.000Z"
      }
    }
  ],
  "meta": {
    "limit": 50,
    "next_cursor": null,
    "has_more": false
  }
}
```

---

# 13. Get Camera

## `GET /api/v1/cameras/{camera_id}`

Errors:

```text
CAMERA_NOT_FOUND
FORBIDDEN
```

---

# 14. Update Camera

## `PATCH /api/v1/cameras/{camera_id}`

Example:

```json
{
  "name": "North Gate",
  "description": "Renamed display label"
}
```

Immutable identifiers shall be rejected if supplied for mutation.

---

# 15. Enable / Disable Camera

```text
POST /api/v1/cameras/{camera_id}/enable
POST /api/v1/cameras/{camera_id}/disable
```

**Status:** `PROPOSED`.

Response:

```json
{
  "data": {
    "id": "camera-uuid",
    "enabled": false
  }
}
```

---

# 16. Camera Health

## `GET /api/v1/cameras/{camera_id}/health`

```json
{
  "data": {
    "camera_id": "camera-uuid",
    "enabled": true,
    "state": "offline",
    "last_frame_at": "2026-08-20T06:20:00.000Z",
    "last_health_check_at": "2026-08-20T06:22:00.000Z"
  }
}
```

---

# 17. Zone Resource

```json
{
  "id": "zone-uuid",
  "camera_id": "camera-uuid",
  "name": "Restricted Door Area",
  "zone_kind": "restricted",
  "enabled": true,
  "geometry_version": 1,
  "polygon": [
    {"x": 0.10, "y": 0.20},
    {"x": 0.50, "y": 0.20},
    {"x": 0.50, "y": 0.70},
    {"x": 0.10, "y": 0.70}
  ],
  "created_at": "2026-08-20T05:00:00.000Z",
  "updated_at": "2026-08-20T05:00:00.000Z"
}
```

Proposed coordinate rule:

```text
0.0 <= x <= 1.0
0.0 <= y <= 1.0
```

---

# 18. Create Zone

## `POST /api/v1/cameras/{camera_id}/zones`

```json
{
  "name": "Restricted Door Area",
  "zone_kind": "restricted",
  "polygon": [
    {"x": 0.10, "y": 0.20},
    {"x": 0.50, "y": 0.20},
    {"x": 0.50, "y": 0.70},
    {"x": 0.10, "y": 0.70}
  ],
  "enabled": true
}
```

Validation shall cover:

- vertex count;
- coordinate range;
- polygon validity;
- camera existence;
- naming rules.

---

# 19. List Zones

## `GET /api/v1/cameras/{camera_id}/zones`

Query:

```text
enabled
zone_kind
```

---

# 20. Get Zone

## `GET /api/v1/zones/{zone_id}`

---

# 21. Update Zone

## `PATCH /api/v1/zones/{zone_id}`

If geometry changes, `geometry_version` increments.

---

# 22. Enable / Disable Zone

```text
POST /api/v1/zones/{zone_id}/enable
POST /api/v1/zones/{zone_id}/disable
```

---

# 23. Rule Resource

```json
{
  "id": "rule-uuid",
  "camera_id": "camera-uuid",
  "zone_id": "zone-uuid",
  "name": "Door intrusion rule",
  "rule_type": "restricted_area_intrusion",
  "enabled": true,
  "version": 1,
  "configuration": {},
  "created_at": "2026-08-20T05:00:00.000Z",
  "updated_at": "2026-08-20T05:00:00.000Z"
}
```

The API exposes polymorphic `configuration`; the database may store rule config relationally.

---

# 24. Create Intrusion Rule

## `POST /api/v1/rules`

```json
{
  "name": "Door intrusion rule",
  "rule_type": "restricted_area_intrusion",
  "camera_id": "camera-uuid",
  "zone_id": "zone-uuid",
  "enabled": true,
  "configuration": {
    "position_method": "approved-method-code",
    "require_transition_from_outside": true,
    "cooldown_ms": null
  }
}
```

The allowed `position_method` is `TBD`.

---

# 25. Create Loitering Rule

```json
{
  "name": "Lobby loitering",
  "rule_type": "loitering",
  "camera_id": "camera-uuid",
  "zone_id": "zone-uuid",
  "enabled": true,
  "configuration": {
    "dwell_threshold_ms": 30000,
    "track_loss_grace_ms": 1000,
    "reset_on_exit": true,
    "retrigger_after_ms": null
  }
}
```

All numeric values are illustrative, not defaults.

---

# 26. Create Crowd Rule

```json
{
  "name": "Lobby crowd threshold",
  "rule_type": "crowd_threshold",
  "camera_id": "camera-uuid",
  "zone_id": "zone-uuid",
  "enabled": true,
  "configuration": {
    "person_threshold": 5,
    "counting_method": "active_tracks",
    "retrigger_after_ms": null
  }
}
```

`counting_method` remains `TBD`.

---

# 27. List Rules

## `GET /api/v1/rules`

Query:

```text
camera_id
zone_id
rule_type
enabled
limit
cursor
```

---

# 28. Get Rule

## `GET /api/v1/rules/{rule_id}`

---

# 29. Update Rule

## `PATCH /api/v1/rules/{rule_id}`

Material configuration updates shall increment `version`.

---

# 30. Enable / Disable Rule

```text
POST /api/v1/rules/{rule_id}/enable
POST /api/v1/rules/{rule_id}/disable
```

---

# 31. Model Version Summary

```json
{
  "id": "model-version-uuid",
  "model_id": "model-uuid",
  "name": "violence-model",
  "version": "v1",
  "task": "violence_fighting",
  "status": "approved"
}
```

Local artifact paths shall not be exposed to ordinary frontend clients.

---

# 32. Event Resource

```json
{
  "id": "event-uuid",
  "event_type": "restricted_area_intrusion",
  "camera": {
    "id": "camera-uuid",
    "name": "North Entrance"
  },
  "occurred_at": "2026-08-20T06:22:15.423Z",
  "created_at": "2026-08-20T06:22:15.900Z",
  "requires_attention": true,
  "severity": null,
  "status": null,
  "acknowledgement": {
    "acknowledged": false,
    "acknowledged_by": [],
    "first_acknowledged_at": null
  },
  "evidence": {
    "available_count": 0,
    "pending_count": 1,
    "failed_count": 0
  },
  "context": {}
}
```

---

# 33. Intrusion Event Context

```json
{
  "rule_id": "rule-uuid",
  "zone_id": "zone-uuid",
  "zone_geometry_version": 1,
  "track_id": "track-42",
  "trigger_position": {
    "x": 0.42,
    "y": 0.67
  },
  "position_method": "approved-method-code",
  "cooldown_ms": null
}
```

---

# 34. Loitering Event Context

```json
{
  "rule_id": "rule-uuid",
  "zone_id": "zone-uuid",
  "zone_geometry_version": 2,
  "track_id": "track-19",
  "observed_dwell_ms": 30142,
  "threshold_ms": 30000,
  "track_loss_grace_ms": 1000,
  "retrigger_after_ms": null
}
```

Values are illustrative.

---

# 35. Crowd Event Context

```json
{
  "rule_id": "rule-uuid",
  "zone_id": "zone-uuid",
  "zone_geometry_version": 1,
  "observed_count": 7,
  "threshold_count": 5,
  "counting_method": "active_tracks"
}
```

---

# 36. Violence Event Context

```json
{
  "model_version": {
    "id": "model-version-uuid",
    "name": "violence-model",
    "version": "v1"
  },
  "output_label": "violence",
  "score": 0.87,
  "event_threshold": 0.75,
  "score_semantics": "model-specific score",
  "window_started_at": "2026-08-20T06:22:10.000Z",
  "window_ended_at": "2026-08-20T06:22:15.000Z"
}
```

Do not interpret `score` as calibrated probability unless documented.

---

# 37. Camera Offline Event Context

```json
{
  "last_frame_at": "2026-08-20T06:20:00.000Z",
  "offline_after_ms": 10000,
  "reason": "frame_timeout",
  "health_state_before": "healthy",
  "health_state_after": "offline"
}
```

Values are illustrative.

---

# 38. List Events

## `GET /api/v1/events`

Query:

```text
camera_id
event_type
occurred_from
occurred_to
acknowledged
status
requires_attention
limit
cursor
```

Default proposed ordering:

```text
occurred_at DESC, id DESC
```

---

# 39. Get Event

## `GET /api/v1/events/{event_id}`

Returns full event detail including polymorphic context, acknowledgement state, and evidence summary.

---

# 40. Acknowledge Event

## `POST /api/v1/events/{event_id}/acknowledgements`

Authentication: Required.

Request:

```json
{
  "comment": "Reviewed by operator."
}
```

Response:

```json
{
  "data": {
    "id": "ack-uuid",
    "event_id": "event-uuid",
    "user": {
      "id": "user-uuid",
      "display_name": "Operator"
    },
    "acknowledged_at": "2026-08-20T06:23:20.000Z",
    "comment": "Reviewed by operator."
  }
}
```

Proposed idempotency:

same user + same event returns existing acknowledgement rather than duplicate.

---

# 41. List Event Acknowledgements

## `GET /api/v1/events/{event_id}/acknowledgements`

---

# 42. False-Positive Feedback

## `POST /api/v1/events/{event_id}/feedback`

**Status:** `PROPOSED / OPTIONAL_MVP`

```json
{
  "feedback": "false_positive",
  "reason_code": "normal_activity",
  "notes": "Operator review indicates expected activity."
}
```

This shall not automatically trigger model retraining.

---

# 43. Evidence Resource

```json
{
  "id": "evidence-uuid",
  "event_id": "event-uuid",
  "type": "snapshot",
  "status": "available",
  "mime_type": "image/jpeg",
  "size_bytes": 45213,
  "capture_started_at": "2026-08-20T06:22:15.000Z",
  "capture_ended_at": "2026-08-20T06:22:15.000Z",
  "created_at": "2026-08-20T06:22:16.000Z"
}
```

Storage key/path is not necessarily exposed.

---

# 44. List Event Evidence

## `GET /api/v1/events/{event_id}/evidence`

Returns evidence metadata.

---

# 45. Retrieve Evidence Content

## `GET /api/v1/evidence/{evidence_id}/content`

Potential responses:

```text
200 media bytes
302/307 protected redirect
404 not found
409 pending/failed
```

Final behavior depends on evidence-storage decision.

---

# 46. Evidence Metadata

## `GET /api/v1/evidence/{evidence_id}`

Returns metadata only.

---

# 47. Analytics Overview

## `GET /api/v1/analytics/overview`

Query:

```text
from
to
camera_id
```

Example response:

```json
{
  "data": {
    "range": {
      "from": "2026-08-20T00:00:00Z",
      "to": "2026-08-21T00:00:00Z"
    },
    "total_events": 42,
    "events_by_type": {
      "restricted_area_intrusion": 10,
      "loitering": 8,
      "crowd_threshold": 6,
      "violence_fighting": 3,
      "camera_offline": 15
    },
    "acknowledged_events": 25,
    "unacknowledged_events": 17
  }
}
```

Numbers are illustrative.

---

# 48. Analytics Time Series

## `GET /api/v1/analytics/events/timeseries`

Query:

```text
from
to
interval
camera_id
event_type
```

Example:

```json
{
  "data": [
    {
      "bucket_start": "2026-08-20T06:00:00Z",
      "count": 4
    }
  ],
  "meta": {
    "interval": "hour"
  }
}
```

---

# 49. Analytics by Camera

## `GET /api/v1/analytics/events/by-camera`

```json
{
  "data": [
    {
      "camera": {
        "id": "camera-uuid",
        "name": "North Entrance"
      },
      "event_count": 12
    }
  ]
}
```

---

# 50. Camera Health History

## `GET /api/v1/cameras/{camera_id}/health-history`

Returns health state transitions, not every heartbeat.

---

# 51. Model Registry

Potential:

```text
GET /api/v1/models
GET /api/v1/models/{model_id}/versions/{version_id}
```

Status: `PROPOSED`, lower priority than core MVP workflows.

---

# 52. WebSocket Endpoint

Recommended draft path:

```text
/api/v1/ws/events
```

Status: `PROPOSED`.

Authentication: `TBD`.

Do not place long-lived credentials in query strings unless explicitly justified.

---

# 53. WebSocket Envelope

```json
{
  "type": "event.created",
  "message_id": "message-uuid",
  "occurred_at": "2026-08-20T06:22:15.900Z",
  "data": {}
}
```

Fields:

| Field | Required | Meaning |
|---|---:|---|
| `type` | Yes | Stable message type |
| `message_id` | Yes | Message identity |
| `occurred_at` | Yes | Message emission time |
| `data` | Yes | Typed payload |

---

# 54. Proposed WebSocket Message Types

```text
event.created
event.updated
event.acknowledged
camera.health_changed
system.degraded
```

---

# 55. `event.created`

```json
{
  "type": "event.created",
  "message_id": "message-uuid",
  "occurred_at": "2026-08-20T06:22:15.900Z",
  "data": {
    "event": {
      "id": "event-uuid",
      "event_type": "restricted_area_intrusion",
      "camera": {
        "id": "camera-uuid",
        "name": "North Entrance"
      },
      "occurred_at": "2026-08-20T06:22:15.423Z",
      "requires_attention": true
    }
  }
}
```

---

# 56. `event.acknowledged`

```json
{
  "type": "event.acknowledged",
  "message_id": "message-uuid",
  "occurred_at": "2026-08-20T06:23:20.000Z",
  "data": {
    "event_id": "event-uuid",
    "acknowledgement": {
      "id": "ack-uuid",
      "user_id": "user-uuid",
      "acknowledged_at": "2026-08-20T06:23:20.000Z"
    }
  }
}
```

---

# 57. `camera.health_changed`

```json
{
  "type": "camera.health_changed",
  "message_id": "message-uuid",
  "occurred_at": "2026-08-20T06:25:00.000Z",
  "data": {
    "camera_id": "camera-uuid",
    "from_state": "healthy",
    "to_state": "offline"
  }
}
```

---

# 58. Real-Time Delivery Semantics

The system shall not promise exactly-once WebSocket delivery.

Proposed semantics:

```text
best-effort live updates + persisted-state reconciliation
```

Client requirements:

- deduplicate by stable IDs;
- show disconnected state;
- reconnect;
- refetch persisted state;
- merge by event identity.

---

# 59. Reconnection Flow

```text
disconnect
→ mark disconnected
→ reconnect
→ fetch persisted events since checkpoint/current range
→ reconcile by event ID
→ resume live updates
```

Checkpoint mechanism remains `TBD`.

---

# 60. AI Worker Logical Contract

Backend ↔ worker transport remains unresolved.

This section is transport-neutral.

Any HTTP/queue/IPC adapter must preserve equivalent fields and semantics.

---

# 61. Worker Processing Request

```json
{
  "schema_version": "1",
  "job_id": "job-uuid",
  "correlation_id": "correlation-uuid",
  "source": {
    "camera_id": "camera-uuid",
    "source_kind": "file",
    "source_locator_ref": "opaque-or-config-reference"
  },
  "tasks": [
    "person_detection",
    "person_tracking"
  ],
  "requested_at": "2026-08-20T06:20:00.000Z",
  "options": {}
}
```

Rules:

- source reference shall not expose secrets unnecessarily;
- tasks must be supported by worker;
- `job_id` is not an event ID.

---

# 62. Worker Observation Result

```json
{
  "schema_version": "1",
  "job_id": "job-uuid",
  "correlation_id": "correlation-uuid",
  "camera_id": "camera-uuid",
  "source_timestamp": "2026-08-20T06:20:01.234Z",
  "processing_timestamp": "2026-08-20T06:20:01.300Z",
  "status": "success",
  "models": [
    {
      "task": "person_detection",
      "model_version_id": "model-version-uuid"
    }
  ],
  "detections": [
    {
      "class": "person",
      "confidence": 0.93,
      "bbox": {
        "x_min": 0.20,
        "y_min": 0.10,
        "x_max": 0.40,
        "y_max": 0.90
      },
      "track_id": "track-17"
    }
  ]
}
```

Proposed bbox constraints:

```text
0 <= x_min < x_max <= 1
0 <= y_min < y_max <= 1
```

---

# 63. Worker Valid Empty Detection Result

```json
{
  "schema_version": "1",
  "job_id": "job-uuid",
  "correlation_id": "correlation-uuid",
  "camera_id": "camera-uuid",
  "source_timestamp": "2026-08-20T06:20:01.234Z",
  "processing_timestamp": "2026-08-20T06:20:01.300Z",
  "status": "success",
  "models": [
    {
      "task": "person_detection",
      "model_version_id": "model-version-uuid"
    }
  ],
  "detections": []
}
```

This is a valid negative/empty result and is distinct from inference failure.

---

# 64. Worker Violence Result

The qualified violence worker result remains transport-neutral.

```json
{
  "schema_version": "1",
  "job_id": "job-uuid",
  "correlation_id": "correlation-uuid",
  "camera_id": "camera-uuid",
  "window": {
    "started_at": "2026-09-12T07:00:00.000Z",
    "ended_at": "2026-09-12T07:00:02.667Z"
  },
  "status": "success",
  "model": {
    "model_version_id": "6d22f83d-17f8-5ecf-9f0f-246fa326ec72",
    "task": "violence_fighting"
  },
  "result": {
    "label": "fighting",
    "score": 0.94,
    "score_semantics": "uncalibrated sigmoid score for the fighting positive class from EXP-VIO-TEMPORAL-001; higher means more fighting-like"
  }
}
```

Normative interpretation:

- `label = "fighting"` identifies the positive class whose score is reported;
- a successful result is a **model observation**, not a persistent event;
- the worker shall not convert a low score into an application-domain
  `no_event` record;
- the backend applies the frozen live criterion described below;
- the backend shall validate `model_version_id`, task, time window, score range,
  and schema version before using the result.

The stable model-version UUID above is derived from the immutable frozen
checkpoint identity and is reserved for the selected violence model version.


# 64A. Frozen Violence Event Criterion

The live violence criterion was selected using validation data only and frozen
before the one-time official TEST evaluation.

```text
window representation = one exact I3D feature step
stride                = one feature step
positive threshold    = score >= 0.906
temporal smoothing    = at least 3 positive scores among the most recent 5
```

The criterion is a backend/domain rule over valid worker observations.

It shall **not** be implemented by changing the model output schema into an
`event=true` field.

A backend implementation should maintain rolling state per camera/model stream:

```text
camera_id
model_version_id
ordered recent violence scores
ordered window timestamps
```

A qualifying 3-of-5 state means:

```text
candidate violence condition = true
```

It does not by itself define:

- duplicate-event suppression;
- event reopening;
- alert cooldown;
- incident grouping;
- acknowledgement behavior.

Those application semantics remain separate and must be finalized in the event
domain specification.

## 64A.1 Frozen threshold provenance

Threshold `0.906` was selected on the frozen validation split after:

1. freezing the temporal model;
2. freezing `W1 / stride 1 / 3-of-5`;
3. performing validation-only threshold calibration;
4. choosing the validation Pareto-knee operating point;
5. freezing the policy;
6. executing the official TEST exactly once.

No threshold search is permitted on official TEST data after this freeze.

Detailed evidence is recorded in
`19-violence-model-and-runtime-qualification.md`.


---

# 65. Worker Failure Result

```json
{
  "schema_version": "1",
  "job_id": "job-uuid",
  "correlation_id": "correlation-uuid",
  "camera_id": "camera-uuid",
  "status": "failed",
  "error": {
    "code": "MODEL_LOAD_FAILED",
    "message": "Required model could not be loaded."
  }
}
```

A worker failure shall never be converted into a successful non-violence/no-person result.

---

# 66. Worker Error Codes

Proposed:

```text
MODEL_LOAD_FAILED
UNSUPPORTED_INPUT
VIDEO_DECODE_FAILED
INFERENCE_FAILED
TRACKING_FAILED
INVALID_REQUEST
INSUFFICIENT_TEMPORAL_INPUT
INTERNAL_WORKER_ERROR
```

---

# 67. Worker Health / Capability Interface

If HTTP transport is selected:

```text
GET /internal/v1/health
GET /internal/v1/capabilities
```

Status: `PROPOSED_IF_HTTP_TRANSPORT`.

Example capabilities:

```json
{
  "data": {
    "tasks": [
      "person_detection",
      "person_tracking",
      "violence_fighting"
    ],
    "models": [
      {
        "task": "person_detection",
        "model_version_id": "model-version-uuid"
      }
    ]
  }
}
```

Equivalent behavior is required if queue/IPC is chosen.

---

# 68. Internal Worker Security

If worker communication crosses a network boundary:

- internal endpoints shall not be public by default;
- internal authentication/network trust shall be documented;
- worker payload validation remains mandatory.

Exact mechanism: `TBD`.

---

# 69. Correlation Semantics

## `job_id`

One worker-processing unit.

## `correlation_id`

End-to-end trace identity.

Potentially propagated through:

```text
backend
worker
worker result
event
logs
```

## `event_id`

Created only after backend decides a domain event exists.

---

# 70. General Validation Rules

Reject:

- malformed identifiers;
- malformed timestamps;
- coordinates outside range;
- invalid polygon;
- unknown rule/event codes;
- negative durations;
- zero/negative crowd threshold;
- source/zone mismatch;
- missing required nested objects;
- malformed worker result.

---

# 71. Validation Error Example

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": {
      "fields": [
        {
          "path": "polygon[2].x",
          "code": "OUT_OF_RANGE",
          "message": "Value must be between 0 and 1."
        }
      ]
    },
    "request_id": "request-uuid"
  }
}
```

---

# 72. Proposed HTTP Status Mapping

| Situation | HTTP |
|---|---:|
| successful GET | 200 |
| created resource | 201 |
| existing idempotent acknowledgement | 200 |
| action with no response body if used | 204 |
| invalid domain request | 400 |
| unauthenticated | 401 |
| forbidden | 403 |
| not found | 404 |
| state conflict | 409 |
| unsupported media/input | 415 |
| schema validation | 422 |
| rate limit if implemented | 429 |
| internal server error | 500 |
| dependency unavailable | 503 |

---

# 73. Stable Error Codes

## Authentication

```text
UNAUTHENTICATED
FORBIDDEN
```

## Not Found

```text
CAMERA_NOT_FOUND
ZONE_NOT_FOUND
RULE_NOT_FOUND
EVENT_NOT_FOUND
EVIDENCE_NOT_FOUND
MODEL_NOT_FOUND
USER_NOT_FOUND
```

## State / Conflict

```text
RULE_STATE_CONFLICT
EVENT_STATE_CONFLICT
CAMERA_DISABLED
DUPLICATE_RESOURCE
```

## Source

```text
SOURCE_UNAVAILABLE
SOURCE_CONFIGURATION_INVALID
SOURCE_DISABLED
SOURCE_TYPE_UNSUPPORTED
```

## Evidence

```text
EVIDENCE_PENDING
EVIDENCE_FAILED
EVIDENCE_DELETED
EVIDENCE_ACCESS_DENIED
```

---

# 74. Rate Limiting

Status: `TBD/DEFERRED`.

Do not add arbitrary rate limits.

Login may later require rate limiting for security.

---

# 75. Video Upload Endpoint

Only define if uploaded-video input is selected.

Potential:

```text
POST /api/v1/uploads/videos
```

Status: `TBD`.

If implemented:

- size limits;
- type validation;
- safe filename handling;
- isolated storage;
- no traversal.

---

# 76. Camera Stream Endpoint

Not defined yet.

Potential:

```text
GET /api/v1/cameras/{camera_id}/stream
```

Status: `TBD`.

Streaming depends on selected camera/input/browser design.

---

# 77. Camera Snapshot Endpoint

Potential:

```text
GET /api/v1/cameras/{camera_id}/snapshot
```

Status: `PROPOSED_IF_NEEDED_FOR_ZONE_EDITOR`.

---

# 78. Event Context Schema Version

Potential:

```json
{
  "context_schema_version": "1"
}
```

Status: `PROPOSED`.

Useful if event context evolves.

---

# 79. API Versioning Policy

External API:

```text
/api/v1
```

Worker messages:

```text
schema_version
```

Breaking changes include:

- removing/renaming fields;
- changing units;
- changing coordinate convention;
- changing enum semantics;
- changing requiredness.

Breaking changes require coordinated version/baseline updates.

---

# 80. Machine Codes vs Display Labels

Machine code:

```text
restricted_area_intrusion
```

Display:

```text
Restricted Area Intrusion
```

Never use UI labels as protocol identifiers.

---

# 81. Proposed Event Type Codes

```text
restricted_area_intrusion
loitering
crowd_threshold
violence_fighting
camera_offline
```

---

# 82. Proposed Rule Type Codes

```text
restricted_area_intrusion
loitering
crowd_threshold
```

---

# 83. Proposed Evidence Type Codes

```text
snapshot
clip
```

---

# 84. Proposed Evidence Status Codes

```text
pending
available
failed
deleted
```

---

# 85. Proposed Camera Health Codes

```text
unknown
healthy
degraded
offline
```

Intentional disable is separate from health state.

---

# 86. Proposed Model Task Codes

```text
person_detection
person_tracking
violence_fighting
```

---

# 87. Null Semantics

Null must have one defined meaning.

Examples:

```text
severity = null
```

means severity not assigned/not baselined.

```text
last_frame_at = null
```

means no valid frame recorded.

Do not substitute empty string for unknown values.

---

# 88. PATCH Semantics

- omitted field → unchanged;
- explicit `null` → clear only if nullable;
- immutable field mutation → reject.

---

# 89. Event Search Time Semantics

Proposed filtering:

```text
occurred_at >= occurred_from
occurred_at < occurred_to
```

Filter event occurrence time, not row creation time.

---

# 90. CORS

Allowed origins shall be configured according to frontend deployment.

Do not use unrestricted credentialed CORS in final configuration.

---

# 91. Evidence Authorization

Evidence must be protected at least as strongly as event metadata.

Knowing an evidence ID must not bypass authorization.

---

# 92. Audit API

Potential:

```text
GET /api/v1/audit
```

Status: `TBD`.

If implemented, likely restricted to Administrator/Reviewer.

---

# 93. API-to-SRS Traceability

| API | Requirement families |
|---|---|
| `/cameras` | FR-CAM-* |
| `/zones` | FR-ZONE-* |
| `/rules` | FR-RULE-*, FR-INT-*, FR-LOIT-*, FR-CROWD-* |
| `/events` | FR-EVT-* |
| acknowledgements | FR-ALT-004/005 |
| feedback | FR-ALT-006 |
| evidence | FR-EVD-* |
| analytics | FR-ANL-* |
| WebSocket | FR-ALT-002, FR-UI-005 |
| worker contract | FR-DET-*, FR-TRK-*, FR-VIO-*, FR-INTG-* |
| auth | FR-AUTH-*, NFR-SEC-* |
| errors | NFR-SEC-005/007 |
| pagination | FR-HIST-006 |

---

# 94. API-to-Use-Case Traceability

| Use Case | API |
|---|---|
| UC-CAM-001 | POST `/cameras` |
| UC-CAM-002 | GET `/cameras` |
| UC-CAM-003 | PATCH `/cameras/{id}` |
| UC-CAM-004 | enable/disable camera |
| UC-ZONE-001 | POST camera zones |
| UC-ZONE-002 | PATCH zone |
| UC-RULE-001/2/3 | POST `/rules` |
| UC-MON-001 | WebSocket + GET `/events` |
| UC-EVT-006 | POST acknowledgements |
| UC-EVD-001 | GET evidence |
| UC-HIST-001 | GET `/events` filters |
| UC-ANL-001 | GET `/analytics/*` |
| UC-AI-001 | worker observation contract |
| UC-AI-002 | worker violence contract |
| UC-SYS-001 | health/readiness + worker error |
| UC-SYS-004 | reconnect + event reconciliation |

---

# 95. FastAPI / OpenAPI Alignment

FastAPI can generate OpenAPI from typed request/response schemas.

Once this document is baselined:

- Pydantic schemas should implement this contract;
- generated OpenAPI should be reviewed against this file;
- generated OpenAPI does not replace this engineering specification;
- divergence shall be treated as a defect.

---

# 96. OpenAPI Contract Snapshot

Recommended integration/CI process:

1. start backend;
2. export generated OpenAPI;
3. compare accepted paths/schemas with a contract snapshot;
4. flag breaking drift.

Status: `PROPOSED`.

---

# 97. Frontend Type Generation

If selected frontend stack supports it, generate API types from OpenAPI.

Benefits:

- field-name consistency;
- faster parallel implementation;
- compile-time mismatch detection.

Status: `PROPOSED`.

---

# 98. Mock API

Frontend may use mock data before backend implementation.

Mocks must conform to this contract and be clearly separated from production data.

Mock success does not prove backend integration.

---

# 99. Contract Tests

Minimum contract tests:

- create/get camera;
- zone polygon validation;
- rule polymorphic config validation;
- event context per event type;
- acknowledgement idempotency;
- evidence authorization;
- worker malformed payload;
- worker explicit failure;
- WebSocket message schemas;
- pagination metadata.

---

# 100. End-to-End API Flow — Intrusion

```text
1. POST /api/v1/cameras
2. POST /api/v1/cameras/{camera_id}/zones
3. POST /api/v1/rules
4. AI worker sends tracked observation
5. backend evaluates intrusion
6. backend persists event
7. WebSocket emits event.created
8. frontend GET /api/v1/events/{event_id}
9. frontend GET /api/v1/events/{event_id}/evidence
10. operator POST /api/v1/events/{event_id}/acknowledgements
11. WebSocket emits event.acknowledged
```

---

# 101. End-to-End API Flow — History

```text
GET /api/v1/events
    ?occurred_from=...
    &occurred_to=...
    &event_type=loitering
    &camera_id=...
    &acknowledged=false
    &limit=50
```

---

# 102. End-to-End API Flow — Analytics

```text
GET /api/v1/analytics/overview?from=...&to=...
GET /api/v1/analytics/events/timeseries?from=...&to=...&interval=hour
GET /api/v1/analytics/events/by-camera?from=...&to=...
```

---

# 103. End-to-End Worker Flow — Person Observation

```text
camera/video
→ worker job
→ detection/tracking
→ AIObservationResult
→ backend contract validation
→ deterministic rule evaluation
→ event persistence
→ WebSocket event.created
```

---

# 104. End-to-End Worker Flow — Violence

```text
video temporal window
→ violence worker inference
→ structured model result
→ backend validates model/version
→ backend applies event threshold
→ violence event
→ evidence
→ operator notification
```

---

# 105. Request Logging

Recommended API request log fields:

```text
request_id
route_template
method
status_code
duration
authenticated_user_id where appropriate
```

Do not log full sensitive request bodies.

---

# 106. Request ID

Proposed response header:

```text
X-Request-ID
```

Status: `PROPOSED`.

---

# 107. Timeouts

No request or worker timeout value is currently baselined.

Do not invent 5/30/60-second requirements.

Timeouts shall be chosen after architecture/measurement.

---

# 108. Retries

Safe GET requests may be retried by clients.

Mutation retries require idempotency awareness.

Do not blindly retry:

- camera creation;
- rule creation;
- zone creation.

Acknowledgement is intentionally proposed as repeat-safe.

---

# 109. Idempotency-Key

Potential future HTTP header:

```text
Idempotency-Key
```

Status: `DEFERRED`.

Not required unless mutation duplicate issues become real.

---

# 110. Deprecation

If a baselined field/path is replaced:

1. mark deprecated;
2. update consumers;
3. maintain transition where practical;
4. remove only through coordinated version change.

---

# 111. Explicitly Forbidden Public Endpoint Pattern

Do not create:

```text
POST /api/v1/process-video
```

that synchronously:

- decodes arbitrary video;
- runs every model;
- applies rules;
- writes events;
- waits for completion;
- returns everything.

This violates the worker architecture and creates an unsafe integration boundary.

---

# 112. No Arbitrary Frontend Event Creation

There shall be no production endpoint:

```text
POST /api/v1/events
```

for ordinary frontend creation of surveillance events.

Events are created by:

- deterministic rule evaluation;
- violence criterion;
- health logic.

A test-injection endpoint, if ever used, must be internal/development-only.

---

# 113. Development Test Injection

Potential:

```text
POST /internal/test/events
```

Status: `DEFERRED / DEVELOPMENT_ONLY`.

Must not be exposed as normal production functionality.

---

# 114. API Security Review Checklist

Before baseline:

- [ ] auth selected;
- [ ] authorization matrix selected;
- [ ] protected endpoints identified;
- [ ] evidence protected;
- [ ] worker internal transport protected;
- [ ] CORS defined;
- [ ] errors safe;
- [ ] no local artifact paths exposed;
- [ ] no secrets returned;
- [ ] upload route omitted unless needed;
- [ ] debug/test routes isolated.

---

# 115. Contract Baseline Checklist

Before `BASELINED`:

- [ ] `/api/v1` accepted.
- [ ] response envelope accepted.
- [ ] error envelope accepted.
- [ ] pagination accepted.
- [ ] timestamp format accepted.
- [ ] duration unit accepted.
- [ ] camera routes accepted.
- [ ] zone routes accepted.
- [ ] rule routes accepted.
- [ ] event schema accepted.
- [ ] event context shapes accepted.
- [ ] acknowledgement route/idempotency accepted.
- [ ] evidence routes accepted.
- [ ] analytics routes accepted.
- [ ] WebSocket endpoint accepted.
- [ ] WebSocket message types accepted.
- [ ] reconnect/reconciliation accepted.
- [ ] worker logical schema accepted.
- [ ] worker transport selected or deliberately deferred.
- [ ] worker error codes accepted.
- [ ] coordinate representation accepted.
- [ ] auth selected.
- [ ] authorization matrix selected.
- [ ] no route exists merely because an AI assistant guessed it.

---

# 116. Open API Decisions

| ID | Decision | Status |
|---|---|---|
| API-OD-001 | Confirm `/api/v1` | `PROPOSED` |
| API-OD-002 | Confirm response envelope | `PROPOSED` |
| API-OD-003 | Confirm cursor pagination | `PROPOSED` |
| API-OD-004 | Default/max limit | `TBD` |
| API-OD-005 | Authentication mechanism | `TBD` |
| API-OD-006 | Role permissions | `TBD` |
| API-OD-007 | Camera source kinds | `TBD` |
| API-OD-008 | Stream/snapshot interface | `TBD` |
| API-OD-009 | Normalized geometry | `PROPOSED` |
| API-OD-010 | Intrusion position method | `TBD` |
| API-OD-011 | Rule threshold semantics | `TBD` |
| API-OD-012 | Event lifecycle/status | `TBD` |
| API-OD-013 | Evidence delivery | `TBD` |
| API-OD-014 | WebSocket endpoint | `PROPOSED` |
| API-OD-015 | WebSocket auth | `TBD` |
| API-OD-016 | Reconnect checkpoint strategy | `TBD` |
| API-OD-017 | Worker transport | `TBD` |
| API-OD-018 | Worker schema version | `PROPOSED` |
| API-OD-019 | Internal worker security | `TBD` |
| API-OD-020 | Audit API inclusion | `TBD` |

---

# 117. AI Assistant Contract Rules

Once baselined, an AI assistant shall:

1. not invent endpoint paths;
2. not rename request/response fields;
3. not add hidden client-only response fields;
4. not return ORM entities directly without schema serialization;
5. not change null semantics silently;
6. not invent new machine codes;
7. not change coordinate convention;
8. not change milliseconds to seconds without contract update;
9. not expose storage paths;
10. not add production `POST /events`;
11. not bypass worker validation;
12. not treat worker errors as successful negative inference;
13. update this document before breaking changes;
14. add/update contract tests for changed schemas.

---

# 118. Final API Rule

> **The Sentinel AI API is the boundary between independently developed components.**
>
> Once baselined, the contract is more authoritative than frontend assumptions, backend convenience, AI-worker internals, generated code, or coding-assistant suggestions.
>
> If a component needs a new field or endpoint, the correct sequence is:
>
> ```text
> requirement/design justification
> → API specification update
> → team review
> → implementation
> → contract test
> ```
>
> not:
>
> ```text
> implement first
> → force other components to adapt later
> ```
