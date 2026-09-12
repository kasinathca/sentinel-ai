---
title: "Sentinel AI — Verification and Test Plan"
document_id: "SEN-TEST"
version: "0.2.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-09-12"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "test strategy"
  - "test levels"
  - "requirement verification"
  - "test case identification"
  - "test fixtures"
  - "pass fail criteria"
  - "regression policy"
  - "test evidence"
  - "final demo acceptance suite"
---

# Sentinel AI — Verification and Test Plan

> **Document purpose**
>
> This document defines how Sentinel AI shall be verified before it is considered complete.
>
> It is the master test plan for:
>
> - backend modules;
> - database behavior;
> - API contracts;
> - AI-worker contracts;
> - deterministic event rules;
> - violence/fighting model integration;
> - frontend behavior;
> - WebSocket/reconnect behavior;
> - evidence handling;
> - security and privacy controls;
> - performance measurement;
> - end-to-end workflows;
> - final demonstration acceptance.
>
> This document remains the master test plan for the whole Sentinel system.
>
> As of 2026-09-12, the **violence model/runtime qualification suite has
> execution evidence**, while most backend/frontend/detector/tracker/full-E2E
> test families remain pending.
>
> Individual test cases become factual only when execution evidence exists.

---

# 0. Document Control

## 0.1 Authority

After baseline approval, this document becomes authoritative for verification planning.

It is subordinate to:

1. `PROJECT_HANDBOOK.md`
2. `02-srs.md`
3. `03-use-case-specification.md`
4. `04-system-architecture.md`
5. `06-database-design.md`
6. `07-api-specification.md`
7. `08-ai-ml-design.md`
8. `11-model-card-and-evaluation.md`
9. `12-ui-ux-specification.md`
10. `13-security-and-privacy.md`
11. accepted ADRs

## 0.2 Test status vocabulary

Use:

```text
NOT_YET_EXECUTED
PASS
FAIL
BLOCKED
SKIPPED_WITH_JUSTIFICATION
INVALIDATED
```

Do not use:

```text
probably works
looks fine
mostly passes
```

## 0.3 Test type vocabulary

```text
UNIT
MODULE
DATABASE
API
CONTRACT
AI_WORKER
MODEL_EVALUATION
FRONTEND
REALTIME
SECURITY
PERFORMANCE
RECOVERY
END_TO_END
MANUAL_ACCEPTANCE
```

---

# 1. Test Objectives

Sentinel testing shall verify:

1. requirements are implemented;
2. component boundaries behave as specified;
3. deterministic rules are correct;
4. AI failures are explicit;
5. persisted event history is trustworthy;
6. operator acknowledgement is durable;
7. evidence failures do not destroy events;
8. unauthorized access is denied;
9. real-time updates reconcile with persistent state;
10. final demo is reproducible.

---

# 2. Verification Principles

## 2.1 Requirements first

Every important test should trace to:

```text
requirement ID
or
use-case ID
```

## 2.2 Deterministic before probabilistic

Test deterministic:

- geometry;
- timer;
- counting;
- persistence;
- API;

before attributing failure to AI.

## 2.3 Negative tests are mandatory

A feature is not verified only because the happy path succeeds.

Test:

- invalid input;
- unavailable dependencies;
- unauthorized user;
- malformed worker result;
- missing evidence;
- repeated request.

## 2.4 Evidence over verbal claims

A test result requires:

- command or steps;
- actual outcome;
- pass/fail;
- artifact/log/screenshot where useful.

---

# 3. Test Pyramid

Recommended emphasis:

```text
many unit/module tests
↓
fewer integration/contract tests
↓
focused end-to-end acceptance tests
```

Do not rely on only browser-clicking through the final system.

---

# 4. Test Environments

## 4.1 DEV

Purpose:

- local development;
- rapid tests;
- mocks/fixtures allowed.

## 4.2 TEST

Purpose:

- isolated automated tests;
- deterministic DB;
- synthetic/test configuration.

## 4.3 DEMO

Purpose:

- integrated final demonstration;
- real selected model/artifacts;
- controlled media;
- mocks disabled unless explicitly disclosed.

Exact environment implementation remains `TBD`.

---

# 5. Test Data Classes

Use explicit categories:

```text
SYNTHETIC_FIXTURE
CONTROLLED_VIDEO
EXTERNAL_DATASET_TEST
MALFORMED_INPUT
SECURITY_PAYLOAD
PERFORMANCE_INPUT
```

Do not mix formal model-test data with demo fixtures silently.

---

# 6. Test Evidence Directory

Recommended:

```text
artifacts/
├── tests/
│   ├── unit/
│   ├── api/
│   ├── database/
│   ├── worker/
│   ├── frontend/
│   ├── realtime/
│   ├── security/
│   ├── performance/
│   └── e2e/
```

Large/private media should remain outside Git unless permitted.

---

# 7. Test Case Record Template

```yaml
test_id: "TC-..."
title: "..."
type: "..."
requirements:
  - "..."
use_cases:
  - "..."
preconditions:
  - "..."
input:
  - "..."
steps:
  - "..."
expected:
  - "..."
actual:
  - "NOT_YET_EXECUTED"
status: "NOT_YET_EXECUTED"
evidence:
  - "TBD"
commit: "TBD"
executed_at: "TBD"
executed_by: "TBD"
```

---

# 8. Naming Convention

Recommended:

```text
TC-UNIT-...
TC-DB-...
TC-API-...
TC-RULE-...
TC-WRK-...
TC-ML-...
TC-UI-...
TC-WS-...
TC-SEC-...
TC-PERF-...
TC-E2E-...
```

---

# 9. Backend Unit Tests

Primary targets:

- domain validation;
- state transitions;
- rule policies;
- conversion/mapping;
- duplicate logic;
- evidence state logic.

Backend unit tests should avoid requiring:

- browser;
- real database;
- real model;

unless the test is explicitly integration-level.

---

# 10. Camera Domain Unit Tests

## TC-UNIT-CAM-001 — Create valid camera object

Expected:

- required fields accepted;
- identity generated externally/appropriately.

## TC-UNIT-CAM-002 — Reject unsupported source type

Expected:

- validation failure.

## TC-UNIT-CAM-003 — Disabled camera semantics

Expected:

```text
enabled = false
```

is not automatically represented as:

```text
health = offline
```

---

# 11. Zone Geometry Unit Tests

## TC-UNIT-ZONE-001 — Normalized coordinate range

Reject:

```text
x < 0
x > 1
y < 0
y > 1
```

## TC-UNIT-ZONE-002 — Minimum polygon vertices

Reject invalid polygon with insufficient points.

## TC-UNIT-ZONE-003 — Reprojection

Normalized polygon should map consistently across different display sizes.

---

# 12. Point-in-Polygon Tests

For the selected geometry method:

## TC-RULE-GEO-001

Point clearly outside → false.

## TC-RULE-GEO-002

Point clearly inside → true.

## TC-RULE-GEO-003

Boundary behavior → according to baselined policy.

## TC-RULE-GEO-004

Malformed polygon → rejected before evaluation.

---

# 13. Intrusion Rule Tests

## TC-RULE-INT-001 — Outside remains outside

Expected events:

```text
0
```

## TC-RULE-INT-002 — Outside enters zone

Expected:

```text
1 intrusion event
```

## TC-RULE-INT-003 — Remains inside

Expected:

```text
no frame-by-frame duplicate events
```

## TC-RULE-INT-004 — Exit and re-entry

Expected:

according to retrigger policy.

## TC-RULE-INT-005 — Disabled rule

Expected:

```text
0 events
```

## TC-RULE-INT-006 — Wrong camera/zone relationship

Expected:

- configuration rejected.

---

# 14. Loitering Rule Tests

## TC-RULE-LOIT-001 — Below threshold

Expected:

```text
0 events
```

## TC-RULE-LOIT-002 — Reaches threshold

Expected:

```text
1 event
```

## TC-RULE-LOIT-003 — Exits before threshold

Expected:

```text
0 events
```

## TC-RULE-LOIT-004 — Track loss

Expected:

according to baselined grace/reset policy.

## TC-RULE-LOIT-005 — Sustained presence after first event

Expected:

no duplicate flood.

---

# 15. Crowd Rule Tests

## TC-RULE-CROWD-001 — Below threshold

Expected:

```text
0 events
```

## TC-RULE-CROWD-002 — At threshold

Expected:

according to baselined `>=` or `>` semantics.

## TC-RULE-CROWD-003 — Above threshold

Expected:

```text
1 candidate/event episode
```

## TC-RULE-CROWD-004 — Sustained exceedance

Expected:

no frame-by-frame duplicates.

## TC-RULE-CROWD-005 — Falls below and re-crosses

Expected:

according to retrigger policy.

---

# 16. Camera Health Tests

## TC-UNIT-HEALTH-001 — Healthy stream

Frames continue → health remains healthy.

## TC-UNIT-HEALTH-002 — Temporary delay

Behavior depends on configured offline threshold.

## TC-UNIT-HEALTH-003 — Sustained no-frame state

Expected:

- offline transition;
- one offline event episode.

## TC-UNIT-HEALTH-004 — Disabled camera

Expected:

- not classified as unexpected offline.

## TC-UNIT-HEALTH-005 — Recovery

Expected:

- health returns according to policy;
- no duplicate offline spam.

---

# 17. Duplicate Suppression Tests

For each event family:

```text
intrusion
loitering
crowd
violence
camera_offline
```

verify:

- repeated qualifying observations;
- only allowed event count created;
- retrigger behavior after state reset/cooldown.

---

# 18. Database Test Strategy

Database tests verify:

- schema constraints;
- foreign keys;
- uniqueness;
- transaction behavior;
- migration compatibility;
- persistence semantics.

Use isolated test database.

---

# 19. Database Migration Tests

## TC-DB-MIG-001 — Empty DB upgrade

Expected:

- all migrations apply successfully.

## TC-DB-MIG-002 — Current shared revision upgrade

Expected:

- migration succeeds from previous expected revision.

## TC-DB-MIG-003 — Model/schema consistency

Expected:

- ORM models match migrated schema.

---

# 20. Database Referential Integrity

## TC-DB-FK-001

Create event with unknown camera → rejected.

## TC-DB-FK-002

Create zone with unknown camera → rejected.

## TC-DB-FK-003

Hard-delete camera referenced by event → blocked according to design.

## TC-DB-FK-004

Delete model version referenced by violence event → blocked.

---

# 21. Database Event Context Integrity

## TC-DB-EVT-001

Intrusion event + intrusion context → accepted.

## TC-DB-EVT-002

Intrusion event + violence context → application/service rejects.

## TC-DB-EVT-003

Event transaction fails before context creation → no partial inconsistent record.

---

# 22. Acknowledgement Persistence Tests

## TC-DB-ACK-001

Create acknowledgement → persists.

## TC-DB-ACK-002

Same user/event repeated → idempotent behavior.

## TC-DB-ACK-003

Refresh/reload → acknowledgement remains.

## TC-DB-ACK-004

Unknown event → reject.

---

# 23. Evidence Persistence Tests

## TC-DB-EVD-001

Event exists + evidence pending.

## TC-DB-EVD-002

Evidence generation succeeds → available.

## TC-DB-EVD-003

Evidence generation fails → failed state.

## TC-DB-EVD-004

Event remains valid when evidence fails.

---

# 24. API Contract Tests

The API test suite shall validate:

- route;
- method;
- request schema;
- status code;
- response envelope;
- response fields;
- errors.

---

# 25. API Health Tests

## TC-API-HLT-001

`GET /api/v1/health`

Expected:

```text
200
valid success envelope
```

## TC-API-HLT-002

Health response contains no secret configuration.

---

# 26. Camera API Tests

## TC-API-CAM-001

Create valid camera → `201`.

## TC-API-CAM-002

Invalid source kind → validation error.

## TC-API-CAM-003

List cameras → collection envelope.

## TC-API-CAM-004

Unknown ID → `404`.

## TC-API-CAM-005

Disable camera → persisted disabled state.

## TC-API-CAM-006

Unauthorized administrative action → denied.

---

# 27. Zone API Tests

## TC-API-ZONE-001

Create valid polygon.

## TC-API-ZONE-002

Out-of-range coordinate rejected.

## TC-API-ZONE-003

Malformed polygon rejected.

## TC-API-ZONE-004

Update geometry → version increments.

## TC-API-ZONE-005

Zone belongs to wrong camera → reject.

---

# 28. Rule API Tests

## TC-API-RULE-001

Create intrusion rule with valid config.

## TC-API-RULE-002

Create loitering rule with invalid duration → reject.

## TC-API-RULE-003

Create crowd rule with non-positive count → reject.

## TC-API-RULE-004

Update material config → version increments.

## TC-API-RULE-005

Disable → persists.

---

# 29. Event API Tests

## TC-API-EVT-001

List events newest first.

## TC-API-EVT-002

Filter by camera.

## TC-API-EVT-003

Filter by type.

## TC-API-EVT-004

Filter by acknowledgement state.

## TC-API-EVT-005

Unknown event → `404`.

## TC-API-EVT-006

Context shape matches event type.

---

# 30. Pagination Tests

## TC-API-PAGE-001

First page returns:

```text
limit
next_cursor
has_more
```

## TC-API-PAGE-002

Next cursor continues without duplicate/missing stable ordering.

## TC-API-PAGE-003

Invalid cursor → safe validation error.

## TC-API-PAGE-004

Server maximum limit enforced.

Exact max value remains `TBD`.

---

# 31. API Error Envelope Tests

For representative failure:

verify:

```text
error.code
error.message
request_id where configured
```

and ensure absence of:

- stack trace;
- SQL;
- secret;
- local path.

---

# 32. AI Worker Contract Tests

AI-worker tests are separate from model-accuracy evaluation.

Purpose:

- verify input/output shape;
- explicit failures;
- provenance;
- timestamps;
- coordinates.

---

# 33. Worker Person Result Tests

## TC-WRK-DET-001 — Person detected

Expected:

- valid detection;
- normalized bbox;
- model version;
- source timestamp.

## TC-WRK-DET-002 — No person

Expected:

```text
status = success
detections = []
```

## TC-WRK-DET-003 — Invalid frame

Expected:

```text
status = failed
```

not empty success.

---

# 34. Worker Tracking Tests

## TC-WRK-TRK-001

Sequential frames maintain track.

## TC-WRK-TRK-002

No valid detection → tracker handles according to config.

## TC-WRK-TRK-003

Track ID scope documented.

---

# 35. Worker Violence Tests

## TC-WRK-VIO-001

Valid temporal window → structured result.

## TC-WRK-VIO-002

Insufficient frames → explicit failure/insufficient input.

## TC-WRK-VIO-003

Model load missing → explicit failure.

## TC-WRK-VIO-004

Score semantics field present.

---

# 36. Malformed Worker Result Tests

Backend receives:

- missing camera ID;
- invalid bbox;
- unknown schema version;
- unknown model version;
- wrong score type.

Expected:

- reject;
- log safe error;
- do not create event.

---

# 37. Worker Availability Tests

## TC-WRK-FAIL-001

Worker stopped.

Expected:

- backend health becomes degraded;
- event history remains accessible;
- no fake negative inference.

## TC-WRK-FAIL-002

Worker restarts.

Expected:

- health recovers;
- backend remains usable.

---

# 38. Model Evaluation Tests

Model metrics are governed by `11-model-card-and-evaluation.md`.

Test plan responsibilities:

- exact evaluation script executes;
- exact dataset/split referenced;
- output artifact saved;
- metric reproducible.

---

# 39. Detector Evaluation Execution

Required before final reporting:

- detector ID fixed;
- evaluation dataset ID fixed;
- threshold fixed;
- precision measured;
- recall measured;
- mAP only if valid ground truth/evaluator;
- latency measured.

Status now:

```text
NOT_YET_EXECUTED
```

---

# 40. Tracker Evaluation Execution

Required:

- selected tracker/config;
- controlled clips;
- track continuity;
- ID switches/losses;
- optional MOT17 benchmark if claimed;
- latency overhead.

---

# 41. Violence Evaluation Execution

Required:

- exact model;
- exact test dataset;
- exact split hash;
- fixed threshold;
- confusion matrix;
- precision;
- recall;
- F1;
- false-positive review;
- false-negative review;
- inference latency.

---

# 42. Frontend Test Strategy

Frontend tests include:

- component tests;
- API-state tests;
- interaction tests;
- manual browser acceptance.

---

# 43. Application Shell Tests

## TC-UI-SHELL-001

Navigation renders expected items.

## TC-UI-SHELL-002

Selected route highlighted.

## TC-UI-SHELL-003

Protected route behavior follows auth design.

---

# 44. Dashboard Tests

## TC-UI-DASH-001

API data renders.

## TC-UI-DASH-002

Loading state.

## TC-UI-DASH-003

Empty state.

## TC-UI-DASH-004

Section-level error.

## TC-UI-DASH-005

No hard-coded production counters.

---

# 45. Live View Tests

## TC-UI-LIVE-001

Selected camera metadata displays.

## TC-UI-LIVE-002

Zone overlay aligns.

## TC-UI-LIVE-003

Disabled state displayed as disabled.

## TC-UI-LIVE-004

Offline state displayed as offline.

## TC-UI-LIVE-005

Recorded test source not labeled live.

---

# 46. Zone Editor Tests

## TC-UI-ZONE-001

Add vertices.

## TC-UI-ZONE-002

Close polygon.

## TC-UI-ZONE-003

Drag vertex.

## TC-UI-ZONE-004

Reset.

## TC-UI-ZONE-005

Resize viewport preserves polygon alignment.

## TC-UI-ZONE-006

Validation error preserves unsaved geometry where intended.

---

# 47. Rule Form Tests

## TC-UI-RULE-001

Selecting intrusion shows intrusion fields.

## TC-UI-RULE-002

Selecting loitering shows duration fields.

## TC-UI-RULE-003

Invalid threshold shown field-locally.

## TC-UI-RULE-004

Submit loading state prevents repeated submit.

---

# 48. Event List Tests

## TC-UI-EVT-001

Newest events displayed first.

## TC-UI-EVT-002

Filters update results.

## TC-UI-EVT-003

Empty filtered result distinct from error.

## TC-UI-EVT-004

Acknowledgement status visible.

## TC-UI-EVT-005

Evidence status visible.

---

# 49. Event Detail Tests

## TC-UI-EDTL-001

Intrusion context.

## TC-UI-EDTL-002

Loitering context.

## TC-UI-EDTL-003

Crowd context.

## TC-UI-EDTL-004

Violence model score labeled correctly.

## TC-UI-EDTL-005

Camera-offline context.

---

# 50. Evidence Viewer Tests

## TC-UI-EVD-001

Snapshot available.

## TC-UI-EVD-002

Clip available.

## TC-UI-EVD-003

Pending state.

## TC-UI-EVD-004

Failed state.

## TC-UI-EVD-005

Unauthorized state.

---

# 51. Acknowledgement UI Tests

## TC-UI-ACK-001

Click acknowledge → loading.

## TC-UI-ACK-002

Successful response updates state.

## TC-UI-ACK-003

Failed response does not falsely persist.

## TC-UI-ACK-004

Refresh retains backend state.

---

# 52. Accessibility Tests

At minimum:

## TC-UI-A11Y-001

Keyboard reaches core controls.

## TC-UI-A11Y-002

Visible focus.

## TC-UI-A11Y-003

Form labels.

## TC-UI-A11Y-004

Status not color-only.

## TC-UI-A11Y-005

Modal focus behavior.

No formal WCAG compliance claim unless separately evaluated.

---

# 53. Responsive Tests

Test:

```text
desktop
laptop
tablet
mobile
```

Core requirement:

- event list/detail/ack remains usable;
- no critical horizontal overflow.

---

# 54. Real-Time/WebSocket Tests

If WebSocket is baselined.

---

# 55. Connection Tests

## TC-WS-001

Connect authenticated client.

## TC-WS-002

Receive `event.created`.

## TC-WS-003

Receive `event.acknowledged`.

## TC-WS-004

Receive camera-health change.

---

# 56. Reconnect Tests

## TC-WS-REC-001

Disconnect client.

Expected:

- disconnected state.

## TC-WS-REC-002

Reconnect.

Expected:

- REST/persistence reconciliation.

## TC-WS-REC-003

Event created during disconnect.

Expected:

- appears after reconciliation.

## TC-WS-REC-004

No duplicate event row after replay + REST sync.

---

# 57. Security Tests

Security cases are defined in `13-security-and-privacy.md`.

This plan tracks execution.

Mandatory categories:

```text
authentication
authorization
object access
mass assignment
injection
XSS
path traversal
file upload if enabled
SSRF if remote source URLs accepted
WebSocket auth/origin
worker validation
evidence authorization
secret/log review
dependency audit
```

---

# 58. Authentication Test Gate

If auth mechanism remains unimplemented:

security acceptance is blocked.

Do not mark the app secure merely because demo runs on localhost.

---

# 59. Evidence Access Gate

Final acceptance fails if evidence is accessible without required authorization.

---

# 60. Path Traversal Gate

Final acceptance fails if user-controlled media/path input can read arbitrary files.

---

# 61. Secret Exposure Gate

Final acceptance fails if:

- real DB secret;
- camera credential;
- token;

is exposed in repository or frontend bundle.

---

# 62. Performance Test Strategy

Performance tests shall measure actual configured hardware.

No target values are invented in advance.

Metrics may include:

- detector latency;
- tracker overhead;
- violence latency;
- worker pipeline latency;
- event-to-client latency;
- processed FPS.

---

# 63. Performance Test Conditions

Record:

```text
hardware
OS
model
input resolution
source FPS
processed FPS
stream count
warm-up
sample count
commit
```

---

# 64. Performance Test Repetition

Use multiple observations.

Report:

- mean;
- median;
- optional p95.

Exact N remains `TBD`.

---

# 65. Performance Baseline Test Cases

## TC-PERF-DET-001

Detector steady-state latency.

## TC-PERF-TRK-001

Tracker overhead.

## TC-PERF-VIO-001

Violence temporal-window inference latency.

## TC-PERF-WRK-001

Worker end-to-end result latency.

## TC-PERF-E2E-001

Event-condition → frontend render latency.

---

# 66. Recovery Tests

Recovery tests verify graceful degradation.

---

# 67. Database Failure

## TC-REC-DB-001

Database unavailable.

Expected:

- API reports service failure safely;
- no fake successful persistence.

---

# 68. AI Worker Failure

## TC-REC-WRK-001

Worker unavailable.

Expected:

- AI-dependent functionality degraded;
- history/admin unaffected where possible.

---

# 69. Evidence Storage Failure

## TC-REC-EVD-001

Event persists but media write fails.

Expected:

- evidence failed state;
- event still visible/acknowledgeable.

---

# 70. Camera Source Failure

## TC-REC-CAM-001

Source stops.

Expected:

- health transition;
- offline event according to policy.

---

# 71. Frontend Network Failure

## TC-REC-UI-001

Browser disconnects.

Expected:

- stale/disconnected indication;
- no claim of current live updates.

---

# 72. End-to-End Test Strategy

End-to-end tests exercise:

```text
source
→ AI
→ rule/model
→ persistence
→ API
→ real-time
→ frontend
→ acknowledgement
```

Use only a small number of high-value E2E scenarios.

---

# 73. E2E Golden Intrusion Scenario

## TC-E2E-INT-001

### Preconditions

- backend running;
- database ready;
- worker ready;
- controlled video available;
- camera configured;
- zone configured;
- intrusion rule enabled;
- authorized operator logged in.

### Steps

1. start/replay controlled video;
2. person begins outside zone;
3. person enters zone;
4. worker produces person detection/track;
5. backend evaluates rule;
6. event is persisted;
7. evidence metadata created;
8. frontend receives event;
9. operator opens event;
10. operator acknowledges;
11. refresh/reload.

### Expected

- exactly expected intrusion event count;
- correct camera;
- correct occurrence time context;
- evidence state explicit;
- acknowledgement persists;
- no duplicate flood.

---

# 74. E2E Loitering Scenario

## TC-E2E-LOIT-001

Use controlled video whose person remains in zone above threshold.

Expected:

- event generated at/after threshold;
- no event below threshold;
- one event episode;
- acknowledgement works.

---

# 75. E2E Crowd Scenario

## TC-E2E-CROWD-001

Controlled scene crosses configured person count.

Expected:

- observed count context;
- event once per episode;
- evidence state;
- acknowledgement.

---

# 76. E2E Violence Positive

## TC-E2E-VIO-001

Controlled/allowed positive sample.

Expected:

- structured violence result;
- model version recorded;
- threshold criterion met;
- event visible.

This test does not replace formal model evaluation.

---

# 77. E2E Violence Negative

## TC-E2E-VIO-002

Negative sample.

Expected:

```text
no violence event
```

unless the model produces a known false positive, in which case the result is recorded as a failure/limitation, not hidden.

---

# 78. E2E Camera Offline

## TC-E2E-OFF-001

Healthy source then stop source.

Expected:

- offline after configured criterion;
- event visible;
- disabled state not confused.

---

# 79. E2E Worker Failure

## TC-E2E-WRK-001

Stop worker during operation.

Expected:

- backend still serves history;
- UI indicates degraded AI;
- no fake negative results.

---

# 80. E2E Evidence Failure

## TC-E2E-EVD-001

Force evidence storage failure.

Expected:

- event persists;
- evidence marked failed;
- operator can still review event metadata.

---

# 81. E2E Reconnect

## TC-E2E-WS-001

Disconnect frontend during event generation.

Expected:

- after reconnect, event is recovered from persistence;
- no duplicate visual event.

---

# 82. Test Fixture Management

Fixtures must be stable and versioned by metadata.

Recommended:

```text
fixture_id
file checksum
scenario
expected event count
expected timing
camera config
zone config
rule config
```

---

# 83. Golden Fixture

Highest-priority fixture:

```text
SENT-FIX-INT-001
```

Status:

```text
TBD_NOT_YET_REGISTERED
```

Expected:

```text
one person crosses into one restricted zone exactly once
```

---

# 84. Negative Fixture

Recommended:

```text
SENT-FIX-NEG-001
```

Expected:

- person visible;
- never enters restricted zone;
- no intrusion event.

---

# 85. Loitering Fixtures

At least:

```text
below threshold
above threshold
```

---

# 86. Crowd Fixtures

At least:

```text
below threshold
above threshold
```

---

# 87. Corrupt Media Fixture

A small invalid/corrupt media fixture may be used to test decoder failure.

Do not use untrusted malware samples.

---

# 88. Test DB Fixtures

Use deterministic test entities:

```text
User A
Camera A
Zone A
Rule A
Event A
```

with generated IDs.

Do not depend on developer's personal DB state.

---

# 89. Seed vs Fixture

Seed data:

- stable application bootstrap/reference data.

Test fixture:

- disposable scenario-specific data.

Do not confuse them.

---

# 90. Mocking Policy

Mocks are allowed for:

- external worker in backend unit tests;
- API in isolated frontend component tests;
- evidence adapter;
- clock/time.

Mocks are not sufficient for:

- final E2E acceptance;
- model performance claims.

---

# 91. Clock Control

Deterministic loitering/offline tests should inject/fake time where practical rather than sleeping real seconds.

This makes tests fast and reliable.

---

# 92. Geometry Fixture

Use simple polygons with known inside/outside points.

Example conceptual square:

```text
(0.2,0.2)
(0.8,0.2)
(0.8,0.8)
(0.2,0.8)
```

Values are test-only examples, not production defaults.

---

# 93. API Fixture Isolation

Each test should:

- create required records;
- execute;
- clean/rollback.

Avoid hidden dependency on test execution order.

---

# 94. Test Parallelism

Automated tests should be parallelizable only if isolated.

Do not enable parallelism if it creates shared DB/file collisions.

Correctness over speed.

---

# 95. Regression Policy

Every bug fix should add or update a regression test where practical.

Workflow:

```text
reproduce bug
→ add failing test
→ fix
→ test passes
```

---

# 96. High-Risk Regression Areas

Always rerun after relevant changes:

- auth;
- event creation;
- acknowledgement;
- evidence;
- rule semantics;
- worker contract;
- migrations;
- WebSocket reconnect.

---

# 97. Contract Change Regression

If API changes:

rerun:

- backend contract tests;
- frontend integration tests;
- OpenAPI snapshot if used.

---

# 98. Database Change Regression

If migration/schema changes:

rerun:

- clean migration;
- DB tests;
- API tests;
- event persistence;
- acknowledgement;
- evidence.

---

# 99. AI Model Change Regression

If detector changes:

rerun:

- detector eval;
- tracker integration;
- intrusion;
- loitering;
- crowd;
- performance.

If tracker changes:

rerun:

- intrusion;
- loitering;
- crowd.

If violence model changes:

rerun:

- model evaluation;
- violence E2E;
- latency.

---

# 100. Frontend Regression

After API/state changes:

rerun:

- dashboard;
- event list/detail;
- acknowledge;
- reconnect;
- errors.

---

# 101. Security Regression

After auth/storage/dependency changes:

rerun relevant security negative tests.

---

# 102. Test Automation

Recommended automated suites:

```text
backend unit
backend API
database integration
worker contract
frontend component/integration
```

Manual suites:

```text
visual UX
media playback
E2E demo
security abuse review
performance
```

---

# 103. CI Strategy

If GitHub Actions or another CI system is used:

on PR:

```text
lint
unit tests
API tests
frontend tests
```

Potentially:

```text
DB integration
```

Heavy model tests may be optional/manual due to compute.

---

# 104. Model Tests in CI

Do not download huge model/dataset artifacts on every PR unless practical.

Use:

- small contract fixtures;
- mock model output;
- lightweight smoke inference where possible.

Full model evaluation remains controlled/manual or scheduled.

---

# 105. CI Failure Policy

Do not merge if required checks fail unless:

- issue documented;
- test intentionally changed;
- reviewer accepts.

Do not disable tests to obtain green status.

---

# 106. Flaky Tests

A flaky test is a defect.

Do not repeatedly rerun until green and ignore cause.

Record:

```text
flaky
```

and fix/isolate.

---

# 107. Test Coverage

Code coverage percentage may be recorded but is not the primary quality metric.

Do not set arbitrary high coverage target without reason.

Focus on:

- critical branches;
- rule logic;
- authorization;
- failure paths.

---

# 108. Manual Test Record

Recommended:

```yaml
manual_test_id: "..."
browser: "..."
viewport: "..."
commit: "..."
steps:
  - "..."
result: "PASS"
screenshots:
  - "..."
```

---

# 109. Screenshot Evidence

Useful for:

- dashboard;
- live view;
- zone editor;
- event detail;
- evidence;
- acknowledge;
- offline/degraded states.

Screenshot alone does not prove persistence/authorization.

---

# 110. Database Evidence

For persistence tests, evidence may include:

- API GET after mutation;
- direct test query in controlled environment;
- automated assertion.

Prefer API-level verification for user-visible behavior.

---

# 111. Log Evidence

Logs may support:

- correlation;
- worker failure;
- timing.

Do not expose secrets in test artifacts.

---

# 112. Test Failure Severity

Suggested internal categories:

```text
BLOCKER
CRITICAL
MAJOR
MINOR
```

Example blocker:

- cannot persist events.

Critical:

- unauthorized evidence access.

Major:

- loitering event duplicates.

Minor:

- small layout issue.

---

# 113. Stop-Demo Conditions

Do not proceed with final demo as "complete" if:

- backend cannot persist events;
- acknowledgement does not persist;
- worker failure creates fake negative results;
- unauthorized evidence accessible;
- secrets exposed;
- vertical slice not reproducible.

---

# 114. Final Demo Acceptance Suite

This is the minimum suite to run before presentation.

---

# 115. Acceptance A — Startup

## ACPT-001

Fresh documented environment starts required services.

Pass if:

- backend starts;
- DB ready;
- worker ready or declared degraded explicitly;
- frontend loads.

---

# 116. Acceptance B — Authentication

## ACPT-002

Authorized user can sign in/access protected app.

## ACPT-003

Unauthenticated user cannot access protected operations.

Exact flow depends on auth design.

---

# 117. Acceptance C — Camera

## ACPT-004

Configured camera/source appears.

## ACPT-005

Health state visible.

---

# 118. Acceptance D — Zone

## ACPT-006

Admin can open zone editor.

## ACPT-007

Polygon saves and reloads aligned.

---

# 119. Acceptance E — Rule

## ACPT-008

Intrusion rule can be enabled.

Configuration visible after refresh.

---

# 120. Acceptance F — Golden Intrusion

## ACPT-009

Controlled video produces expected intrusion event exactly as specified.

This is mandatory.

---

# 121. Acceptance G — Evidence

## ACPT-010

Event detail shows evidence or explicit pending/failed state.

No silent broken media.

---

# 122. Acceptance H — Acknowledgement

## ACPT-011

Operator acknowledges.

## ACPT-012

Refresh confirms persisted acknowledgement.

Mandatory.

---

# 123. Acceptance I — Event History

## ACPT-013

Event appears in history.

## ACPT-014

Filter by event type/camera works.

---

# 124. Acceptance J — Camera Offline

## ACPT-015

Stop source.

Expected offline behavior occurs according to configured policy.

---

# 125. Acceptance K — Worker Failure

## ACPT-016

Stop AI worker.

Expected:

- UI/backend degrade honestly;
- existing history remains available.

---

# 126. Acceptance L — Real-Time Reconnect

## ACPT-017

Disconnect/reconnect client.

Expected:

- state reconciles.

Required only if WebSocket is baselined.

---

# 127. Acceptance M — Security

## ACPT-018

Unauthorized evidence access denied.

## ACPT-019

Admin-only action denied to lower role.

## ACPT-020

Repository/config secret review passes.

---

# 128. Acceptance N — Violence

## ACPT-021

Selected positive sample produces structured model result/event according to threshold.

## ACPT-022

Selected negative sample behaves as measured.

If model makes a known error, report it honestly.

---

# 129. Acceptance O — Analytics

## ACPT-023

Analytics loads persisted event data.

No mock numbers.

---

# 130. Acceptance P — Responsive/UX

## ACPT-024

Primary desktop browser flow works without critical layout break.

---

# 131. Final Demo Acceptance Result

Template:

```yaml
acceptance_run_id: "DEMO-ACPT-..."
commit: "..."
date: "..."
environment: "..."
tests_total: "TBD"
passed: "TBD"
failed: "TBD"
blocked: "TBD"
decision: "NOT_YET_EXECUTED"
```

---

# 132. Requirement Verification Matrix Seed

| Requirement family | Primary test type |
|---|---|
| FR-AUTH | API + security + UI |
| FR-CAM | API + DB + UI |
| FR-ZONE | rule + API + UI |
| FR-RULE | unit + API + UI |
| FR-DET | worker + model evaluation |
| FR-TRK | worker + operational evaluation |
| FR-INT | rule + E2E |
| FR-LOIT | rule + E2E |
| FR-CROWD | rule + E2E |
| FR-VIO | worker + model eval + E2E |
| FR-EVT | DB + API + E2E |
| FR-ALT | API + UI + E2E |
| FR-EVD | DB + API + UI + security |
| FR-HIST | API + UI |
| FR-ANL | API + UI |
| FR-AUD | DB + API if implemented |
| FR-UI | frontend |
| FR-INTG | contract + recovery |
| FR-CFG | unit + startup |
| FR-DEMO | E2E acceptance |
| NFR-SEC | security |
| NFR-PERF | performance |
| NFR-REL | recovery + E2E |
| NFR-PRIV | security/privacy review |
| NFR-MAINT | code/doc review |
| NFR-TEST | this plan/execution |
| NFR-USAB | UI/manual |
| NFR-OBS | logging/correlation |
| NFR-COMPAT | browser/runtime test |
| NFR-DATA | DB |
| NFR-ACAD | evidence/review |

---

# 133. Test Traceability Requirement

Every final requirement should eventually map:

```text
Requirement
→ Test ID
→ Execution result
→ Evidence
```

The full matrix belongs in:

`15-requirements-traceability.md`

---

# 134. Test Execution Log

Recommended table:

| Date | Test ID | Commit | Status | Evidence |
|---|---|---|---|---|
| `TBD` | `TBD` | `TBD` | `NOT_YET_EXECUTED` | `TBD` |

---

# 135. Test Review Cadence

During 2–3 week build:

## Daily

- unit/API regression for changed areas.

## At first vertical slice

- E2E intrusion.

## After each major feature

- relevant module + E2E.

## Before demo

- full acceptance suite.

---

# 136. Day-by-Day Verification Focus

## Days 1–3

- domain/rule unit tests;
- API schema tests;
- DB migration tests.

## Days 4–6

- detector/worker contract;
- frontend component tests.

## Days 6–8

- golden intrusion E2E.

## Days 9–11

- loitering/crowd/offline/evidence.

## Days 12–14

- violence evaluation;
- security negatives;
- performance baseline.

## Final days

- regression;
- acceptance suite;
- clean-environment setup.

---

# 137. Clean Environment Test

Before final submission/demo:

1. clone/copy clean project;
2. follow deployment guide;
3. install dependencies;
4. configure env;
5. migrate DB;
6. start services;
7. run smoke tests.

This catches undocumented local dependencies.

---

# 138. Documentation Verification

Verify:

- README commands work;
- deployment guide matches actual commands;
- environment variables documented;
- no obsolete endpoint references.

---

# 139. Academic Evidence Verification

Before final report:

- metric values match evaluation artifacts;
- screenshots correspond to actual system;
- no mock data presented as real;
- no unexecuted test described as passed.

---

# 140. Test Result Immutability

Do not change:

```text
FAIL
```

to:

```text
PASS
```

without rerunning after fix.

Record new execution result.

---

# 141. Invalidated Results

Mark `INVALIDATED` when:

- test was run on wrong build;
- dataset changed;
- evaluator bug found;
- fixture changed materially.

---

# 142. Blocked Tests

Use `BLOCKED` when required dependency is unavailable.

Example:

```text
Violence E2E blocked because final model not selected.
```

Do not mark it skipped silently.

---

# 143. Skipped Tests

`SKIPPED_WITH_JUSTIFICATION` requires explicit reason.

Example:

```text
MOT17 formal benchmark skipped because optional and outside final schedule.
```

---

# 144. Test Ownership

Recommended:

## Backend/System Lead

- DB;
- API;
- integration;
- E2E.

## Frontend/AWT Lead

- UI;
- responsive;
- WebSocket client;
- manual UX.

## AI/Data Lead

- worker;
- model evaluation;
- detector/tracker;
- violence.

Cross-review required for critical tests.

---

# 145. Independent Review

At least one teammate other than feature owner should review:

- golden vertical slice;
- final model metrics;
- security negatives;
- final demo acceptance.

---

# 146. Test Defect Record

Recommended:

```yaml
defect_id: "BUG-..."
test_id: "..."
summary: "..."
severity: "..."
found_at_commit: "..."
expected: "..."
actual: "..."
root_cause: "TBD"
fix_commit: "TBD"
regression_test: "TBD"
status: "OPEN"
```

---

# 147. Defect Closure

A defect closes only when:

- fix implemented;
- original failing test rerun;
- regression test passes.

---

# 148. Test Automation Anti-Patterns

Do not:

- assert only HTTP 200 while ignoring body;
- disable flaky tests permanently;
- mock every layer in an integration test;
- seed random untracked data;
- swallow exceptions;
- mark test pass because no exception appeared.

---

# 149. E2E Anti-Patterns

Do not:

- fake event directly in frontend;
- inject DB row and call it AI integration;
- use hidden development endpoint without disclosure;
- manually change acknowledgement state in DB.

---

# 150. Security Test Anti-Patterns

Do not:

- test only logged-in admin;
- assume UUID prevents access;
- skip authorization because "it's local";
- use real destructive payloads against unrelated systems.

---

# 151. Performance Test Anti-Patterns

Do not:

- time one frame;
- include model load in one candidate but not another;
- report source FPS as inference FPS;
- benchmark on different hardware without noting it;
- run with debug/profiler and compare to optimized build without disclosure.

---

# 152. Model Test Anti-Patterns

Do not:

- evaluate on training data;
- tune threshold on final test;
- copy paper metrics;
- hide false positives;
- choose only easiest clips.

---

# 153. UI Test Anti-Patterns

Do not:

- treat screenshot as proof of backend persistence;
- replace API error with fake data;
- omit loading/error states;
- test only desktop if responsive behavior is claimed.

---

# 154. Pre-Merge Test Checklist

For each PR:

- [ ] Relevant unit tests pass.
- [ ] Relevant integration tests pass.
- [ ] New behavior has test.
- [ ] No known regression.
- [ ] Docs/contracts updated.
- [ ] Security impact considered.
- [ ] Screenshots included for UI change.
- [ ] Migration tested if DB change.
- [ ] Model/data references updated if AI change.

---

# 155. Final Test Report Structure

At project completion, test report should summarize:

1. environment;
2. commit;
3. automated test counts;
4. failed/blocked/skipped;
5. final acceptance suite;
6. security tests;
7. performance results;
8. model evaluation reference;
9. known limitations.

---

# 156. Current Execution Status

As of this document:

```text
Automated tests executed: NOT_YET_VERIFIED
Final E2E tests executed: NOT_YET_EXECUTED
Security acceptance: NOT_YET_EXECUTED
Performance acceptance: NOT_YET_EXECUTED
Model evaluation: NOT_YET_EXECUTED
Final demo acceptance: NOT_YET_EXECUTED
```

These fields must be updated only from actual evidence.

---

# 157. Open Test Decisions

| ID | Decision | Status |
|---|---|---|
| TEST-OD-001 | Backend test framework/version | `TBD` |
| TEST-OD-002 | Frontend test framework | `TBD` |
| TEST-OD-003 | E2E browser framework | `TBD` |
| TEST-OD-004 | Test DB strategy | `TBD` |
| TEST-OD-005 | CI platform/workflow | `TBD` |
| TEST-OD-006 | Performance repetition count | `TBD` |
| TEST-OD-007 | Detector evaluation annotation set | `TBD` |
| TEST-OD-008 | MOT17 benchmark included? | `TBD` |
| TEST-OD-009 | Exact security audit tool(s) | `TBD` |
| TEST-OD-010 | Exact browser support matrix | `TBD` |
| TEST-OD-011 | WebSocket required for final MVP? | `PROPOSED` |
| TEST-OD-012 | Clean-environment platform | `TBD` |
| TEST-OD-013 | Evidence-failure injection method | `TBD` |
| TEST-OD-014 | DB-failure injection method | `TBD` |
| TEST-OD-015 | Test artifact retention | `TBD` |

---

# 158. Baseline Checklist

Before changing this document to `BASELINED`:

- [ ] Test status vocabulary accepted.
- [ ] Test ID convention accepted.
- [ ] Rule test matrix accepted.
- [ ] DB test strategy accepted.
- [ ] API contract testing accepted.
- [ ] Worker contract tests accepted.
- [ ] Model evaluation handoff accepted.
- [ ] Frontend state tests accepted.
- [ ] WebSocket/reconnect tests accepted.
- [ ] Security execution matrix accepted.
- [ ] Performance measurement plan accepted.
- [ ] Golden E2E scenario accepted.
- [ ] Final demo acceptance suite accepted.
- [ ] Fixture management accepted.
- [ ] Regression policy accepted.
- [ ] Clean-environment test accepted.
- [ ] No test is falsely marked passed.

---

# 159. AI Assistant Test Rules

An AI coding assistant shall never:

1. claim tests passed without execution;
2. invent test counts;
3. delete a failing test to make CI green;
4. weaken assertions without justification;
5. silently skip authorization negatives;
6. replace real integration tests with mocks and call them E2E;
7. fabricate screenshots/logs;
8. mark `BLOCKED` test as `PASS`;
9. change expected behavior to match a bug without spec review;
10. hide model errors from evaluation;
11. use test data as training data without registry update;
12. hard-code fake analytics in acceptance mode;
13. disable security controls for demo;
14. claim performance targets that were not measured;
15. write final report claims from unverified test output.

---

# 160. Final Verification Rule

> **Sentinel AI is complete only when its critical behavior is demonstrated by evidence, not merely by implementation presence.**
>
> The minimum trustworthy verification chain is:
>
> ```text
> requirement
> → implemented behavior
> → test case
> → actual execution
> → pass/fail result
> → evidence
> ```
>
> The highest-priority final acceptance remains:
>
> ```text
> controlled video
> → person detection
> → tracking
> → restricted-zone event
> → persistence
> → evidence state
> → frontend notification
> → acknowledgement
> → refresh
> → persisted acknowledgement
> ```
>
> If this flow cannot be reproduced in a clean documented environment, the project shall not claim the integrated MVP is complete.


---

# 73. Executed Violence Qualification Suite — 2026-09-12

The following experiment/test sequence has execution evidence and shall not be
described as merely planned.

| Evidence ID | Purpose | Result |
|---|---|---|
| Phase 2D / `EXP-VIO-RUNTIME-COMPAT-001` | exact raw-video I3D feature reproduction | `PASS` |
| Phase 2E-A | frozen baseline classifier parity | `PASS` |
| Phase 2F | one-command raw MP4 → exact I3D → baseline | `PASS` |
| Phase 2G-A | cold-process runtime benchmark | `PASS` |
| Phase 2G-B | persistent-extractor runtime benchmark | `PASS` |
| Phase 2H-A | validation-only Logistic baseline live-window study | `COMPLETE` |
| Phase 2H-B | validation-only temporal-model live-window study | `PASS` |
| Phase 2H-C | validation-only live threshold calibration | `PASS` |
| Phase 2I / `EXP-VIO-LIVE-WINDOW-004` | one-time official live-policy TEST | `PASS` |
| Phase 2J / `EXP-VIO-LIVE-RUNTIME-001` | raw-video final temporal-policy parity | `PASS` |

## 73.1 Key pass criteria achieved

### Exact feature compatibility

Required:

```text
reference shape == generated shape
feature cosine approximately 1
small numeric error
```

Observed on both compatibility fixtures:

```text
cosine > 0.9999999
raw feature shapes identical
```

### Frozen temporal validation reproduction

Required confusion:

```text
TN=405 FP=5 FN=15 TP=60
```

Observed: exact match.

### Final live-policy TEST

Frozen before TEST:

```text
W1
stride 1
3-of-5
threshold 0.906
```

Observed official TEST:

```text
TN=285 FP=15 FN=21 TP=86
F1=0.826923
precision=0.851485
positive-video coverage=0.803738
specificity=0.950000
```

### Raw-video final-policy parity

Required:

- threshold flags identical;
- 3-of-5 flags identical;
- final event condition identical.

Observed:

```text
Normal fixture   = PASS
Fighting fixture = PASS
```

## 73.2 What is still not verified

These executed AI tests do **not** prove:

- backend event persistence;
- duplicate/cooldown behavior;
- evidence-media generation;
- WebSocket delivery;
- operator acknowledgement;
- full event-to-client latency;
- detector/tracker quality;
- multi-camera production load.

Those remain in the broader system test plan.

Detailed artifacts and hashes are listed in
`19-violence-model-and-runtime-qualification.md`.
