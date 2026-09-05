---
title: "Sentinel AI — Database Design Specification"
document_id: "SEN-DB"
version: "0.1.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
database_engine: "PROPOSED: PostgreSQL"
modeling_style: "Relational, event-centric, normalized application data"
last_updated: "2026-08-20"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "logical relational model"
  - "proposed physical schema"
  - "entity definitions"
  - "keys and foreign keys"
  - "database invariants"
  - "indexes"
  - "retention/deletion behavior"
  - "migration rules"
  - "database-to-SRS traceability"
---

# Sentinel AI — Database Design Specification

> **Document purpose**
>
> This document defines the proposed relational data model for Sentinel AI.
>
> It is intentionally detailed enough that, once baselined, a backend developer or AI coding assistant can implement database models and migrations without inventing table names, columns, relationships, constraints, or lifecycle behavior.
>
> **Important status rule**
>
> The database engine is still `PROPOSED: PostgreSQL`.
>
> Therefore:
>
> - the **logical model** in this document is the primary design;
> - PostgreSQL-specific physical recommendations are explicitly labeled;
> - this document must be reviewed before its status becomes `BASELINED`;
> - no AI assistant may treat a `TBD` field, enum value, threshold, or retention rule as decided merely because this document discusses it.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for persistent application data.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `01-vision-and-scope.md`
3. `02-srs.md`
4. `03-use-case-specification.md`
5. `04-system-architecture.md`
6. accepted ADRs

The API specification shall consume this database model, not silently redefine it.

## 0.2 Database decision status

| Decision | Status |
|---|---|
| Relational database model | `PROPOSED_FOR_BASELINE` |
| PostgreSQL engine | `PROPOSED` |
| UUID-style stable identifiers | `PROPOSED` |
| UTC-aware persisted timestamps | `PROPOSED` |
| Event-centric persistence | `PROPOSED` |
| No per-frame raw-detection persistence by default | `PROPOSED` |
| Evidence binaries stored outside relational DB | `PROPOSED` |
| One event base row + event-specific context table | `PROPOSED` |
| Dedicated alert table | `NOT_RECOMMENDED_FOR_MVP` |
| Separate incident table | `TBD / NOT IN INITIAL SCHEMA` |
| Database partitioning | `DEFERRED` |

## 0.3 Design objectives

The database shall support:

- stable camera/source identities;
- zone and rule configuration;
- event persistence;
- event-specific provenance;
- model/version provenance;
- evidence metadata;
- acknowledgements;
- history/search;
- analytics;
- source health;
- optional audit records;
- future lifecycle expansion without corrupting historical records.

---

# 1. Core Data-Model Principles

## 1.1 Event-centric persistence

Sentinel processes many frames and detections.

The database should **not** become a raw frame-by-frame telemetry store in the MVP.

Preferred flow:

```text
raw frame
    ↓
AI detection / track
    ↓
rule/model qualification
    ↓
domain event
    ↓
persist event + relevant context
```

Only information needed for:

- event review;
- traceability;
- evidence;
- analytics;
- debugging;

should be retained persistently by default.

## 1.2 Configuration and history must be separable

A rule or zone may change after an event occurs.

Historical events must remain interpretable.

Therefore event-specific context must preserve enough information to explain the event even if:

- the zone geometry later changes;
- the rule threshold later changes;
- the model is replaced;
- the camera is renamed.

## 1.3 No credentials in ordinary camera columns

Camera/source credentials shall not be embedded into persisted source URI fields in plaintext.

If credentials are required, store a reference to an external secret/configuration mechanism.

## 1.4 Evidence binary separation

The relational database should store:

- evidence metadata;
- storage reference;
- integrity metadata;
- status;

not large video binaries by default.

## 1.5 Append/history over destructive mutation

For audit-sensitive information, prefer:

- append records;
- explicit state transitions;
- disable/deactivate;

over destructive deletion.

---

# 2. Proposed Logical Entity Catalogue

## 2.1 Identity and authorization

- `users`
- `roles`
- `user_roles`

Optional future:

- `permissions`
- `role_permissions`

## 2.2 Camera and monitoring configuration

- `cameras`
- `camera_health_history`
- `zones`
- `zone_vertices`
- `rules`
- `intrusion_rule_config`
- `loitering_rule_config`
- `crowd_rule_config`
- `camera_health_policies`
- `violence_event_policies`

## 2.3 Event and operator workflow

- `events`
- `intrusion_event_context`
- `loitering_event_context`
- `crowd_event_context`
- `violence_event_context`
- `camera_offline_event_context`
- `event_acknowledgements`
- `event_status_history` — `TBD`
- `event_feedback` — `PROPOSED`

## 2.4 Evidence

- `evidence_items`

## 2.5 AI provenance

- `models`
- `model_versions`

## 2.6 Audit

- `audit_log` — `PROPOSED`

## 2.7 Explicitly omitted from initial schema

- raw video-frame table;
- every-frame detection table;
- every-frame track table;
- biometric identity table;
- face embedding table;
- notification delivery table for SMS/email;
- multi-site hierarchy;
- enterprise tenancy tables.

---

# 3. Proposed Entity Relationship Model

```mermaid
erDiagram
    USERS ||--o{ USER_ROLES : assigned
    ROLES ||--o{ USER_ROLES : grants

    CAMERAS ||--o{ ZONES : contains
    ZONES ||--o{ ZONE_VERTICES : composed_of

    CAMERAS ||--o{ RULES : evaluates_on
    ZONES ||--o{ RULES : optionally_scopes

    RULES ||--o| INTRUSION_RULE_CONFIG : configures
    RULES ||--o| LOITERING_RULE_CONFIG : configures
    RULES ||--o| CROWD_RULE_CONFIG : configures

    CAMERAS ||--o| CAMERA_HEALTH_POLICIES : health_policy
    CAMERAS ||--o{ VIOLENCE_EVENT_POLICIES : violence_policy

    MODELS ||--o{ MODEL_VERSIONS : versions
    MODEL_VERSIONS ||--o{ VIOLENCE_EVENT_POLICIES : selected_model

    CAMERAS ||--o{ EVENTS : produces
    RULES ||--o{ EVENTS : may_trigger

    EVENTS ||--o| INTRUSION_EVENT_CONTEXT : has
    EVENTS ||--o| LOITERING_EVENT_CONTEXT : has
    EVENTS ||--o| CROWD_EVENT_CONTEXT : has
    EVENTS ||--o| VIOLENCE_EVENT_CONTEXT : has
    EVENTS ||--o| CAMERA_OFFLINE_EVENT_CONTEXT : has

    MODEL_VERSIONS ||--o{ VIOLENCE_EVENT_CONTEXT : produced_by

    EVENTS ||--o{ EVIDENCE_ITEMS : has
    EVENTS ||--o{ EVENT_ACKNOWLEDGEMENTS : acknowledged_by
    USERS ||--o{ EVENT_ACKNOWLEDGEMENTS : creates

    EVENTS ||--o{ EVENT_STATUS_HISTORY : transitions
    USERS ||--o{ EVENT_STATUS_HISTORY : may_initiate

    EVENTS ||--o{ EVENT_FEEDBACK : receives
    USERS ||--o{ EVENT_FEEDBACK : submits

    USERS ||--o{ AUDIT_LOG : acts
```

---

# 4. Identifier Strategy

## 4.1 Preferred identifier type

**Logical type:** UUID

Status: `PROPOSED`.

Reasons:

- stable across distributed components;
- safe for frontend/API references;
- avoids exposing sequential record counts;
- worker/backend correlation can use same identifier family.

## 4.2 Generation

The final implementation may generate UUIDs:

- application-side; or
- database-side.

Exact generation mechanism shall be selected with the database engine.

## 4.3 Identifier invariants

1. Primary IDs are immutable.
2. Display names are not identifiers.
3. Camera names may change without changing camera ID.
4. Event IDs never change.
5. Model-version IDs never change.

---

# 5. Timestamp Strategy

## 5.1 Proposed policy

Persist timestamps as UTC-aware instants.

For PostgreSQL:

```text
TIMESTAMPTZ
```

is recommended.

## 5.2 Required timestamp distinctions

Do not collapse the following into one ambiguous timestamp:

- frame/source time;
- event occurrence time;
- row creation time;
- row update time;
- acknowledgement time;
- model window start/end;
- camera health transition time.

## 5.3 Naming convention

Use explicit suffixes:

```text
occurred_at
created_at
updated_at
acknowledged_at
window_started_at
window_ended_at
last_frame_at
disabled_at
deleted_at
```

Avoid generic:

```text
timestamp
date
time
```

when semantics matter.

---

# 6. Common Column Conventions

## 6.1 Audit timestamps

Configuration entities should generally contain:

```text
created_at
updated_at
```

## 6.2 Soft deactivation

Operational configuration should prefer:

```text
enabled BOOLEAN
```

or:

```text
disabled_at
```

rather than hard deletion when historical events may reference it.

## 6.3 Soft deletion

Use `deleted_at` only where a real delete concept is necessary.

Do not add soft deletion to every table automatically.

## 6.4 Boolean naming

Use positive meaning where possible:

```text
enabled
requires_attention
```

Avoid confusing negatives such as:

```text
not_disabled
```

---

# 7. Table: `users`

**Status:** `PROPOSED`

Purpose:

Represent a human application user independently from the exact authentication mechanism.

## 7.1 Proposed columns

| Column | Logical type | Null | Constraint / Meaning |
|---|---|---:|---|
| `id` | UUID | No | Primary key |
| `display_name` | String | No | Human-readable name |
| `login_name` | String | Yes | Unique local login identifier if used |
| `auth_subject` | String | Yes | External/token identity subject if used |
| `email` | String | Yes | Optional identity/contact attribute |
| `enabled` | Boolean | No | Default true |
| `created_at` | Timestamp | No | Creation instant |
| `updated_at` | Timestamp | No | Last metadata update |
| `disabled_at` | Timestamp | Yes | Optional disable instant |

## 7.2 Constraints

At least one selected authentication identity field must be present after auth strategy is baselined.

Possible:

```text
login_name
```

or:

```text
auth_subject
```

Do not require both until auth mechanism is selected.

## 7.3 Intentionally excluded

- plaintext password;
- detected-person identity;
- face embedding;
- biometric profile.

If local password auth is selected, password credential storage shall be designed separately and never store plaintext.

---

# 8. Table: `roles`

**Status:** `PROPOSED`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `code` | String | No | Unique stable role code |
| `name` | String | No | Display label |
| `description` | String/Text | Yes | Role meaning |
| `created_at` | Timestamp | No | Creation |

Candidate role codes are not yet baselined.

Potential:

```text
administrator
operator
reviewer
```

---

# 9. Table: `user_roles`

**Status:** `PROPOSED`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `user_id` | UUID | No | FK → users |
| `role_id` | UUID | No | FK → roles |
| `assigned_at` | Timestamp | No | Assignment time |
| `assigned_by_user_id` | UUID | Yes | FK → users |

Primary key / unique:

```text
(user_id, role_id)
```

---

# 10. Table: `cameras`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Represent a configured Sentinel video source.

## 10.1 Columns

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `name` | String | No | User-visible camera/source name |
| `description` | Text | Yes | Optional description |
| `source_kind` | String | No | Input type code; values TBD |
| `source_locator` | Text | No | File/stream/device locator without embedded secrets |
| `credential_ref` | String | Yes | Reference to external credential/config source |
| `enabled` | Boolean | No | Whether processing is intentionally enabled |
| `health_state_code` | String | No | Current health state |
| `last_frame_at` | Timestamp | Yes | Last valid frame timestamp observed by system |
| `last_health_check_at` | Timestamp | Yes | Last health evaluation |
| `created_at` | Timestamp | No | Creation |
| `updated_at` | Timestamp | No | Last config update |
| `disabled_at` | Timestamp | Yes | Intentional disable time |

## 10.2 Constraints

- `name` should be unique within the project unless team decides otherwise.
- `source_locator` shall not contain plaintext credentials.
- disabled and offline are different concepts.
- `health_state_code` values are not baselined yet.

## 10.3 Candidate health states

`PROPOSED`:

```text
unknown
healthy
degraded
offline
```

Intentional disable is represented by `enabled = false`, not necessarily by `health_state_code`.

---

# 11. Table: `camera_health_history`

**Status:** `PROPOSED`

Purpose:

Preserve source-health transitions for audit/analytics without storing every health poll.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `camera_id` | UUID | No | FK → cameras |
| `from_state_code` | String | Yes | Previous state |
| `to_state_code` | String | No | New state |
| `reason_code` | String | Yes | Why transition occurred |
| `observed_at` | Timestamp | No | Transition time |
| `correlation_id` | UUID/String | Yes | Diagnostic correlation |

Do not write one row per health heartbeat.

Write a row only when relevant state changes.

---

# 12. Table: `zones`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Represent a logical monitoring region tied to one camera/source.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `camera_id` | UUID | No | FK → cameras |
| `name` | String | No | Zone label |
| `zone_kind` | String | No | Restricted/monitored/counting etc.; values TBD |
| `enabled` | Boolean | No | Whether zone is active |
| `geometry_version` | Integer | No | Incremented on geometry change |
| `created_at` | Timestamp | No | Creation |
| `updated_at` | Timestamp | No | Last update |
| `disabled_at` | Timestamp | Yes | Optional disable time |

## 12.1 Unique constraint

Recommended:

```text
UNIQUE(camera_id, name)
```

## 12.2 Geometry representation

A zone's polygon vertices are stored in `zone_vertices`.

This avoids opaque geometry JSON for the MVP and enables clear validation.

---

# 13. Table: `zone_vertices`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Store ordered polygon vertices.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `zone_id` | UUID | No | FK → zones |
| `vertex_index` | Integer | No | Ordered vertex position |
| `x_norm` | Decimal | No | Horizontal normalized coordinate |
| `y_norm` | Decimal | No | Vertical normalized coordinate |

Primary key:

```text
(zone_id, vertex_index)
```

## 13.1 Proposed coordinate strategy

Normalized coordinate space:

```text
0.0 <= x_norm <= 1.0
0.0 <= y_norm <= 1.0
```

Status: `PROPOSED`.

Advantages:

- independent of display scaling;
- independent of resolution;
- easy frontend rendering.

Before baseline, confirm this against the zone editor.

## 13.2 Polygon constraints

Database can enforce:

- coordinate range;
- unique index per zone.

Application/domain layer must additionally validate:

- minimum vertex count;
- polygon validity;
- self-intersection policy.

---

# 14. Table: `rules`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Base record for deterministic event rules.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `camera_id` | UUID | No | FK → cameras |
| `zone_id` | UUID | Yes | FK → zones |
| `rule_type_code` | String | No | Intrusion / loitering / crowd |
| `name` | String | No | Rule display name |
| `enabled` | Boolean | No | Active evaluation |
| `version` | Integer | No | Configuration version |
| `created_at` | Timestamp | No | Creation |
| `updated_at` | Timestamp | No | Modification |
| `disabled_at` | Timestamp | Yes | Disable time |

## 14.1 Rule type codes

Proposed fixed MVP values:

```text
restricted_area_intrusion
loitering
crowd_threshold
```

Violence and camera-offline policy are intentionally separated into dedicated policy tables.

## 14.2 Constraints

- rule camera must match zone camera when `zone_id` is present;
- exactly one subtype config row should exist for each rule;
- subtype must match `rule_type_code`.

Cross-table subtype consistency is primarily an application/migration invariant unless implemented with database triggers.

Avoid complex triggers in MVP unless clearly justified.

---

# 15. Table: `intrusion_rule_config`

**Status:** `PROPOSED`

One-to-one with `rules`.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `rule_id` | UUID | No | PK/FK → rules |
| `position_method_code` | String | No | Point/geometry method; TBD |
| `require_transition_from_outside` | Boolean | No | Entry semantic |
| `cooldown_ms` | Integer/BigInt | Yes | Duplicate/retrigger interval |
| `created_at` | Timestamp | No | Creation/update record time |

## 15.1 Unresolved fields

The exact default values remain `TBD`.

No migration shall invent values merely to satisfy non-null constraints.

During draft stage, either:

- keep unresolved fields nullable; or
- do not create migration until values are baselined.

---

# 16. Table: `loitering_rule_config`

**Status:** `PROPOSED`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `rule_id` | UUID | No | PK/FK |
| `dwell_threshold_ms` | BigInt | No after baseline | Required duration |
| `track_loss_grace_ms` | BigInt | Yes | Optional grace |
| `reset_on_exit` | Boolean | No after baseline | Timer behavior |
| `retrigger_after_ms` | BigInt | Yes | Duplicate policy |
| `created_at` | Timestamp | No | Created |

Constraints:

```text
dwell_threshold_ms > 0
track_loss_grace_ms >= 0
retrigger_after_ms >= 0
```

when fields are non-null.

---

# 17. Table: `crowd_rule_config`

**Status:** `PROPOSED`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `rule_id` | UUID | No | PK/FK |
| `person_threshold` | Integer | No after baseline | Threshold |
| `counting_method_code` | String | No after baseline | Tracks/detections; TBD |
| `retrigger_after_ms` | BigInt | Yes | Duplicate policy |
| `created_at` | Timestamp | No | Created |

Constraints:

```text
person_threshold > 0
retrigger_after_ms >= 0
```

---

# 18. Table: `camera_health_policies`

**Status:** `PROPOSED`

Purpose:

Define camera-offline criteria separately from normal rule configuration.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `camera_id` | UUID | No | PK/FK → cameras |
| `offline_after_ms` | BigInt | No after baseline | Missing-frame/failure duration |
| `health_check_interval_ms` | BigInt | Yes | Evaluation interval |
| `enabled` | Boolean | No | Policy active |
| `created_at` | Timestamp | No | Created |
| `updated_at` | Timestamp | No | Updated |

Exact values remain `TBD`.

---

# 19. Table: `models`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Represent a logical AI model family/task.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `name` | String | No | Stable model name |
| `task_code` | String | No | person_detection / violence_fighting |
| `source_name` | String | Yes | Original framework/provider/project |
| `source_url` | Text | Yes | Official provenance URL |
| `license_name` | String | Yes | Recorded license |
| `created_at` | Timestamp | No | Registry creation |

Unique recommendation:

```text
UNIQUE(name, task_code)
```

---

# 20. Table: `model_versions`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Represent immutable deployable model version metadata.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `model_id` | UUID | No | FK → models |
| `version_label` | String | No | Human/version identifier |
| `artifact_reference` | Text | No | Controlled file/storage reference |
| `artifact_sha256` | String(64) | Yes | Integrity checksum |
| `framework_name` | String | Yes | e.g. PyTorch |
| `framework_version` | String | Yes | Runtime version |
| `base_model_reference` | Text | Yes | Pretrained source/base |
| `dataset_registry_id` | String | Yes | ID from dataset registry document |
| `training_commit` | String | Yes | Git commit for trained/fine-tuned artifact |
| `status_code` | String | No | experimental/approved/retired; values TBD |
| `created_at` | Timestamp | No | Registry time |

Unique:

```text
UNIQUE(model_id, version_label)
```

## 20.1 Immutability

Once a model version is used to generate a persisted event:

- its identity/provenance fields should not be rewritten to describe a different artifact;
- a new artifact should create a new version row.

---

# 21. Table: `violence_event_policies`

**Status:** `PROPOSED`

Purpose:

Map a camera or global application policy to a selected violence model/version and event threshold.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `camera_id` | UUID | Yes | FK → cameras; null may mean global if accepted |
| `model_version_id` | UUID | No | FK → model_versions |
| `enabled` | Boolean | No | Policy active |
| `event_threshold_value` | Double/Decimal | No after baseline | Event criterion |
| `score_semantics` | String | Yes | Meaning of model score |
| `cooldown_ms` | BigInt | Yes | Event duplicate policy |
| `created_at` | Timestamp | No | Created |
| `updated_at` | Timestamp | No | Updated |

## 21.1 Constraint caution

Do not assume the score is a calibrated probability.

The column is called:

```text
event_threshold_value
```

not:

```text
probability_threshold
```

---

# 22. Table: `events`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Store every accepted domain event.

## 22.1 Columns

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `event_type_code` | String | No | Primary event taxonomy |
| `camera_id` | UUID | No | FK → cameras |
| `rule_id` | UUID | Yes | FK → rules if deterministic rule event |
| `occurred_at` | Timestamp | No | Event occurrence instant |
| `created_at` | Timestamp | No | Persistence creation time |
| `severity_code` | String | Yes | Severity if baselined |
| `requires_attention` | Boolean | No | Whether operator alert projection applies |
| `lifecycle_status_code` | String | Yes | `TBD` until event state model accepted |
| `correlation_id` | UUID/String | Yes | Cross-component trace |
| `summary` | String/Text | Yes | Optional generated operator summary |

## 22.2 Proposed event types

```text
restricted_area_intrusion
loitering
crowd_threshold
violence_fighting
camera_offline
```

## 22.3 Alert representation decision

**Proposed MVP decision: no dedicated `alerts` table.**

Rationale:

An alert is an operator-facing projection of an event that:

```text
requires_attention = true
```

and has acknowledgement/lifecycle state.

Advantages:

- avoids duplicate event/alert state;
- simpler 2–3 week architecture;
- no ambiguous one-to-one alert relationship;
- real-time transport can publish event state directly.

If future notification deliveries are added, separate delivery tables may be introduced.

## 22.4 Event immutability

Core facts should be treated as immutable after creation:

- type;
- camera;
- occurrence time;
- originating rule;
- event-specific observed context.

Mutable workflow state should live in:

- acknowledgement records;
- event-status history;
- feedback/review records.

---

# 23. Table: `intrusion_event_context`

**Status:** `PROPOSED_FOR_BASELINE`

One-to-one with intrusion event.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `event_id` | UUID | No | PK/FK → events |
| `rule_id` | UUID | No | FK → rules |
| `zone_id` | UUID | No | FK → zones |
| `zone_geometry_version` | Integer | No | Zone version at event |
| `track_id` | String | Yes | Temporary tracker identifier |
| `position_x_norm` | Decimal | Yes | Trigger position |
| `position_y_norm` | Decimal | Yes | Trigger position |
| `position_method_code` | String | No | Geometry method used |
| `cooldown_ms_snapshot` | BigInt | Yes | Rule value at event |

This table snapshots relevant event facts.

---

# 24. Table: `loitering_event_context`

**Status:** `PROPOSED_FOR_BASELINE`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `event_id` | UUID | No | PK/FK |
| `rule_id` | UUID | No | Origin rule |
| `zone_id` | UUID | No | Origin zone |
| `zone_geometry_version` | Integer | No | Geometry version |
| `track_id` | String | Yes | Temporary track |
| `dwell_duration_ms` | BigInt | No | Observed qualifying duration |
| `threshold_ms_snapshot` | BigInt | No | Threshold used |
| `track_loss_grace_ms_snapshot` | BigInt | Yes | Grace used |
| `retrigger_ms_snapshot` | BigInt | Yes | Retrigger rule value |

---

# 25. Table: `crowd_event_context`

**Status:** `PROPOSED_FOR_BASELINE`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `event_id` | UUID | No | PK/FK |
| `rule_id` | UUID | No | Origin rule |
| `zone_id` | UUID | Yes | Zone if scoped |
| `zone_geometry_version` | Integer | Yes | Geometry version |
| `observed_count` | Integer | No | Person count |
| `threshold_count_snapshot` | Integer | No | Threshold used |
| `counting_method_code` | String | No | Tracks/detections etc. |

Constraints:

```text
observed_count >= 0
threshold_count_snapshot > 0
```

---

# 26. Table: `violence_event_context`

**Status:** `PROPOSED_FOR_BASELINE`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `event_id` | UUID | No | PK/FK |
| `model_version_id` | UUID | No | FK → model_versions |
| `output_label` | String | No | Model classification label |
| `score_value` | Double/Decimal | Yes | Raw/deployed score |
| `event_threshold_snapshot` | Double/Decimal | Yes | Threshold used |
| `score_semantics` | String | Yes | Interpretation |
| `window_started_at` | Timestamp | Yes | Temporal input start |
| `window_ended_at` | Timestamp | Yes | Temporal input end |

## 26.1 Important rule

Do not rename `score_value` to `probability` unless the selected model explicitly produces a calibrated probability and the team documents that fact.

---

# 27. Table: `camera_offline_event_context`

**Status:** `PROPOSED_FOR_BASELINE`

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `event_id` | UUID | No | PK/FK |
| `camera_id` | UUID | No | FK → cameras |
| `last_frame_at` | Timestamp | Yes | Last valid frame before offline |
| `offline_after_ms_snapshot` | BigInt | Yes | Policy threshold used |
| `reason_code` | String | Yes | Failure classification |
| `health_state_before` | String | Yes | Prior state |
| `health_state_after` | String | No | Offline state code |

---

# 28. Table: `evidence_items`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Represent snapshot/clip artifacts associated with events.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `event_id` | UUID | No | FK → events |
| `evidence_type_code` | String | No | snapshot / clip |
| `status_code` | String | No | pending / available / failed / deleted; values proposed |
| `storage_backend_code` | String | No | local/object/etc. |
| `storage_key` | Text | Yes | Controlled artifact reference |
| `mime_type` | String | Yes | e.g. image/jpeg, video/mp4 |
| `size_bytes` | BigInt | Yes | Artifact size |
| `sha256` | String(64) | Yes | Integrity checksum |
| `capture_started_at` | Timestamp | Yes | Media time range start |
| `capture_ended_at` | Timestamp | Yes | Media time range end |
| `created_at` | Timestamp | No | Metadata creation |
| `available_at` | Timestamp | Yes | Artifact ready |
| `deleted_at` | Timestamp | Yes | Media deletion |
| `failure_code` | String | Yes | Failure category |
| `failure_detail` | Text | Yes | Safe diagnostic text |

## 28.1 Constraints

If:

```text
status_code = available
```

then `storage_key` should be non-null.

If:

```text
status_code = failed
```

then `failure_code` should normally be non-null.

These cross-field rules may be enforced in application validation and optionally database checks.

## 28.2 Security

`storage_key` is not a public URL by definition.

Frontend access should pass through authorized media resolution.

---

# 29. Table: `event_acknowledgements`

**Status:** `PROPOSED_FOR_BASELINE`

Purpose:

Persist operator acknowledgement without overwriting core event facts.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `event_id` | UUID | No | FK → events |
| `user_id` | UUID | No | FK → users |
| `acknowledged_at` | Timestamp | No | Server-trusted acknowledgement time |
| `comment` | Text | Yes | Optional note |
| `correlation_id` | UUID/String | Yes | Request trace |

## 29.1 Unique policy

Proposed:

```text
UNIQUE(event_id, user_id)
```

This permits multiple authorized users to acknowledge the same event, but prevents duplicate acknowledgement records from the same user.

## 29.2 Derived event acknowledgement

An event may be considered:

```text
acknowledged = EXISTS(event_acknowledgements WHERE event_id = ...)
```

This avoids mutating an `acknowledged` boolean on the event row.

If the team wants exactly one global acknowledgement, this design can be tightened during baseline.

---

# 30. Table: `event_status_history`

**Status:** `TBD`

Create this table only if the team baselines a richer event lifecycle.

Proposed structure:

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `event_id` | UUID | No | FK |
| `from_status_code` | String | Yes | Previous status |
| `to_status_code` | String | No | New status |
| `changed_by_user_id` | UUID | Yes | Null for system transition |
| `changed_at` | Timestamp | No | Transition time |
| `reason` | Text | Yes | Optional reason |

Candidate statuses remain `TBD`.

Do not seed:

```text
OPEN
ACKNOWLEDGED
INVESTIGATING
RESOLVED
FALSE_POSITIVE
```

until lifecycle is formally accepted.

---

# 31. Table: `event_feedback`

**Status:** `PROPOSED / OPTIONAL_MVP`

Purpose:

Store human review such as false-positive feedback.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `event_id` | UUID | No | FK |
| `user_id` | UUID | No | FK |
| `feedback_code` | String | No | e.g. false_positive; values TBD |
| `reason_code` | String | Yes | Structured reason |
| `notes` | Text | Yes | Reviewer note |
| `created_at` | Timestamp | No | Submission time |

This is **human feedback**, not automatically trusted ML ground truth.

---

# 32. Table: `audit_log`

**Status:** `PROPOSED`

Purpose:

Append security/workflow-sensitive application actions.

| Column | Type | Null | Meaning |
|---|---|---:|---|
| `id` | UUID | No | PK |
| `actor_user_id` | UUID | Yes | FK → users; null for system |
| `action_code` | String | No | Stable action identifier |
| `entity_type_code` | String | Yes | Target type |
| `entity_id` | UUID/String | Yes | Target ID |
| `outcome_code` | String | No | success/denied/failed etc. |
| `occurred_at` | Timestamp | No | Server time |
| `correlation_id` | UUID/String | Yes | Request/process trace |
| `metadata_json` | JSON/Object | Yes | Non-sensitive structured context |

## 32.1 Audit constraints

Do not store:

- passwords;
- tokens;
- camera credentials;
- raw frames.

`metadata_json` is for supplemental diagnostic context, not uncontrolled dumping of request bodies.

---

# 33. Optional Table: `processing_jobs`

**Status:** `DEFERRED_UNTIL_WORKER_TRANSPORT_SELECTED`

Only create if backend/worker architecture is job-oriented and persistence is useful.

Potential fields:

```text
id
correlation_id
camera_id
job_type_code
model_version_id
status_code
submitted_at
started_at
completed_at
error_code
```

Do not persist one job per frame if that would create unnecessary high-volume data.

---

# 34. Decision: No Raw Detection Table in MVP

**Status:** `PROPOSED`

The MVP should not persist every frame's person detections.

Reasons:

- very high row volume;
- little value for core operator workflow;
- increased retention/privacy burden;
- slower academic implementation;
- analytics requirements focus on events.

Relevant event-specific detection context is copied into event context tables.

If later research requires detector analytics, add a separate sampled/telemetry design.

---

# 35. Decision: No Persistent Track Table in MVP

**Status:** `PROPOSED`

Tracks are operational/transient.

Persist only event-relevant:

```text
track_id
```

inside event context.

Reason:

Track identity is temporary and not a real-world identity.

---

# 36. Decision: No Dedicated Alert Table in MVP

**Status:** `PROPOSED`

Alert is modeled as an application projection of an event.

A query can derive:

```text
events
WHERE requires_attention = true
```

plus:

- acknowledgements;
- lifecycle state;
- evidence.

Benefits:

- less duplicated state;
- fewer race conditions;
- simpler UI/backend contract.

Future SMS/email deliveries would justify separate delivery records.

---

# 37. Decision: No Separate Incident Table Initially

**Status:** `TBD / OMITTED_FROM_INITIAL_SCHEMA`

The project currently needs:

- event;
- acknowledgement;
- history;
- evidence.

The exact `event` vs `incident` relationship is unresolved.

Therefore the database shall **not invent an incidents table** until the SRS/use-case domain model defines:

- one event = one incident;
- multiple events grouped into one incident;
- or incident as workflow state.

---

# 38. Referential Integrity Rules

## 38.1 Camera references

Historical events must not be invalidated if a camera is disabled.

Prefer:

- disable camera;
- retain row.

Hard deletion of a camera with historical events should be blocked.

## 38.2 Zone references

Zones referenced by events/rules should not be hard-deleted casually.

Prefer:

- disable;
- version/update.

## 38.3 Rule references

Rules that generated events should remain addressable.

Disable rather than hard delete.

## 38.4 Model-version references

Model versions referenced by events are immutable provenance.

Do not delete or rewrite them casually.

## 38.5 User references

Users with acknowledgement/audit history should be disabled rather than hard-deleted.

---

# 39. Proposed Foreign-Key Deletion Actions

| Relationship | Proposed action |
|---|---|
| `zones.camera_id → cameras.id` | `RESTRICT` |
| `zone_vertices.zone_id → zones.id` | `CASCADE` only for pre-history hard delete |
| `rules.camera_id → cameras.id` | `RESTRICT` |
| `rules.zone_id → zones.id` | `RESTRICT` |
| `events.camera_id → cameras.id` | `RESTRICT` |
| `events.rule_id → rules.id` | `RESTRICT` or nullable only for non-rule events |
| event context → event | `CASCADE` if event is legitimately hard-deleted |
| evidence → event | `CASCADE` metadata only; physical media requires separate cleanup |
| acknowledgement → event | `CASCADE` only if event hard delete is explicitly permitted |
| acknowledgement → user | `RESTRICT` |
| model_versions → models | `RESTRICT` |
| violence_event_context → model_version | `RESTRICT` |

Because event hard deletion is not normal MVP behavior, cascades are safety mechanisms rather than normal workflow.

---

# 40. Event Context Invariant

For each event:

```text
event_type_code
```

must match exactly one appropriate context table.

Example:

```text
restricted_area_intrusion
→ exactly one intrusion_event_context
→ no loitering_event_context
→ no crowd_event_context
→ no violence_event_context
```

Application service shall enforce this invariant transactionally.

Database trigger enforcement is optional and not recommended unless necessary.

---

# 41. Event Creation Transaction

Proposed transaction:

```text
BEGIN

insert events
insert matching event_context
insert evidence pending metadata if required
insert audit/system context if required

COMMIT
```

Real-time notification should occur **after successful commit**.

Do not notify frontend of an event that later fails to persist.

---

# 42. Acknowledgement Transaction

Proposed:

```text
BEGIN

validate event
insert event_acknowledgements
optional insert audit_log
optional event lifecycle transition

COMMIT
```

Repeated same-user acknowledgement should resolve deterministically via:

- pre-check; or
- unique constraint + idempotent handling.

---

# 43. Evidence Creation Transaction Boundary

Physical media storage cannot always be part of the relational DB transaction.

Recommended workflow:

```text
1. event committed
2. evidence_items row = pending
3. media encode/write
4. if success:
       update evidence_items = available
   if failure:
       update evidence_items = failed
```

This supports explicit evidence failure without rolling back the event.

---

# 44. Camera Health Persistence

Do not store every heartbeat.

Persist:

- current health fields on `cameras`;
- state transitions in `camera_health_history`;
- offline domain events in `events`.

This supports:

- dashboard current state;
- health analytics;
- event history;

without heartbeat data explosion.

---

# 45. Zone Versioning Strategy

## 45.1 Proposed simple MVP design

`zones.geometry_version` increments whenever geometry changes.

Event context stores:

```text
zone_geometry_version
```

This identifies which zone version applied.

## 45.2 Stronger historical option

If exact old geometry must be reconstructible:

create:

```text
zone_geometry_versions
zone_geometry_version_vertices
```

Status: `DEFERRED_UNLESS_REQUIRED`.

For MVP, event-level trigger coordinates + geometry version may be sufficient if changes are rare and old zone screenshots/evidence exist.

This decision should be revisited before final baseline.

---

# 46. Rule Versioning Strategy

`rules.version` increments on material rule configuration change.

Event context snapshots the critical values:

- threshold;
- cooldown;
- counting method;
- dwell duration;
- geometry method.

This prevents later rule edits from changing the explanation of old events.

---

# 47. Model Provenance Strategy

Every violence event records:

```text
model_version_id
```

and relevant deployed threshold/output.

The model registry row records:

- source;
- license;
- artifact;
- hash;
- dataset registry reference;
- training commit.

This allows:

```text
event
→ exact model version
→ exact artifact provenance
```

---

# 48. Evidence Integrity Strategy

Recommended metadata:

```text
size_bytes
sha256
mime_type
storage_key
```

Benefits:

- detect missing/replaced files;
- verify demo artifacts;
- support future migration.

Checksum generation may be omitted only if implementation time is constrained and the limitation is documented.

---

# 49. Normalization Strategy

## 49.1 Target

Approximately Third Normal Form for core application data.

## 49.2 Intentional denormalization

Event context snapshots threshold/config values intentionally duplicate current rule configuration.

This is **historical denormalization**, not accidental duplication.

Rationale:

Old events must remain interpretable after configuration changes.

---

# 50. JSON Usage Policy

Use structured relational columns for:

- event types;
- source IDs;
- rule thresholds;
- counts;
- model IDs;
- evidence state.

JSON may be used for:

- optional audit metadata;
- truly extensible non-core diagnostics.

Do not place the entire event payload into one JSON column as the primary data model.

---

# 51. String Code vs Database Enum Policy

**Proposed MVP recommendation: use string codes with application validation and/or lookup/check constraints rather than PostgreSQL ENUM types.**

Reasons:

- easier migrations during rapidly changing academic project;
- event lifecycle is not fully baselined;
- fewer irreversible schema decisions.

Example:

```text
event_type_code VARCHAR(...)
```

with a CHECK constraint once values are stable.

If PostgreSQL ENUMs are later chosen, record that in an ADR.

---

# 52. Proposed PostgreSQL Type Mapping

If PostgreSQL is confirmed:

| Logical type | PostgreSQL type |
|---|---|
| UUID | `UUID` |
| String | `VARCHAR(n)` or `TEXT` |
| Text | `TEXT` |
| Boolean | `BOOLEAN` |
| Timestamp | `TIMESTAMPTZ` |
| Integer | `INTEGER` |
| BigInt duration | `BIGINT` |
| Decimal coordinate | `NUMERIC(8,7)` |
| Raw score | `DOUBLE PRECISION` |
| JSON/Object | `JSONB` |

## 52.1 Coordinate precision

`NUMERIC(8,7)` supports normalized values with sufficient precision.

CHECK:

```sql
CHECK (x_norm >= 0 AND x_norm <= 1)
```

---

# 53. Proposed Primary Indexes

## 53.1 Events

```text
PK events(id)
INDEX events(occurred_at DESC)
INDEX events(camera_id, occurred_at DESC)
INDEX events(event_type_code, occurred_at DESC)
INDEX events(requires_attention, occurred_at DESC)
```

If lifecycle status is baselined:

```text
INDEX events(lifecycle_status_code, occurred_at DESC)
```

## 53.2 Zones

```text
INDEX zones(camera_id, enabled)
UNIQUE zones(camera_id, name)
```

## 53.3 Rules

```text
INDEX rules(camera_id, enabled)
INDEX rules(zone_id, enabled)
```

## 53.4 Evidence

```text
INDEX evidence_items(event_id)
INDEX evidence_items(status_code)
```

## 53.5 Acknowledgements

```text
INDEX event_acknowledgements(event_id)
INDEX event_acknowledgements(user_id, acknowledged_at DESC)
UNIQUE(event_id, user_id)
```

## 53.6 Health history

```text
INDEX camera_health_history(camera_id, observed_at DESC)
```

## 53.7 Audit

```text
INDEX audit_log(occurred_at DESC)
INDEX audit_log(actor_user_id, occurred_at DESC)
INDEX audit_log(entity_type_code, entity_id)
```

---

# 54. Search Query Support

The SRS requires history filtering by:

- time;
- type;
- camera;
- acknowledgement/status where baselined.

The indexes above are chosen specifically for those access paths.

Do not add indexes only because a column exists.

---

# 55. Analytics Query Support

MVP analytics should be computable directly from `events` and acknowledgement data.

Examples:

## 55.1 Events by type

```sql
SELECT event_type_code, COUNT(*)
FROM events
WHERE occurred_at >= :start
  AND occurred_at < :end
GROUP BY event_type_code;
```

## 55.2 Events by camera

```sql
SELECT camera_id, COUNT(*)
FROM events
WHERE occurred_at >= :start
  AND occurred_at < :end
GROUP BY camera_id;
```

## 55.3 Acknowledged events

Conceptually:

```sql
SELECT COUNT(DISTINCT event_id)
FROM event_acknowledgements
WHERE acknowledged_at >= :start
  AND acknowledged_at < :end;
```

Final SQL may differ by DB/framework.

---

# 56. Pagination

Event history shall be bounded.

Recommended API/database approach:

**cursor/keyset pagination** by:

```text
(occurred_at, id)
```

Status: `PROPOSED`.

Advantages:

- stable for descending event feed;
- avoids large `OFFSET` cost.

For small academic data, offset pagination is simpler and acceptable if documented.

Decision belongs in API specification.

---

# 57. Severity

`events.severity_code` is optional until severity rules are defined.

Do not seed arbitrary:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

unless the team defines:

- meaning;
- mapping per event type;
- UI behavior.

It is acceptable to leave severity `NULL` in early MVP.

---

# 58. Event Summary

`events.summary` may contain a human-readable generated summary such as:

```text
Restricted-area intrusion detected on Camera 03
```

It shall not be the only source of event facts.

The structured columns remain authoritative.

---

# 59. Camera Source Security

`cameras.source_locator` must not contain plaintext embedded credentials such as:

```text
rtsp://username:password@host/...
```

Preferred:

```text
source_locator = rtsp://host/...
credential_ref = CAMERA_03_RTSP_SECRET
```

The exact secret storage mechanism is outside the database model.

---

# 60. Data Retention

## 60.1 Event retention

`TBD`.

For an academic MVP, events may remain for the duration of the project/demo unless the team establishes a shorter policy.

## 60.2 Evidence retention

`TBD`.

Evidence deletion must update:

```text
evidence_items.status_code
deleted_at
```

and remove/expire the physical artifact according to storage policy.

## 60.3 Audit retention

`TBD`.

## 60.4 Raw video retention

Sentinel is not intended as a full archival CCTV recorder.

Long-term raw video storage is outside initial relational design.

---

# 61. Deletion Policy

## 61.1 Users

Prefer disable.

## 61.2 Cameras

Prefer disable.

Hard delete only if:

- no historical event/config dependencies; or
- controlled development reset.

## 61.3 Zones

Prefer disable.

## 61.4 Rules

Prefer disable.

## 61.5 Events

No ordinary user hard-delete feature in MVP unless explicitly required.

## 61.6 Evidence

May be deleted according to retention while preserving evidence metadata/status.

---

# 62. Concurrency Rules

## 62.1 Event duplicate races

If two processing results attempt to create the same logical event concurrently, duplicate suppression should use:

- rule state;
- transaction;
- optional uniqueness key.

Exact uniqueness key depends on event semantics.

## 62.2 Acknowledgement races

Use:

```text
UNIQUE(event_id, user_id)
```

or equivalent to prevent duplicate same-user acknowledgements.

## 62.3 Rule updates

Rule update should use:

- transaction;
- updated version;
- optionally optimistic version check.

A rule event already created retains the old snapshot.

---

# 63. Idempotency

## 63.1 Worker results

If worker transport can retry, the result should include stable:

```text
correlation_id
```

Potential future table:

```text
processed_messages
```

is not needed unless actual duplicate-delivery behavior requires it.

## 63.2 Acknowledgement

Repeated logical request should not produce inconsistent state.

---

# 64. Data Validation Boundaries

## 64.1 API validation

Validate syntax/types.

## 64.2 Domain validation

Validate:

- zone belongs to camera;
- rule subtype consistency;
- lifecycle transition;
- event context type;
- thresholds.

## 64.3 Database constraints

Enforce:

- primary keys;
- foreign keys;
- unique keys;
- nullability;
- basic numeric ranges.

Do not rely exclusively on database exceptions for user-facing validation.

---

# 65. Proposed SQL Constraint Examples

**Illustrative PostgreSQL-oriented examples.**

```sql
CHECK (person_threshold > 0)
```

```sql
CHECK (dwell_threshold_ms > 0)
```

```sql
CHECK (x_norm >= 0 AND x_norm <= 1)
```

```sql
CHECK (y_norm >= 0 AND y_norm <= 1)
```

```sql
CHECK (capture_ended_at IS NULL OR capture_started_at IS NULL
       OR capture_ended_at >= capture_started_at)
```

---

# 66. Migration Strategy

## 66.1 Requirement

All shared schema changes shall be migration-driven once the DB stack is initialized.

## 66.2 Recommended tool

If SQLAlchemy is selected:

```text
Alembic
```

is a natural candidate.

Status: `PROPOSED`.

## 66.3 Migration rules

1. Never edit an already-shared migration casually.
2. Create a new migration for schema evolution.
3. Migration and ORM model change belong in the same PR.
4. Database design document must be updated for contract changes.
5. Destructive migrations require explicit review.
6. Seed-data changes for codes/roles require review.
7. Test migrations on a clean database.
8. Test upgrade from previous shared revision where feasible.

---

# 67. Migration Naming

Recommended:

```text
YYYYMMDD_HHMM_<short_description>
```

or tool-generated revision IDs with descriptive message.

Examples:

```text
create_cameras_and_zones
add_event_context_tables
add_model_registry
```

Avoid:

```text
fix
changes
final
```

---

# 68. Seed Data

Seed only stable baseline data.

Potential:

- role codes;
- event type codes;
- model task codes.

Do not seed unresolved:

- severity codes;
- lifecycle states;
- default thresholds.

---

# 69. Development Database

Recommended:

- separate local/dev DB;
- automated test DB or transaction-isolated test schema;
- no reliance on manually created tables.

Do not commit personal database dumps.

---

# 70. Test Data

Test fixtures should use:

- synthetic user records;
- synthetic camera names;
- deterministic event times;
- known rule thresholds;
- safe evidence references.

Do not use real camera credentials in fixtures.

---

# 71. Database Test Requirements

At minimum test:

## 71.1 Referential integrity

- event requires valid camera;
- rule requires valid camera;
- zone requires valid camera.

## 71.2 Rule subtype

- intrusion rule has intrusion config;
- loitering rule has loitering config;
- crowd rule has crowd config.

## 71.3 Event context

- event type receives matching context.

## 71.4 Acknowledgement

- same user cannot duplicate acknowledgement;
- event remains after acknowledgement.

## 71.5 Evidence

- missing/failed evidence state is representable.

## 71.6 Model provenance

- violence event references valid model version.

---

# 72. Database Error Handling

Backend shall translate low-level DB errors into meaningful domain/API errors.

Examples:

- unique violation;
- FK violation;
- database unavailable;
- transaction conflict.

Do not expose raw SQL or credentials in client errors.

---

# 73. Backup and Restore

For academic MVP:

- at minimum document how to export/backup the application DB;
- document media separately.

Exact automated backup system is `DEFERRED`.

Important:

A DB backup alone does not back up evidence files.

---

# 74. Analytics Data Integrity

Analytics must be derived from:

```text
events
event_acknowledgements
camera_health_history
```

as applicable.

Do not persist hard-coded dashboard counters.

Caching aggregates is optional and not initially required.

---

# 75. Privacy and Minimization

The schema intentionally avoids:

- face templates;
- biometric IDs;
- inferred sensitive attributes;
- full raw video archive;
- persistent track histories.

This reduces unnecessary surveillance-data retention.

---

# 76. Event-Specific Data Dictionary Summary

| Event type | Required context |
|---|---|
| restricted-area intrusion | rule, zone, track if available, trigger position, geometry method |
| loitering | rule, zone, track, observed duration, threshold |
| crowd threshold | rule, zone if scoped, observed count, threshold, counting method |
| violence/fighting | model version, output label, score, threshold, temporal window |
| camera offline | camera, last frame, offline threshold, reason/state transition |

---

# 77. Proposed Database Views

Views are optional.

Potential:

## 77.1 `v_event_ack_state`

Derive whether event is acknowledged.

## 77.2 `v_event_feed`

Join:

- event;
- camera display name;
- acknowledgement state;
- evidence availability.

## 77.3 `v_camera_current_state`

Camera + current health.

Do not add views until query duplication justifies them.

---

# 78. No Database Trigger Dependency for Core Domain Logic

Core event logic should remain testable in application/domain services.

Avoid implementing:

- intrusion;
- loitering;
- crowd threshold;

as database triggers.

Database triggers may be considered only for simple data-integrity enforcement if necessary.

---

# 79. Proposed PostgreSQL DDL Skeleton — `events`

**Illustrative only until PostgreSQL is confirmed and this document is baselined.**

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    event_type_code VARCHAR(64) NOT NULL,
    camera_id UUID NOT NULL REFERENCES cameras(id),
    rule_id UUID NULL REFERENCES rules(id),
    occurred_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    severity_code VARCHAR(32) NULL,
    requires_attention BOOLEAN NOT NULL DEFAULT TRUE,
    lifecycle_status_code VARCHAR(32) NULL,
    correlation_id UUID NULL,
    summary TEXT NULL
);
```

---

# 80. Proposed PostgreSQL DDL Skeleton — `zone_vertices`

```sql
CREATE TABLE zone_vertices (
    zone_id UUID NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    vertex_index INTEGER NOT NULL CHECK (vertex_index >= 0),
    x_norm NUMERIC(8,7) NOT NULL CHECK (x_norm >= 0 AND x_norm <= 1),
    y_norm NUMERIC(8,7) NOT NULL CHECK (y_norm >= 0 AND y_norm <= 1),
    PRIMARY KEY (zone_id, vertex_index)
);
```

---

# 81. Proposed PostgreSQL DDL Skeleton — `event_acknowledgements`

```sql
CREATE TABLE event_acknowledgements (
    id UUID PRIMARY KEY,
    event_id UUID NOT NULL REFERENCES events(id),
    user_id UUID NOT NULL REFERENCES users(id),
    acknowledged_at TIMESTAMPTZ NOT NULL,
    comment TEXT NULL,
    correlation_id UUID NULL,
    UNIQUE (event_id, user_id)
);
```

---

# 82. Proposed PostgreSQL DDL Skeleton — `evidence_items`

```sql
CREATE TABLE evidence_items (
    id UUID PRIMARY KEY,
    event_id UUID NOT NULL REFERENCES events(id),
    evidence_type_code VARCHAR(32) NOT NULL,
    status_code VARCHAR(32) NOT NULL,
    storage_backend_code VARCHAR(32) NOT NULL,
    storage_key TEXT NULL,
    mime_type VARCHAR(128) NULL,
    size_bytes BIGINT NULL CHECK (size_bytes IS NULL OR size_bytes >= 0),
    sha256 CHAR(64) NULL,
    capture_started_at TIMESTAMPTZ NULL,
    capture_ended_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL,
    available_at TIMESTAMPTZ NULL,
    deleted_at TIMESTAMPTZ NULL,
    failure_code VARCHAR(64) NULL,
    failure_detail TEXT NULL
);
```

---

# 83. ORM Mapping Guidance

If SQLAlchemy is used:

- keep ORM models aligned with this document;
- avoid business logic inside model property setters;
- use explicit relationships;
- do not allow automatic lazy loading to create hidden N+1 behavior in event history;
- use transaction boundaries in application services.

Exact ORM library/version remains implementation decision.

---

# 84. Query Ownership

Database queries should be owned by backend modules.

Examples:

- camera queries → camera module;
- zone queries → zone module;
- event history → event/history module;
- analytics aggregates → analytics module.

Avoid one global repository containing unrelated queries.

---

# 85. API Exposure Rule

Database column names are not automatically public API field names.

The API may expose stable DTO/schema fields.

However, API and DB names should remain semantically aligned to avoid unnecessary translation.

---

# 86. Historical Configuration Problem

Example:

1. Loitering rule threshold = 30 s.
2. Event generated.
3. Rule later changes to 60 s.

Historical event must still state:

```text
threshold used = 30 s
observed duration = ...
```

Therefore the event context stores:

```text
threshold_ms_snapshot
```

This is a deliberate design requirement.

---

# 87. Historical Camera Rename Problem

Example:

1. Event occurs on camera ID `C1` named "Entrance".
2. Camera later renamed "North Entrance".

Event identity should still reference stable camera ID.

UI may show current name and optionally historical snapshot name if needed.

A camera-name snapshot is not currently required.

---

# 88. Historical Model Replacement Problem

Example:

1. Violence event generated by model version `v1`.
2. Deployment moves to `v2`.

Old event must continue referencing `v1`.

Never update old event provenance to current model.

---

# 89. Correlation ID Strategy

Proposed:

- one correlation ID per meaningful worker/backend processing unit;
- persisted on events when relevant;
- propagated to logs.

Do not use event ID as the only pre-event correlation mechanism because event ID does not exist before event creation.

---

# 90. Event Uniqueness Strategy

There is no universal database uniqueness constraint that can identify duplicate events across all event types.

Duplicate suppression is domain-specific.

Potential event fingerprint:

```text
camera
event type
rule
track
episode
```

but `episode` semantics vary.

Therefore do not add arbitrary:

```text
UNIQUE(camera_id, event_type_code, occurred_at)
```

because legitimate simultaneous events may exist.

---

# 91. Camera Offline Uniqueness

Offline state is best protected by health state transition logic:

```text
healthy → offline
```

not a time-based unique constraint.

Sustained offline state does not generate repeated events.

---

# 92. Evidence Cardinality

An event may have:

- zero evidence items if generation fails/not required;
- one snapshot;
- one clip;
- multiple evidence items in future.

Therefore:

```text
events 1 → many evidence_items
```

is intentional.

---

# 93. Acknowledgement Cardinality

Proposed:

```text
event 1 → many acknowledgements
user 1 → many acknowledgements
```

with one acknowledgement per user per event.

If the team wants only one global acknowledgement, modify during baseline.

---

# 94. Role Cardinality

Proposed:

```text
user many ↔ many roles
```

through `user_roles`.

This is more flexible than one hard-coded role column.

For a small project, one role per user would also be sufficient; the team should confirm before implementation.

---

# 95. Authentication Credential Storage

Because authentication strategy is `TBD`, this document intentionally does **not** define:

```text
password_hash
refresh_token
session_token
```

columns as final schema.

If local password auth is selected, create a separate auth-specific design/migration.

Do not put password hashes directly in `users` by assumption.

---

# 96. Media Storage Key Semantics

`evidence_items.storage_key` should be an opaque application-controlled reference.

Examples:

```text
events/<event-id>/snapshot-1.jpg
```

or object-store key.

It should not be:

```text
C:\Users\Name\Desktop\secret.mp4
```

returned directly to clients.

---

# 97. Database Naming Standard

## Tables

Plural snake_case:

```text
events
camera_health_history
model_versions
```

## Columns

snake_case:

```text
occurred_at
model_version_id
```

## Foreign keys

```text
<entity>_id
```

## Booleans

```text
enabled
requires_attention
```

---

# 98. Check Constraint Naming

If explicit names are used:

```text
ck_<table>_<meaning>
```

Example:

```text
ck_zone_vertices_x_norm_range
```

Foreign keys:

```text
fk_<table>_<column>_<target>
```

Indexes:

```text
ix_<table>_<columns>
```

Exact naming conventions may follow ORM defaults if consistent.

---

# 99. Migration Review Checklist

Every DB-changing PR shall verify:

- [ ] schema change is reflected here;
- [ ] migration exists;
- [ ] rollback/down behavior considered;
- [ ] clean DB migration succeeds;
- [ ] existing data migration considered;
- [ ] new nullability is safe;
- [ ] indexes are justified;
- [ ] secrets are not added;
- [ ] API impact assessed;
- [ ] AI-worker contract impact assessed;
- [ ] test fixtures updated.

---

# 100. Initial Migration Sequence Recommendation

If the schema is accepted, a practical migration order is:

1. users / roles / user_roles
2. cameras
3. zones / zone_vertices
4. rules + subtype config
5. models / model_versions
6. camera health / violence policies
7. events
8. event context tables
9. evidence
10. acknowledgements
11. optional feedback
12. optional audit
13. indexes

This order follows foreign-key dependencies.

---

# 101. Database Reset Policy During Early Development

Before the first shared baseline, the team may choose to reset local development databases instead of writing complex data migrations.

After a migration has been shared and used by all contributors:

- do not silently rewrite migration history;
- create forward migrations.

---

# 102. Database Performance Boundaries

The MVP is not expected to support enterprise-scale CCTV history.

Do not prematurely:

- partition tables;
- shard;
- add read replicas;
- create materialized aggregate pipelines.

Measure first.

---

# 103. Future Partitioning Path

If event volume becomes large:

```text
events
→ time-range partitioning
```

may be considered.

Status: `DEFERRED`.

This is not necessary for current scope.

---

# 104. Database Security Requirements Mapping

| Concern | Design |
|---|---|
| Credentials | external reference; not plaintext |
| Evidence | DB stores protected reference, not public path |
| Authorization | backend enforces; DB not exposed to frontend |
| PII minimization | limited user fields, no biometric data |
| Audit | append log proposed |
| SQL injection | parameterized ORM/query layer |
| Secret logging | prohibited |

---

# 105. SRS Traceability Matrix

| Database area | Related SRS |
|---|---|
| `users`, `roles` | FR-AUTH-*, FR-USER-* |
| `cameras` | FR-CAM-* |
| `zones`, `zone_vertices` | FR-ZONE-* |
| `rules` | FR-RULE-* |
| intrusion config/context | FR-INT-* |
| loitering config/context | FR-LOIT-* |
| crowd config/context | FR-CROWD-* |
| model registry | MLR-MOD-*, MLR-LIC-* |
| violence policy/context | FR-VIO-*, MLR-VIO-* |
| `events` | FR-EVT-* |
| evidence | FR-EVD-* |
| acknowledgements | FR-ALT-004/005 |
| feedback | FR-ALT-006 |
| health history | FR-CAM-006/007/008 |
| audit | FR-AUD-* |
| indexes/history | FR-HIST-* |
| analytics | FR-ANL-* |
| timestamps | NFR-DATA-002 |
| integrity | NFR-DATA-001/003 |

---

# 106. Use-Case Traceability Matrix

| Table area | Related use cases |
|---|---|
| users/roles | UC-AUTH-001/002 |
| cameras | UC-CAM-* |
| zones | UC-ZONE-* |
| rules | UC-RULE-* |
| events | UC-EVT-001 through UC-EVT-006 |
| evidence | UC-EVD-001 |
| acknowledgements | UC-EVT-006 |
| feedback | UC-EVT-007 |
| history indexes | UC-HIST-* |
| analytics | UC-ANL-001 |
| model versions | UC-AI-* |
| health history | UC-EVT-005 |

---

# 107. Open Database Decisions

| ID | Decision | Status |
|---|---|---|
| DB-OD-001 | Confirm PostgreSQL | `TBD` |
| DB-OD-002 | Confirm UUID generation mechanism | `TBD` |
| DB-OD-003 | Confirm normalized zone coordinates | `TBD` |
| DB-OD-004 | Confirm rule subtype tables | `PROPOSED` |
| DB-OD-005 | Confirm one event context table per event type | `PROPOSED` |
| DB-OD-006 | Confirm no dedicated alerts table | `PROPOSED` |
| DB-OD-007 | Confirm no incidents table initially | `PROPOSED` |
| DB-OD-008 | Confirm multi-acknowledgement cardinality | `TBD` |
| DB-OD-009 | Confirm event lifecycle/status design | `TBD` |
| DB-OD-010 | Confirm audit-log inclusion | `TBD` |
| DB-OD-011 | Confirm evidence storage backend | `TBD` |
| DB-OD-012 | Confirm exact health-state codes | `TBD` |
| DB-OD-013 | Confirm severity model | `TBD` |
| DB-OD-014 | Confirm source-type codes | `TBD` |
| DB-OD-015 | Confirm role model | `TBD` |
| DB-OD-016 | Confirm retention policies | `TBD` |
| DB-OD-017 | Confirm old zone geometry reconstruction need | `TBD` |
| DB-OD-018 | Confirm worker-job persistence requirement | `TBD` |

---

# 108. Baseline Checklist

Before setting:

```yaml
status: BASELINED
```

the team shall confirm:

- [ ] PostgreSQL or alternative selected.
- [ ] Identifier strategy accepted.
- [ ] Timestamp strategy accepted.
- [ ] Camera fields match selected input mode.
- [ ] No camera credentials are stored in plaintext.
- [ ] Zone coordinate system accepted.
- [ ] Rule config tables accepted.
- [ ] Intrusion parameters baselined.
- [ ] Loitering parameters baselined.
- [ ] Crowd parameters baselined.
- [ ] Camera health policy baselined.
- [ ] Violence model policy design accepted.
- [ ] Event taxonomy accepted.
- [ ] Event context-table pattern accepted.
- [ ] Alert-as-event-projection decision accepted or replaced.
- [ ] Incident omission accepted or relationship defined.
- [ ] Acknowledgement cardinality accepted.
- [ ] Event lifecycle design accepted or explicitly deferred.
- [ ] Evidence metadata fields accepted.
- [ ] Evidence storage selected.
- [ ] Model registry fields accepted.
- [ ] Audit inclusion decided.
- [ ] Indexes match expected queries.
- [ ] Retention/deletion rules reviewed.
- [ ] Migration tool selected.
- [ ] No field exists only because an AI assistant guessed it.

---

# 109. Implementation Rule for AI Assistants

Once this document is baselined:

1. Do not add a table absent from this design without updating the design first.
2. Do not add a column solely to make code compile.
3. Do not remove a foreign key to bypass an integrity error.
4. Do not change nullability without migration/data review.
5. Do not add JSON blobs where structured columns are specified.
6. Do not persist raw detections/tracks unless the design is changed.
7. Do not store media binaries in the DB unless an ADR changes the decision.
8. Do not add authentication credential fields until authentication is selected.
9. Do not create an `incidents` table until its domain semantics are defined.
10. Do not create an `alerts` table unless the alert/event relationship is deliberately changed.
11. Do not silently seed unresolved enum/status values.
12. Every schema change requires a migration and documentation update.

---

# 110. Final Database Design Rule

> **The Sentinel AI database exists to preserve durable, interpretable operational facts — not every transient computer-vision observation.**
>
> A good MVP schema shall make it possible to answer:
>
> - Which camera produced this event?
> - Which rule or model caused it?
> - Which configuration value was actually used at that time?
> - Which model version produced the AI result?
> - What evidence belongs to the event?
> - Who acknowledged it and when?
> - Can the event still be interpreted after rules/models change?
> - Can history and analytics be queried efficiently?
>
> If a proposed schema change cannot explain which project requirement it serves, it should not be added merely because it appears conventional.
