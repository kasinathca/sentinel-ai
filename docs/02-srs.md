---
title: "Sentinel AI — Software Requirements Specification"
document_id: "SEN-SRS"
version: "0.1.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
team_size: 3
architecture_baseline: "FastAPI modular monolith + separate AI worker"
last_updated: "2026-08-19"
owners:
  - "TBD"
reviewers:
  - "TBD"
authoritative_for:
  - "functional requirements"
  - "non-functional requirements"
  - "AI/ML system requirements"
  - "external behavioral requirements"
  - "acceptance criteria"
supersedes: []
---

# Sentinel AI — Software Requirements Specification

> **Document purpose**
>
> This Software Requirements Specification (SRS) defines the externally observable and testable requirements of Sentinel AI.
>
> It is intentionally written so that a developer, reviewer, tester, or AI coding assistant can determine what the system **shall** do without inventing missing behavior.
>
> This document does **not** define implementation details that belong in the architecture, database, API, AI design, or deployment documents unless those details are already an explicit project constraint.
>
> **Unknown values remain `TBD`. They must not be silently guessed.**

---

# 0. Document Control

## 0.1 Authority

This document is authoritative for mandatory product behavior after requirements are baselined.

It is subordinate to:

- `PROJECT_HANDBOOK.md`
- `01-vision-and-scope.md`
- accepted Architecture Decision Records where those ADRs define constraints that do not contradict requirements

Implementation shall not redefine requirements merely because code currently behaves differently.

## 0.2 Requirement lifecycle

Requirement lifecycle is separate from project decision status.

| Lifecycle | Meaning |
|---|---|
| `DRAFT` | Proposed requirement not yet baselined |
| `BASELINED` | Accepted requirement |
| `MODIFIED` | Baselined requirement changed through control process |
| `RETIRED` | Requirement intentionally removed |

All requirements in this version are `DRAFT` unless explicitly stated otherwise.

## 0.3 Scope-status vocabulary

| Scope status | Meaning |
|---|---|
| `CONFIRMED_SCOPE` | The underlying capability is already accepted in the MVP |
| `PROPOSED_SCOPE` | The capability or exact behavior requires team acceptance |
| `TBD_SCOPE` | A requirement cannot be fully specified because a source decision is unresolved |
| `DEFERRED_SCOPE` | Valid future requirement not in the MVP |
| `REJECTED_SCOPE` | Explicitly excluded |

## 0.4 Normative language

- **shall** — mandatory requirement
- **should** — recommendation, not mandatory
- **may** — permitted optional behavior
- **shall not** — mandatory prohibition

Words such as *fast*, *secure*, *robust*, *intelligent*, *real-time*, and *accurate* are not sufficient requirements unless objectively defined.

## 0.5 Requirement structure

Each requirement contains:

- requirement ID;
- title;
- lifecycle;
- scope status;
- priority;
- source;
- verification method;
- dependencies where applicable;
- rationale;
- normative statement;
- clarifications/constraints;
- acceptance criteria.

## 0.6 Priority

| Priority | Interpretation |
|---|---|
| `MUST` | Required for MVP acceptance |
| `SHOULD` | Important but may be simplified if schedule risk threatens MVP |
| `COULD` | Optional if time remains |
| `WONT_MVP` | Explicitly not part of current MVP |

## 0.7 Verification method vocabulary

Typical methods:

- inspection;
- static analysis;
- unit test;
- integration test;
- API test;
- system test;
- security test;
- performance test;
- model evaluation;
- demonstration;
- document review.

## 0.8 Requirements-engineering reference

This SRS is informed by the discipline of ISO/IEC/IEEE 29148:2018 requirements engineering.

This project does not claim formal certification to that standard.

Official reference:

https://www.iso.org/standard/72089.html

---

# 1. Product Overview

## 1.1 Product perspective

Sentinel AI is a web-based intelligent CCTV monitoring and event-management system.

The confirmed architectural baseline is:

```text
Web frontend
    ↕
FastAPI modular monolith
    ↕
Application persistence / evidence integration

Separate AI worker
    ↕
video source
```

Exact frontend technology, database technology, worker transport, video transport, and media-storage implementation remain governed by separate design decisions.

## 1.2 Primary system purpose

The system shall support the following end-to-end concept:

```text
video
→ AI observation
→ tracking/context
→ deterministic rule or violence inference
→ event
→ persistence
→ operator-facing alert
→ acknowledgement/review
→ historical analysis
```

## 1.3 MVP event categories

The MVP scope includes:

- restricted-area intrusion;
- loitering;
- crowd-threshold event;
- violence/fighting event;
- camera-offline event.

## 1.4 Explicitly excluded from MVP

The MVP shall not include:

- facial recognition;
- biometric identity profiles;
- fall detection;
- fire/smoke detection;
- audio anomaly detection;
- SMS/email notification adapters;
- PWA/mobile-specific application;
- multiple-site enterprise monitoring;
- autonomous online retraining.

---

# 2. User Classes and Actors

## 2.1 Administrator

**Status:** `PROPOSED_SCOPE`

An administrative user is expected to configure system resources such as cameras, zones, rules, and possibly users.

Exact permissions remain `TBD`.

## 2.2 Operator

**Status:** `PROPOSED_SCOPE`

An operator is expected to monitor events, review evidence, acknowledge alerts/events, and inspect history.

Exact permissions remain `TBD`.

## 2.3 Reviewer / supervisor

**Status:** `PROPOSED_SCOPE`

A reviewer/supervisor may inspect history, analytics, and event outcomes.

Exact permissions remain `TBD`.

## 2.4 System actor — AI worker

The AI worker is an internal system actor that produces structured AI observations/results.

## 2.5 System actor — camera/video source

A configured source provides video or frames.

Exact supported input modes remain `TBD`.

---

# 3. System-Wide Behavioral Principles

## 3.1 Observation/event separation

A low-level detection shall not automatically be treated as a domain event.

## 3.2 Track/identity separation

A track identifier shall not represent a real-world identity.

## 3.3 Human review

AI/rule results shall support human review and shall not be described as legal or criminal determinations.

## 3.4 Explicit failure

Processing failure shall not silently be represented as a successful negative detection result.

## 3.5 Traceability

A formal event shall be traceable, directly or indirectly, to the source observation/rule/model context required by the final design.

---

# 4. Functional Requirements
### FR-AUTH-001 — Authenticated access to protected application functions

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §19  
**Verification:** System test  

**Rationale**

Surveillance events and evidence are not intended to be publicly exposed.

**Normative requirement**

The system shall require successful authentication before a user can access any function classified as protected by the authorization policy.

**Acceptance criteria**

1. An unauthenticated request to a protected function is denied.
2. An authenticated request is evaluated against authorization rules before protected data is returned.
3. The client does not receive protected content merely because a protected page route is known.

---

### FR-AUTH-002 — Server-side authorization

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Security test  

**Rationale**

Client-side hiding is not an access-control mechanism.

**Normative requirement**

The backend shall enforce authorization for protected operations independently of frontend visibility or navigation controls.

**Acceptance criteria**

1. Removing or bypassing a frontend button does not grant backend permission.
2. A user without permission receives a denied response when directly invoking the protected operation.
3. Authorization behavior is covered by at least one negative test for each high-risk operation.

---

### FR-AUTH-003 — Authentication failure handling

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Security test  

**Normative requirement**

The system shall reject invalid authentication attempts without revealing whether a sensitive credential component was partially correct.

**Acceptance criteria**

1. Invalid credentials do not create an authenticated session or token.
2. Failure response does not expose password hashes, secrets, stack traces, or internal authentication details.
3. A failed authentication attempt is distinguishable from successful authentication.

---

### FR-AUTH-004 — Logout or session termination

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS OQ-04  
**Verification:** System test  

**Normative requirement**

If session-based or token-based interactive authentication is adopted, the system shall provide a defined mechanism for the user to terminate the current authenticated session.

**Acceptance criteria**

1. The user can invoke the documented logout/session-termination action.
2. After termination, the same client context can no longer access protected functions without re-authentication, subject to the selected authentication design.
3. The UI reflects that the session is no longer authenticated.

---

### FR-USER-001 — User identity record

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Integration test  

**Normative requirement**

If user accounts are implemented, the system shall maintain a unique application-level identifier for each user account.

**Acceptance criteria**

1. Two active user records do not share the same primary application identifier.
2. Audit-relevant user actions can reference the acting user identifier.
3. Changing display information does not change the stable identifier unless the design explicitly requires it.

---

### FR-USER-002 — Role or permission association

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS OQ-13  
**Verification:** System test  

**Normative requirement**

If role-based access control is adopted, the system shall associate each user with the role or permission data required to evaluate protected actions.

**Acceptance criteria**

1. Authorized actions succeed for a user with the required permission.
2. The same action is denied for a user lacking the permission.
3. The exact permission model is documented before baseline.

---

### FR-CAM-001 — Register a camera or video source

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.1  
**Verification:** System test  
**Dependencies:** OD-005  

**Rationale**

Event processing requires a system-level source identity.

**Normative requirement**

The system shall allow an authorized user to register a supported camera or video source with the metadata required by the selected ingestion design.

**Acceptance criteria**

1. A valid supported source can be created and receives a stable system identifier.
2. Invalid or incomplete required source metadata is rejected.
3. The created source appears in subsequent camera/source retrieval operations.

---

### FR-CAM-002 — List configured camera or video sources

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-001  

**Normative requirement**

The system shall allow an authorized user to retrieve the set of camera or video sources visible to that user.

**Acceptance criteria**

1. The returned collection contains configured sources the user is authorized to view.
2. Unauthorized sources are not exposed.
3. Each returned source includes enough state to distinguish at least its identifier and current configured/health state as defined by the final design.

---

### FR-CAM-003 — Retrieve camera/source details

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-001  

**Normative requirement**

The system shall allow an authorized user to retrieve the configuration and current system-visible state of a specific camera or video source.

**Acceptance criteria**

1. A valid accessible source identifier returns the source details.
2. A nonexistent source identifier produces a defined not-found outcome.
3. An inaccessible existing source does not leak protected details.

---

### FR-CAM-004 — Update camera/source configuration

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-001  

**Normative requirement**

The system shall allow an authorized user to modify supported mutable configuration fields of a camera or video source.

**Acceptance criteria**

1. A valid update persists.
2. Unsupported or invalid values are rejected.
3. Immutable identifiers are not silently replaced.
4. Changes that affect processing become effective according to the documented lifecycle behavior.

---

### FR-CAM-005 — Disable camera/source processing

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

The system shall allow an authorized user to place a configured source into a disabled state that prevents normal event processing for that source.

**Acceptance criteria**

1. A disabled source is distinguishable from an offline-but-enabled source.
2. Normal AI/rule events are not newly generated from intentionally disabled processing unless specifically documented.
3. Re-enabling restores eligibility for processing.

---

### FR-CAM-006 — Camera/source health state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-001  

**Normative requirement**

The system shall maintain an application-visible health state for each enabled camera or video source according to the health criteria defined in the SRS baseline.

**Acceptance criteria**

1. The source can be distinguished as healthy/available versus offline/unavailable using the final state model.
2. Health state changes are persisted or otherwise made observable according to the architecture.
3. The health state does not depend solely on whether the frontend page is open.

---

### FR-CAM-007 — Camera-offline event

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-006  

**Normative requirement**

When an enabled source satisfies the baselined offline condition, the system shall generate a camera-offline event.

**Clarification / constraints**

The exact timeout and failure criteria are `TBD` and shall not be guessed.

**Acceptance criteria**

1. The offline condition is objectively defined before baseline.
2. An event is generated when the condition transitions from not-offline to offline according to the final rule.
3. Repeated health checks do not generate unbounded duplicate offline events.
4. The event references the affected source.

---

### FR-CAM-008 — Camera recovery state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CAM-006  

**Normative requirement**

When an offline source later satisfies the baselined healthy condition, the system shall update its health state to reflect recovery.

**Acceptance criteria**

1. The recovered source is distinguishable from an offline source.
2. The source may resume eligible processing.
3. Whether a dedicated recovery event is created remains a separate design decision and shall not be assumed.

---

### FR-ZONE-001 — Create polygonal monitoring zone

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.4  
**Verification:** System test  

**Normative requirement**

The system shall allow an authorized user to define a polygonal monitoring zone within the coordinate space of a configured camera/source.

**Acceptance criteria**

1. The zone is associated with exactly one configured source unless a future design explicitly permits reuse.
2. Valid polygon coordinates are persisted.
3. Invalid polygon definitions are rejected.
4. The saved polygon can be retrieved and rendered consistently against the associated video coordinate space.

---

### FR-ZONE-002 — Update monitoring zone

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ZONE-001  

**Normative requirement**

The system shall allow an authorized user to modify the supported attributes and geometry of an existing monitoring zone.

**Acceptance criteria**

1. A valid update persists.
2. Invalid geometry is rejected.
3. The system does not apply partially invalid geometry.
4. Existing historical events retain enough context to remain interpretable according to the data design.

---

### FR-ZONE-003 — Disable monitoring zone

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ZONE-001  

**Normative requirement**

The system shall allow an authorized user to disable a zone without deleting historical events previously generated from that zone.

**Acceptance criteria**

1. Disabled zones are not evaluated for new zone-based events.
2. Historical event records remain reviewable.
3. The zone can be re-enabled unless deleted or otherwise restricted.

---

### FR-ZONE-004 — Zone-to-source consistency

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Integration test  
**Dependencies:** FR-ZONE-001  

**Normative requirement**

The system shall reject a zone configuration whose geometry cannot be interpreted in the coordinate system of its associated source under the selected design.

**Acceptance criteria**

1. Coordinate values outside the valid domain are rejected or normalized only if normalization is explicitly specified.
2. A zone belonging to one source is not accidentally evaluated against a different source.
3. Zone/source association is preserved across retrieval and update operations.

---

### FR-ZONE-005 — Zone visualization

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ZONE-001  

**Normative requirement**

The web application shall render configured zone geometry over the associated video/image view with spatial alignment sufficient for the user to verify its placement.

**Acceptance criteria**

1. The rendered polygon corresponds to stored zone geometry.
2. Resizing the display does not intentionally change the represented logical zone.
3. A user can distinguish the zone boundary from the underlying video.

---

### FR-DET-001 — Receive structured person detections

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Contract test  
**Dependencies:** MLR-DET-001  

**Normative requirement**

The application/AI processing pipeline shall support structured person-detection results that include the source context, observation time, detected class, spatial geometry, and model result metadata required by the approved AI contract.

**Acceptance criteria**

1. A valid person-detection result can be consumed without parsing human-readable log text.
2. The source is identifiable.
3. Spatial geometry can be mapped to the corresponding frame coordinate space.
4. Malformed required fields are rejected or quarantined according to the final contract.

---

### FR-DET-002 — Preserve detection provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** MLR-MOD-001  

**Normative requirement**

The system shall preserve sufficient provenance for a detection used in event generation to identify the producing model/version according to the approved model registry design.

**Acceptance criteria**

1. An event investigation can determine which model/version produced relevant AI output where AI output contributed to the event.
2. Model provenance is not replaced with a generic label such as `AI` when a specific version is available.
3. Missing mandatory provenance is treated according to the contract rather than silently invented.

---

### FR-TRK-001 — Receive or derive track identifiers

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** MLR-TRK-001  

**Normative requirement**

The processing pipeline shall provide temporary track identifiers for person observations where tracking is required by a configured rule.

**Acceptance criteria**

1. Successive observations of a tracked subject can reference the same temporary track identifier while the tracker maintains continuity.
2. Track identifiers are scoped according to the final tracker design.
3. Track identifiers are not presented as real-world identities.

---

### FR-TRK-002 — Track-loss handling

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-TRK-001  

**Normative requirement**

The rule-processing layer shall handle loss or interruption of a track without interpreting the lost track as a confirmed event outcome unless the relevant rule explicitly defines that behavior.

**Clarification / constraints**

Exact grace period, if any, is `TBD`.

**Acceptance criteria**

1. A tracker losing a person does not automatically create a violence or intrusion event.
2. Loitering timer behavior on track loss follows the baselined rule semantics.
3. The behavior is deterministic and covered by tests.

---

### FR-RULE-001 — Create a rule configuration

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.4–11.6  
**Verification:** System test  

**Normative requirement**

The system shall allow an authorized user to create a supported rule configuration associated with the camera/source and zone context required by that rule type.

**Acceptance criteria**

1. Supported rule type is validated.
2. Required associations are validated.
3. The rule receives a stable identifier.
4. The rule can subsequently be enabled, disabled, retrieved, and evaluated according to its type.

---

### FR-RULE-002 — Enable and disable rules

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-RULE-001  

**Normative requirement**

The system shall allow an authorized user to enable or disable an existing rule configuration.

**Acceptance criteria**

1. A disabled rule does not generate new events.
2. Re-enabling restores eligibility for evaluation.
3. Historical events generated before disabling remain available.

---

### FR-RULE-003 — Rule configuration validation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-RULE-001  

**Normative requirement**

The system shall reject rule configurations that omit mandatory parameters or reference incompatible resources.

**Acceptance criteria**

1. A loitering rule cannot be accepted without the required zone/time configuration once those fields are baselined.
2. A restricted-zone rule references a compatible zone.
3. A crowd rule contains a valid threshold once the threshold schema is defined.
4. Invalid rules do not become active.

---

### FR-RULE-004 — Deterministic rule evaluation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Unit test  

**Normative requirement**

For the same baselined input state and rule configuration, the deterministic rule engine shall produce the same rule outcome.

**Acceptance criteria**

1. Rule evaluation is testable without running model training.
2. Repeated execution with identical inputs/configuration produces an equivalent outcome.
3. Any time-dependent input is explicit in the test.

---

### FR-RULE-005 — Rule evaluation audit context

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

When a deterministic rule creates an event, the resulting event shall retain enough context to identify the rule configuration that produced it.

**Acceptance criteria**

1. The event references or snapshots the relevant rule identity/version/context according to the data design.
2. Changing a rule later does not make historical events impossible to interpret.
3. The operator can distinguish the event type that was generated.

---

### FR-INT-001 — Restricted-zone entry evaluation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ZONE-001, FR-RULE-001, FR-TRK-001  

**Normative requirement**

The system shall evaluate whether an eligible tracked person satisfies the baselined restricted-zone entry condition for an enabled restricted-zone rule.

**Acceptance criteria**

1. The evaluation uses the configured zone geometry.
2. Only observations from the associated source are considered.
3. The exact point/geometry method is documented and consistently applied.
4. The condition is independently testable with synthetic coordinates.

---

### FR-INT-002 — Restricted-area intrusion event

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-INT-001, FR-EVT-001  

**Normative requirement**

When the restricted-zone entry condition transitions into the event-triggering state defined by the rule semantics, the system shall create a restricted-area intrusion event.

**Acceptance criteria**

1. A valid crossing/entry scenario produces the event.
2. A person remaining outside does not produce the event.
3. The event references the source and rule/zone context.
4. Duplicate suppression semantics are respected.

---

### FR-INT-003 — Intrusion duplicate suppression

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-INT-002  

**Normative requirement**

The system shall prevent a continuously present person from producing an unbounded new restricted-area intrusion event for every processed frame.

**Clarification / constraints**

Exact cooldown/retrigger duration remains `TBD`.

**Acceptance criteria**

1. A controlled test with a person remaining inside the zone does not create one new event per frame.
2. The exact retrigger/cooldown semantics are defined before baseline.
3. Leaving and re-entering behavior follows the baselined rule.

---

### FR-LOIT-001 — Loitering duration tracking

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ZONE-001, FR-TRK-001, FR-RULE-001  

**Normative requirement**

For an enabled loitering rule, the system shall measure the duration for which an eligible track satisfies the rule's in-zone condition.

**Acceptance criteria**

1. Duration begins according to the defined entry semantics.
2. Duration is associated with the correct track and zone.
3. A track outside the zone does not accumulate in-zone duration.
4. The behavior is testable using controlled timestamps.

---

### FR-LOIT-002 — Loitering event threshold

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-LOIT-001, FR-EVT-001  

**Normative requirement**

When an eligible track satisfies the loitering condition for at least the configured threshold according to the baselined timing semantics, the system shall create a loitering event.

**Clarification / constraints**

Numeric threshold is `TBD` and must be configurable or otherwise explicitly baselined.

**Acceptance criteria**

1. Below-threshold presence does not produce a loitering event.
2. At/above threshold produces the defined event once duplicate rules are satisfied.
3. The event references source, zone/rule, and relevant track context.
4. The configured threshold is not hard-coded if configuration is part of the final requirement.

---

### FR-LOIT-003 — Loitering timer reset semantics

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-LOIT-001  

**Normative requirement**

The system shall implement a single documented rule for how loitering duration is reset or preserved when a track exits the zone or is temporarily lost.

**Acceptance criteria**

1. The reset/pause behavior is explicitly documented before baseline.
2. The implementation matches the documented behavior.
3. Tests cover exit and temporary track-loss cases.
4. The system does not use inconsistent behavior across runs.

---

### FR-LOIT-004 — Loitering duplicate suppression

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-LOIT-002  

**Normative requirement**

The system shall prevent one continuous loitering episode from generating an unbounded event stream.

**Acceptance criteria**

1. One continuous qualifying episode produces events only according to the documented retrigger policy.
2. The retrigger policy is testable.
3. The frontend does not receive one alert per frame for the same episode.

---

### FR-CROWD-001 — Crowd count calculation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-RULE-001  

**Normative requirement**

For an enabled crowd rule, the system shall calculate the number of qualifying persons according to one explicitly baselined counting method.

**Acceptance criteria**

1. The counting method is documented as detections, active tracks, or another explicit definition.
2. The count is scoped to the associated camera/zone as configured.
3. The same controlled input produces the same count under deterministic tracking state.
4. The method is not changed silently between backend and UI.

---

### FR-CROWD-002 — Crowd-threshold event

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CROWD-001, FR-EVT-001  

**Normative requirement**

When the crowd count satisfies the configured event threshold according to the baselined crossing/retrigger semantics, the system shall create a crowd-threshold event.

**Acceptance criteria**

1. Below-threshold count does not create the event.
2. Threshold-satisfying input creates an event.
3. The event records or exposes the observed count/threshold context as defined by the data model.
4. Duplicate suppression is applied.

---

### FR-CROWD-003 — Crowd-event duplicate suppression

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-CROWD-002  

**Normative requirement**

The system shall prevent a continuously exceeded crowd threshold from creating an unbounded event per processed frame.

**Acceptance criteria**

1. A sustained over-threshold test does not produce one new event per frame.
2. The retrigger policy is explicitly documented.
3. Dropping below and re-crossing the threshold follows the baselined behavior.

---

### FR-VIO-001 — Violence/fighting inference request

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** AI worker integration test  
**Dependencies:** MLR-VIO-001  

**Normative requirement**

The AI worker shall support processing the temporal video input required by the selected violence/fighting model.

**Acceptance criteria**

1. A supported video segment/window can be submitted to the selected inference pipeline.
2. Unsupported or malformed temporal input produces an explicit failure.
3. The input windowing/preprocessing behavior is documented in the AI design.

---

### FR-VIO-002 — Violence/fighting result contract

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Contract test  
**Dependencies:** FR-VIO-001, MLR-MOD-001  

**Normative requirement**

The AI worker shall produce a structured violence/fighting result containing the class/score information and model provenance required by the approved AI contract.

**Acceptance criteria**

1. The backend can consume the result without parsing console output.
2. The model/version is identifiable.
3. The score semantics are documented.
4. Missing mandatory fields are rejected according to the contract.

---

### FR-VIO-003 — Violence/fighting event criterion

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-VIO-002, FR-EVT-001  

**Normative requirement**

The system shall define and apply one baselined criterion that determines when a violence/fighting model result becomes a domain event.

**Acceptance criteria**

1. The criterion is explicit and testable.
2. A result below the criterion does not create the event.
3. A qualifying result creates the event.
4. The criterion is not inferred from UI display logic.

---

### FR-VIO-004 — Violence/fighting event provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-VIO-003  

**Normative requirement**

A violence/fighting event shall preserve sufficient information to determine which model version and relevant inference result produced the event.

**Acceptance criteria**

1. The event can be traced to model/version.
2. The event can expose the relevant score/classification context according to access policy.
3. Later model replacement does not erase historical provenance.

---

### FR-VIO-005 — Violence inference failure distinction

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Fault-injection test  
**Dependencies:** FR-VIO-001  

**Normative requirement**

If violence inference fails for a required segment, the system shall not represent that failure as a successful `non-violence` classification.

**Acceptance criteria**

1. An inference exception produces an explicit failure state/log/result path.
2. No `non-violence` event/result is fabricated.
3. The failure can be diagnosed from system evidence.

---

### FR-EVT-001 — Persist domain events

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.9  
**Verification:** System test  

**Normative requirement**

The system shall persist each accepted domain event with a stable event identifier and the minimum context required by its event type.

**Acceptance criteria**

1. A generated event remains retrievable after the creating request/job completes.
2. Each event has a stable unique identifier.
3. The event type is identifiable.
4. The event references the affected source.
5. Required event-specific context is validated.

---

### FR-EVT-002 — Event occurrence time

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

The system shall record the occurrence time semantics of each event separately from unrelated display time or client-render time.

**Acceptance criteria**

1. The stored event time follows the documented timestamp definition.
2. The UI does not replace occurrence time with the current browser time.
3. Time conversion does not destroy the original ordering semantics.

---

### FR-EVT-003 — Event type

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

The system shall assign each event exactly one primary event type from the baselined event taxonomy.

**Acceptance criteria**

1. MVP types include intrusion, loitering, crowd threshold, violence/fighting, and camera offline.
2. Unknown event types are not silently accepted unless extensibility behavior is defined.
3. Frontend and backend use consistent event identifiers.

---

### FR-EVT-004 — Event retrieval

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

The system shall allow an authorized user to retrieve a specific event by its identifier.

**Acceptance criteria**

1. An accessible existing event is returned.
2. A nonexistent event produces a defined not-found outcome.
3. An inaccessible event does not expose protected data.

---

### FR-EVT-005 — Event status

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS OQ-12  
**Verification:** System test  

**Normative requirement**

If event lifecycle status is included in the baseline, the system shall maintain the current event status according to a documented state machine.

**Acceptance criteria**

1. Only allowed transitions succeed.
2. Invalid transitions are rejected.
3. Current state is retrievable.
4. Historical transition requirements are followed if baselined.

---

### FR-EVT-006 — Event-state transition history

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-005  

**Normative requirement**

If auditable event status transitions are baselined, the system shall preserve a history identifying at least the event, transition, time, and actor/system source required by the final audit design.

**Acceptance criteria**

1. A status change does not erase all evidence of the previous status.
2. The transition can be traced to the initiating actor or system process.
3. History ordering is deterministic.

---

### FR-EVT-007 — Duplicate event policy

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

Each event-producing mechanism shall apply a baselined duplicate/retrigger policy that prevents frame-level repetition from becoming uncontrolled event duplication.

**Acceptance criteria**

1. Intrusion, loitering, crowd, violence, and offline scenarios each have an explicit duplicate policy.
2. Tests cover sustained conditions.
3. The policy is implemented in the event/rule layer rather than only hidden in the UI.

---

### FR-ALT-001 — Create operator-facing alert representation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.10  
**Verification:** System test  

**Normative requirement**

For each event category configured to require operator attention, the system shall create or expose an operator-facing alert representation linked to the originating event.

**Acceptance criteria**

1. The alert can be traced to the event.
2. The UI can display the alert without inventing event data.
3. The alert does not exist independently of an originating condition unless the final design explicitly allows system alerts.

---

### FR-ALT-002 — Deliver new alert information to connected clients

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ALT-001  

**Normative requirement**

The system shall provide a mechanism by which an authorized connected client can learn about newly created operator-facing alerts without requiring the user to manually reload the entire application.

**Clarification / constraints**

WebSocket is proposed but not yet baselined.

**Acceptance criteria**

1. A newly created test event becomes visible to a connected authorized client through the selected update mechanism.
2. Unauthorized clients do not receive protected event payloads.
3. The selected transport is documented in the API specification.

---

### FR-ALT-003 — Alert presentation minimum context

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** UI system test  
**Dependencies:** FR-ALT-001  

**Normative requirement**

The web application shall present enough context for an operator to identify what event occurred, the associated source, the event time, and the current review/acknowledgement state where applicable.

**Acceptance criteria**

1. The event type is visible.
2. The camera/source identity is visible.
3. The event occurrence time is visible.
4. The current acknowledgement/status state is visible if the lifecycle supports it.

---

### FR-ALT-004 — Acknowledge eligible event/alert

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.12  
**Verification:** System test  

**Normative requirement**

The system shall allow an authorized operator to acknowledge an eligible event or alert.

**Acceptance criteria**

1. An authorized acknowledgement persists.
2. The acting user and acknowledgement time are recorded if the audit/data model requires them.
3. An unauthorized user cannot acknowledge by directly invoking the backend operation.
4. Repeated acknowledgement behavior is deterministic and documented.

---

### FR-ALT-005 — Persistent acknowledgement state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Integration test  
**Dependencies:** FR-ALT-004  

**Normative requirement**

An acknowledgement shall remain observable after the acknowledging client reloads or reconnects.

**Acceptance criteria**

1. Reloading the UI does not revert an acknowledged item to unacknowledged.
2. A second authorized client observes the persisted acknowledgement according to access rules.
3. Persistence survives request completion.

---

### FR-ALT-006 — False-positive feedback

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

If false-positive feedback is included in the MVP baseline, the system shall allow an authorized user to record that an event was judged to be a false positive without deleting the original event.

**Acceptance criteria**

1. The original event remains retrievable.
2. False-positive feedback is distinguishable from model ground truth.
3. The acting user/time can be audited if required.
4. Feedback does not automatically retrain the model.

---

### FR-EVD-001 — Associate evidence with event

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.11  
**Verification:** System test  

**Normative requirement**

The system shall support associating evidence metadata with an event.

**Acceptance criteria**

1. Evidence is linked to the correct event.
2. An event can be retrieved even if evidence generation failed.
3. Evidence metadata does not claim a media artifact exists when creation failed.

---

### FR-EVD-002 — Evidence snapshot

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVD-001  

**Normative requirement**

The system shall support creating or registering at least one event snapshot for event categories where snapshot evidence is part of the final evidence policy.

**Acceptance criteria**

1. A generated snapshot is associated with the correct source/event.
2. The snapshot is retrievable by an authorized user.
3. A missing snapshot is represented explicitly rather than as a broken success state.

---

### FR-EVD-003 — Evidence clip

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVD-001  

**Normative requirement**

The system shall support creating or registering a short event clip for event categories where clip evidence is part of the final evidence policy.

**Clarification / constraints**

Pre-roll/post-roll durations are `TBD`.

**Acceptance criteria**

1. The clip is associated with the correct event.
2. The clip duration/window follows the baselined policy.
3. Authorized playback/retrieval succeeds for a valid artifact.
4. Evidence-write failure is detectable.

---

### FR-EVD-004 — Protected evidence access

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Security test  
**Dependencies:** FR-EVD-001  

**Normative requirement**

The system shall restrict evidence retrieval to users authorized to access the associated event/media.

**Acceptance criteria**

1. An authorized user can retrieve evidence.
2. An unauthorized user cannot retrieve the same media by guessing its identifier/path.
3. Direct storage paths do not bypass authorization unless the selected deployment explicitly uses protected signed access.

---

### FR-EVD-005 — Evidence integrity reference

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-EVD-001  

**Normative requirement**

The evidence metadata shall preserve enough information to identify the stored media artifact unambiguously under the selected storage design.

**Acceptance criteria**

1. Two evidence records do not ambiguously refer to different files through the same identifier.
2. Missing/deleted artifacts are detectable.
3. The application does not rely on unvalidated user-provided filesystem paths.

---

### FR-EVD-006 — Evidence retention/deletion behavior

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Document review + system test  

**Normative requirement**

Before final deployment or demonstration handoff, the system shall define and document evidence retention and deletion behavior.

**Acceptance criteria**

1. A retention policy exists even if the academic MVP uses manual or local retention.
2. Deletion behavior does not silently leave DB metadata claiming accessible media if media was removed.
3. The operator manual/deployment documentation is consistent with the implemented behavior.

---

### FR-INC-001 — Incident concept

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS OQ-11  
**Verification:** System test  

**Normative requirement**

If incidents are implemented as a distinct domain concept, the system shall define the relationship between events and incidents before persistence and API contracts are baselined.

**Acceptance criteria**

1. The relationship cardinality is documented.
2. Creation/linking behavior is defined.
3. UI terminology matches the domain model.
4. An AI assistant is not required to infer whether event and incident are synonyms.

---

### FR-HIST-001 — List historical events

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.13  
**Verification:** System test  
**Dependencies:** FR-EVT-001  

**Normative requirement**

The system shall allow an authorized user to retrieve historical events.

**Acceptance criteria**

1. Persisted events can be listed after the original processing session ends.
2. Results are ordered deterministically.
3. Unauthorized events are excluded.
4. The response supports the final pagination/limit behavior defined in the API specification.

---

### FR-HIST-002 — Filter events by time range

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-HIST-001  

**Normative requirement**

The history function shall support filtering events by a specified event-occurrence time range.

**Acceptance criteria**

1. Events inside the range are eligible for return.
2. Events outside the range are excluded.
3. Boundary semantics are documented.
4. Invalid ranges are rejected.

---

### FR-HIST-003 — Filter events by event type

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-HIST-001  

**Normative requirement**

The history function shall support filtering by one or more baselined event types.

**Acceptance criteria**

1. Filtering for intrusion excludes non-intrusion events unless multiple types are requested.
2. Unsupported type values are rejected or return a defined empty outcome.
3. Filter semantics match the event taxonomy.

---

### FR-HIST-004 — Filter events by source

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-HIST-001  

**Normative requirement**

The history function shall support filtering events by camera/video-source identifier.

**Acceptance criteria**

1. Only events from the requested accessible source are returned.
2. Invalid/nonexistent source handling is defined.
3. Authorization still applies.

---

### FR-HIST-005 — Filter by acknowledgement/status

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-HIST-001, FR-ALT-004  

**Normative requirement**

If acknowledgement or lifecycle status is baselined, the history function shall support filtering by the relevant state.

**Acceptance criteria**

1. Acknowledged filtering produces state-consistent results.
2. Unacknowledged filtering does not rely on frontend-only state.
3. Unsupported states are rejected.

---

### FR-HIST-006 — Pagination or bounded result retrieval

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

The history interface shall prevent an unbounded historical query from requiring the client to receive the entire event dataset in one response once the dataset exceeds the baselined practical limit.

**Acceptance criteria**

1. A documented page/limit/cursor mechanism exists.
2. The same query can retrieve subsequent result sets without silent duplication/loss under stable data conditions.
3. Invalid pagination parameters are validated.

---

### FR-ANL-001 — Analytics from persisted data

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.14  
**Verification:** System test  

**Normative requirement**

The analytics dashboard shall derive displayed operational metrics from persisted Sentinel data or clearly labeled test/demo fixtures.

**Acceptance criteria**

1. Production/demo-live mode does not display arbitrary hard-coded counts as real system metrics.
2. Refreshing analytics after new persisted events can change applicable metrics.
3. Fixture/demo data is visibly distinguishable when used.

---

### FR-ANL-002 — Event count by type

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ANL-001  

**Normative requirement**

The analytics function shall support summarizing event counts by event type for a selected or default documented time range.

**Acceptance criteria**

1. Counts equal the persisted events matching the query definition.
2. Event type labels match the event taxonomy.
3. The time range is visible or otherwise defined.

---

### FR-ANL-003 — Event activity over time

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ANL-001  

**Normative requirement**

The analytics function shall support at least one time-series aggregation of event activity.

**Acceptance criteria**

1. Aggregation interval is documented.
2. Events are grouped by occurrence time rather than browser render time.
3. Empty periods are handled consistently.

---

### FR-ANL-004 — Event count by camera/source

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ANL-001  

**Normative requirement**

The analytics function shall support summarizing event counts by accessible camera/video source.

**Acceptance criteria**

1. Counts match source-filtered event history under the same time range.
2. Unauthorized source data is excluded.
3. Sources with no events are handled according to documented UI behavior.

---

### FR-ANL-005 — Acknowledgement analytics

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-ALT-004, FR-ANL-001  

**Normative requirement**

If acknowledgement is baselined, analytics shall support at least one metric derived from persisted acknowledgement state.

**Acceptance criteria**

1. The metric is computed from stored acknowledgement data.
2. The metric definition is documented.
3. It is not derived solely from client-side transient state.

---

### FR-AUD-001 — Audit security-sensitive user actions

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** Security test  

**Normative requirement**

If audit logging is baselined, the system shall record security- or workflow-significant user actions identified in the security specification.

**Acceptance criteria**

1. Each audited action records the minimum actor/action/time/target context defined by the audit design.
2. Audit recording occurs server-side.
3. An end user cannot arbitrarily forge the acting-user field through request input.

---

### FR-AUD-002 — Audit acknowledgement

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-AUD-001, FR-ALT-004  

**Normative requirement**

If audit logging is baselined, event acknowledgement shall be included as an auditable action.

**Acceptance criteria**

1. The audit record references the event and acting user.
2. The recorded time is server-derived or otherwise trusted according to the design.
3. The audit record is consistent with the persisted acknowledgement.

---

### FR-UI-001 — Display system navigation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §35  
**Verification:** System test  

**Normative requirement**

The web application shall provide navigation that allows an authorized user to reach the MVP monitoring, history, and analytics functions available to that user.

**Acceptance criteria**

1. Required pages/functions are reachable without manually typing undocumented URLs.
2. Unauthorized functions are not presented as usable actions.
3. Navigation does not replace server-side authorization.

---

### FR-UI-002 — Loading state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

The web application shall provide a visible loading or pending state for user operations whose completion is not immediate.

**Acceptance criteria**

1. The UI does not display stale success while a request is unresolved.
2. Successful completion transitions to the appropriate content state.
3. Failure transitions to an error state.

---

### FR-UI-003 — Error state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

The web application shall present a user-understandable error state when a required API/media operation fails.

**Acceptance criteria**

1. A failed request does not leave the UI falsely indicating success.
2. The user can distinguish an error from an empty data set.
3. Sensitive server internals are not displayed.

---

### FR-UI-004 — Empty state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

The web application shall distinguish a valid empty result from an error condition for event/history/analytics views.

**Acceptance criteria**

1. Zero events displays an empty-state message/visual.
2. A backend failure displays an error state instead.
3. The user is not misled into interpreting a failure as zero events.

---

### FR-UI-005 — Connection state

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  

**Normative requirement**

If the client uses a persistent real-time connection, the web application shall represent disconnected/reconnecting state when that connection is unavailable.

**Acceptance criteria**

1. Disconnecting the real-time channel becomes visible within the defined behavior.
2. The client does not continue to claim live updates while disconnected.
3. Reconnection behavior follows the API specification.

---

### FR-INTG-001 — AI-worker/backend structured contract

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §17.7  
**Verification:** System test  

**Normative requirement**

The AI worker and backend shall communicate using a versioned or otherwise explicitly documented structured contract.

**Acceptance criteria**

1. A schema/specification exists.
2. Malformed payloads are rejected.
3. The contract defines mandatory source/time/model/result fields.
4. Both components have at least one integration/contract test.

---

### FR-INTG-002 — Correlation of processing jobs

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS  
**Verification:** System test  
**Dependencies:** FR-INTG-001  

**Normative requirement**

If asynchronous processing can produce delayed/out-of-order results, the system shall use a correlation mechanism sufficient to associate AI results with the correct source/input job.

**Acceptance criteria**

1. Two concurrent jobs are not confused.
2. A result can be traced to the originating source/window/job.
3. The mechanism is documented in the API/architecture specification.

---

### FR-INTG-003 — Malformed worker result handling

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Fault-injection test  
**Dependencies:** FR-INTG-001  

**Normative requirement**

The backend shall reject or quarantine a worker result that fails the approved contract rather than silently coercing missing mandatory fields.

**Acceptance criteria**

1. Missing mandatory source/model/result fields trigger a defined failure.
2. No domain event is created from an invalid payload unless the design explicitly supports partial data.
3. The failure is logged/observable.

---

### FR-INTG-004 — Worker-unavailable behavior

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Integration test  

**Normative requirement**

When the AI worker is unavailable, the backend shall expose a defined degraded/failure state rather than representing AI processing as healthy.

**Acceptance criteria**

1. A controlled worker outage is detectable.
2. New inference-dependent events are not falsely generated as successful results.
3. The web/system health view can represent degraded state if that view is in scope.

---

### FR-CFG-001 — Externalized runtime configuration

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** PROJECT_HANDBOOK §30  
**Verification:** Inspection + integration test  

**Normative requirement**

The system shall support supplying environment-specific runtime configuration without hard-coding real secrets in source code.

**Acceptance criteria**

1. A clean deployment can provide required values externally.
2. Repository defaults do not contain real passwords/keys.
3. Missing mandatory configuration causes explicit startup/runtime failure according to design.

---

### FR-CFG-002 — Documented configuration keys

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS  
**Verification:** Document review  
**Dependencies:** FR-CFG-001  

**Normative requirement**

Each required runtime configuration key shall be documented with purpose, required/optional status, and safe example format.

**Acceptance criteria**

1. The deployment guide lists required keys.
2. `.env.example` or equivalent contains placeholders only.
3. No undocumented secret is required to start the system.

---

### FR-DEMO-001 — Reproducible recorded-video test path

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS ASM-03  
**Verification:** System test  

**Normative requirement**

The project shall provide at least one documented, reproducible recorded-video or equivalent deterministic input path for integration testing, even if live camera input is also supported.

**Acceptance criteria**

1. A team member can replay the same test input.
2. The same input can be used to reproduce at least one MVP event scenario.
3. The test input provenance/usage permission is documented.

---


# 5. AI/ML Requirements

### MLR-MOD-001 — Model identity and version

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Inspection + integration test  

**Normative requirement**

Every AI model used by the integrated system shall have a stable model identifier and version or equivalent immutable provenance descriptor.

**Acceptance criteria**

1. The deployed detector can be identified.
2. The deployed tracker configuration/algorithm can be identified.
3. The deployed violence model can be identified.
4. Replacing a model changes its version/provenance rather than silently overwriting history.

---

### MLR-MOD-002 — Model-source provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

For every final model or pretrained weight artifact, the project shall record the original source, applicable license/terms, acquisition method, and whether the artifact was used as-is, fine-tuned, or trained by the team.

**Acceptance criteria**

1. The model registry contains the source.
2. The license/terms field is not left fabricated.
3. The final report wording matches actual training usage.
4. Third-party pretrained weights are attributed.

---

### MLR-DATA-001 — Dataset registry

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16.4  
**Verification:** Document review  

**Normative requirement**

Every dataset used for training, validation, or formal model evaluation shall have an entry in `docs/10-dataset-registry.md`.

**Acceptance criteria**

1. The registry identifies dataset name/version/source.
2. The role of each subset is stated.
3. The project can determine which exact data informed each reported model result.
4. Unregistered datasets are not used for formal reported metrics.

---

### MLR-DATA-002 — Dataset acquisition provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

The acquisition path for every external dataset used in the project shall be documented in `docs/09-dataset-acquisition.md` with preference for official/original sources.

**Acceptance criteria**

1. Official/original project source is recorded where available.
2. Any mirror is labeled as a mirror.
3. Usage/license terms are recorded or marked unresolved.
4. The team does not cite a mirror as the original academic source.

---

### MLR-DATA-003 — Train/validation/test separation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review + model evaluation  

**Normative requirement**

For every formally evaluated learned model, the project shall define train, validation, and test usage in a way that prevents the final test data from being used for training.

**Acceptance criteria**

1. Test samples are excluded from training.
2. Threshold/hyperparameter tuning uses training/validation data rather than repeatedly optimizing on the final test set.
3. The split is documented or reproducibly generated.
4. Any deviation is explicitly disclosed.

---

### MLR-DATA-004 — Duplicate leakage check

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

When the selected dataset may contain duplicate or near-duplicate clips across splits, the project shall assess and document the risk of train/test leakage.

**Acceptance criteria**

1. A leakage assessment is recorded.
2. Known duplicates crossing formal evaluation splits are removed or disclosed.
3. Evaluation claims acknowledge unresolved leakage risk where applicable.

---

### MLR-DATA-005 — Dataset usage limitations

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

The project shall document known limitations of each final dataset that materially affect interpretation of model performance.

**Acceptance criteria**

1. At least domain, camera/environment, class, and labeling limitations are considered where relevant.
2. The final report does not imply universal generalization from a narrow dataset.
3. Limitations are linked to model-card discussion.

---

### MLR-DET-001 — Person detection capability

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** AI worker integration test  

**Normative requirement**

The selected detector shall produce person detections from supported Sentinel video frames.

**Acceptance criteria**

1. A representative test frame containing a visible person produces at least one person detection under the selected configuration where the detector is expected to succeed.
2. A structured bounding geometry and model score are available.
3. The detector can run through the AI worker rather than only an isolated notebook.

---

### MLR-DET-002 — Person detector evaluation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The project shall evaluate the person detector on a documented Sentinel-relevant evaluation sample or benchmark before claiming suitability.

**Clarification / constraints**

No minimum mAP/precision/recall target is currently baselined.

**Acceptance criteria**

1. Evaluation data is documented.
2. The chosen metric(s) are appropriate to object detection.
3. Actual measured results are stored.
4. Failure examples are reviewed qualitatively.

---

### MLR-DET-003 — Detector threshold provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The person-detection confidence threshold used by the integrated system shall be recorded and justified by experiment or explicit design decision.

**Acceptance criteria**

1. The threshold is not an undocumented magic number.
2. Changing the threshold is traceable.
3. The final model card/configuration states the deployed value.

---

### MLR-TRK-001 — Tracking capability

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** AI worker integration test  

**Normative requirement**

The selected tracker shall maintain temporary track identifiers across successive frames sufficiently to support the implemented loitering and zone rules.

**Acceptance criteria**

1. A representative person sequence maintains a track for a meaningful interval.
2. Track identifiers are available to rule processing.
3. The tracker can recover/fail according to documented behavior.
4. The tracker does not claim real-world identity.

---

### MLR-TRK-002 — Tracker evaluation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The project shall evaluate tracking behavior on documented representative clips before claiming reliable loitering functionality.

**Acceptance criteria**

1. At least track continuity and obvious ID-switch/loss cases are inspected or measured.
2. The evaluation method is documented.
3. Known failure conditions are recorded.
4. Loitering test scenarios use tracking behavior representative of the integrated system.

---

### MLR-VIO-001 — Temporal violence/fighting model

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §11.7  
**Verification:** Model evaluation  

**Normative requirement**

The final violence/fighting capability shall use temporal information from multiple frames or an equivalent temporal representation rather than a single-frame proximity heuristic.

**Acceptance criteria**

1. The selected model/input representation uses temporal context.
2. The AI design documents the temporal window/feature representation.
3. The implementation is not merely `two people close together = fight`.
4. The model runs through the AI worker.

---

### MLR-VIO-002 — Violence dataset fitness assessment

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

Before selecting the primary violence/fighting dataset, the project shall document why the dataset is suitable for the intended fighting/violence task and feasible within the project constraints.

**Acceptance criteria**

1. The assessment covers class/task fit.
2. Acquisition access is verified.
3. Licensing/usage terms are reviewed.
4. Training/inference feasibility is considered.
5. Known domain limitations are recorded.

---

### MLR-VIO-003 — Violence model baseline

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The project shall establish and record at least one reproducible baseline model result before attempting optional complexity improvements.

**Acceptance criteria**

1. Baseline experiment ID exists.
2. Dataset/split/configuration are recorded.
3. Metrics are measured.
4. The model artifact or reproducible training path is identified.

---

### MLR-VIO-004 — Violence model evaluation metrics

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The project shall report at least precision, recall, F1-score, and confusion-matrix information for the final violence/fighting classifier where the selected task formulation supports these metrics.

**Acceptance criteria**

1. Metrics are computed on the documented evaluation set.
2. The positive class is explicitly defined.
3. The confusion matrix class ordering is labeled.
4. Values are not copied from another paper unless clearly identified as external comparison rather than Sentinel result.

---

### MLR-VIO-005 — Violence threshold provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

If a continuous model score is thresholded to create a binary violence/fighting result, the deployed threshold shall be recorded and justified.

**Acceptance criteria**

1. Threshold value is documented.
2. Selection method is documented.
3. Threshold is not optimized on the final held-out test set without disclosure.
4. Event criterion uses the same deployed value.

---

### MLR-VIO-006 — Violence false-positive review

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

The project shall review and document representative false-positive and false-negative examples for the final violence/fighting model.

**Acceptance criteria**

1. At least one false-positive case is reviewed if any exist.
2. At least one false-negative case is reviewed if any exist.
3. Likely causes/limitations are discussed without inventing certainty.
4. The findings inform final limitations.

---

### MLR-INF-001 — Inference failure reporting

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Fault-injection test  

**Normative requirement**

The AI worker shall return or surface an explicit processing failure when a required model cannot load or inference cannot complete.

**Acceptance criteria**

1. Missing model artifact is detected.
2. Unsupported input is detected.
3. Inference exception is not converted to a successful negative prediction.
4. Failure is observable by the backend/logging path.

---

### MLR-INF-002 — Inference input preprocessing traceability

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Inspection  

**Normative requirement**

The preprocessing applied to model inputs shall be documented and versioned with the relevant model/configuration.

**Acceptance criteria**

1. Resize/crop/normalization/frame sampling are recorded where applicable.
2. Training and inference preprocessing differences are documented.
3. The deployed preprocessing code can be identified from a repository commit/configuration.

---

### MLR-INF-003 — Inference latency measurement

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Performance test  

**Normative requirement**

The project shall measure inference latency for the final detector and violence pipeline in the documented target test environment.

**Acceptance criteria**

1. Hardware/software environment is recorded.
2. Measurement start/end definition is documented.
3. Multiple observations are measured rather than a single anecdotal value where practical.
4. Results are reported as measured values without unsupported scalability claims.

---

### MLR-INF-004 — Model loading strategy

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Inspection + performance test  

**Normative requirement**

The selected AI worker design shall define whether models are loaded once at worker startup, lazily, or per job, and shall avoid repeated full model loading per frame unless explicitly justified.

**Acceptance criteria**

1. The strategy is documented.
2. Profiling/inspection confirms behavior.
3. A model-load failure has an explicit error path.

---

### MLR-EXP-001 — Experiment reproducibility record

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

Every model experiment used to justify a final model decision shall record the code commit, dataset/split, model/base weights, key hyperparameters, and measured result.

**Acceptance criteria**

1. An experiment can be traced to code and data metadata.
2. Missing fields are marked `TBD/unknown` rather than fabricated.
3. Final model selection cites one or more recorded experiments.

---

### MLR-EXP-002 — Randomness control

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §16  
**Verification:** Model evaluation  

**Normative requirement**

For experiments whose results materially depend on pseudo-random operations, the project shall record random seeds where the libraries and workflow support deterministic seeding.

**Acceptance criteria**

1. Seed values are recorded.
2. Known nondeterminism is disclosed.
3. The report does not claim bit-for-bit reproducibility when the environment does not guarantee it.

---

### MLR-LIC-001 — AI dependency license review

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §16  
**Verification:** Document review  

**Normative requirement**

Before a model/framework is accepted into the final project, its applicable software/model license shall be reviewed and recorded.

**Acceptance criteria**

1. License is recorded.
2. Redistribution obligations are identified where relevant.
3. The repository license decision does not knowingly conflict with accepted dependency obligations.
4. Unresolved license uncertainty blocks final acceptance of the dependency.

---


# 6. Non-Functional Requirements

### NFR-SEC-001 — Secrets shall not be committed

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** PROJECT_HANDBOOK §17  
**Verification:** Inspection + secret scan  

**Normative requirement**

The repository shall not contain real passwords, API keys, session secrets, camera credentials, database credentials, or equivalent production/demo secrets.

**Acceptance criteria**

1. Repository scan/manual review finds no known real secrets.
2. Example configuration uses placeholders.
3. Secrets required at runtime are externally supplied.

---

### NFR-SEC-002 — Protected resource authorization

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Security test  

**Normative requirement**

Authorization shall be enforced on the server for protected event, evidence, configuration, and user-management resources.

**Acceptance criteria**

1. Direct backend requests without permission are denied.
2. Frontend manipulation does not bypass the control.
3. At least one negative authorization test exists for each protected high-risk resource category implemented.

---

### NFR-SEC-003 — Password handling

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Security test  

**Normative requirement**

If local password authentication is used, plaintext passwords shall not be stored.

**Acceptance criteria**

1. Stored credential representation is not plaintext.
2. Password verification uses the selected secure password-hashing mechanism.
3. Logs do not contain submitted passwords.

---

### NFR-SEC-004 — Authentication token confidentiality

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection + security test  

**Normative requirement**

If bearer/session tokens are used, the system shall not intentionally expose full valid tokens in logs or UI diagnostics.

**Acceptance criteria**

1. Application logs do not print full tokens.
2. Error responses do not include secrets.
3. Debug output in final configuration does not expose token contents unnecessarily.

---

### NFR-SEC-005 — Input validation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** API/contract test  

**Normative requirement**

Untrusted client and worker inputs shall be validated against the approved schema and domain constraints before use.

**Acceptance criteria**

1. Malformed API bodies are rejected.
2. Malformed worker payloads are rejected.
3. Invalid identifiers/enum values are rejected.
4. Invalid zone geometry is rejected.

---

### NFR-SEC-006 — Path traversal protection

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Security test  

**Normative requirement**

If the system accepts or resolves media/file identifiers, it shall prevent user-controlled input from escaping authorized storage locations through path traversal or equivalent unsafe path construction.

**Acceptance criteria**

1. Traversal payloads do not expose arbitrary files.
2. Media identifiers are validated/resolved safely.
3. Security tests cover representative traversal attempts.

---

### NFR-SEC-007 — Error information exposure

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Security test  

**Normative requirement**

Client-visible error responses shall not expose stack traces, source-code paths, secret configuration, or database credentials in the final demonstration/deployment configuration.

**Acceptance criteria**

1. Forced server errors return safe client messages.
2. Sensitive internals remain in protected logs only where appropriate.
3. Debug exception pages are not exposed in final configuration.

---

### NFR-SEC-008 — Dependency version recording

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

Runtime dependencies shall be version-pinned or otherwise reproducibly recorded to the degree supported by the selected package ecosystem.

**Acceptance criteria**

1. Backend dependencies are recorded.
2. AI-worker dependencies are recorded.
3. Frontend dependencies are recorded once frontend is selected.
4. A clean setup does not depend on undocumented package versions.

---

### NFR-SEC-009 — Evidence access control

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Security test  

**Normative requirement**

Evidence media shall not be publicly retrievable by default when the associated event is protected.

**Acceptance criteria**

1. Unauthorized direct access fails.
2. Media identifiers are not sufficient to bypass authorization.
3. Authorized access works.

---

### NFR-PERF-001 — Event-to-client latency measurement

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Performance test  

**Normative requirement**

The project shall measure end-to-end event-to-client notification latency using a documented start and end point.

**Clarification / constraints**

Target value remains `TBD`.

**Acceptance criteria**

1. Measurement definition is documented.
2. At least multiple test observations are collected where practical.
3. Hardware/network environment is recorded.
4. No target threshold is claimed unless baselined.

---

### NFR-PERF-002 — API latency measurement

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** Performance test  

**Normative requirement**

The project shall measure representative API response latency for core event/history operations in the final test environment.

**Acceptance criteria**

1. At least one core read and one write workflow are measured.
2. Environment and data size are recorded.
3. Results are reported as measurements, not unsupported scalability claims.

---

### NFR-PERF-003 — Non-blocking long-running AI work

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Architecture inspection + performance test  

**Normative requirement**

Long-running AI processing shall not execute synchronously inside ordinary interactive request handlers in a way that prevents the backend from serving unrelated requests for the duration of inference.

**Acceptance criteria**

1. AI work runs through the separate AI worker architecture.
2. A long AI job does not require the FastAPI request worker to run model inference directly.
3. Backend remains responsive to unrelated health/basic requests under the tested design.

---

### NFR-PERF-004 — Bounded history responses

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** System test  

**Normative requirement**

Historical event retrieval shall use a bounded retrieval mechanism once data volume is sufficient to make unbounded responses impractical.

**Acceptance criteria**

1. API design has page/limit/cursor semantics.
2. A request cannot accidentally return an unlimited entire event history unless explicitly allowed for a small controlled export.
3. Frontend supports the chosen mechanism.

---

### NFR-REL-001 — Explicit component health

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Integration test  

**Normative requirement**

The system shall provide enough health/diagnostic state to distinguish at least backend availability, configured source health, and AI-worker processing failure during integration testing.

**Acceptance criteria**

1. Backend health can be checked.
2. Camera/source offline state is observable.
3. Worker outage/failure is observable.
4. A single generic `system okay` indicator is not used to mask component failure.

---

### NFR-REL-002 — No silent AI failure

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Fault-injection test  
**Dependencies:** MLR-INF-001  

**Normative requirement**

A failed AI inference shall not be converted into a successful negative result.

**Acceptance criteria**

1. Forced failure is surfaced.
2. No false `no violence`/`no person` success result is fabricated.
3. The failure is diagnosable.

---

### NFR-REL-003 — Persistent event durability

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Integration test  

**Normative requirement**

Once an event-creation transaction is reported as successful, the event shall remain retrievable after request/job completion and application-page refresh.

**Acceptance criteria**

1. Successful creation survives client refresh.
2. The event can be queried later.
3. Partial failures do not report success when persistence failed.

---

### NFR-REL-004 — Idempotent acknowledgement behavior

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** API test  

**Normative requirement**

The acknowledgement operation shall have deterministic repeated-call behavior so that retrying the same logical acknowledgement does not corrupt event state.

**Acceptance criteria**

1. Repeated acknowledgement does not create contradictory state.
2. The resulting state is documented.
3. Retries can be tested safely.

---

### NFR-REL-005 — Recoverable client connection

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** System test  

**Normative requirement**

If persistent real-time communication is adopted, the client shall have a documented reconnection strategy and shall not assume message delivery is exactly once.

**Acceptance criteria**

1. Disconnect/reconnect behavior is specified.
2. Duplicate/stale event handling is defined.
3. The UI indicates disconnected state.

---

### NFR-PRIV-001 — No facial identification

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS NG-01  
**Verification:** Inspection  

**Normative requirement**

The MVP shall not implement facial recognition or map face imagery to real-world identity.

**Acceptance criteria**

1. No face-recognition dependency/pipeline is part of MVP processing.
2. No biometric identity database exists.
3. UI does not label tracked persons with inferred real-world names.

---

### NFR-PRIV-002 — Minimum evidence retention

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Document review  

**Normative requirement**

The project shall define an evidence-retention policy that avoids indefinite retention by default unless explicitly justified.

**Acceptance criteria**

1. Retention behavior is documented.
2. The policy distinguishes event evidence from raw source video.
3. The final operator/deployment docs match implementation.

---

### NFR-PRIV-003 — Demo footage provenance

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Document review  

**Normative requirement**

Every video used in the final demonstration shall have documented provenance and a legitimate basis for academic use.

**Acceptance criteria**

1. Source is recorded.
2. Private footage is not used without authorization.
3. Redistribution restrictions are respected.
4. The repository does not accidentally publish restricted footage.

---

### NFR-PRIV-004 — No sensitive-attribute inference

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

The MVP shall not intentionally infer protected or highly sensitive personal attributes from a person's appearance.

**Acceptance criteria**

1. No such model is included.
2. UI/database has no fields for inferred sensitive attributes.
3. Documentation does not claim such inference.

---

### NFR-MAINT-001 — Module boundaries

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Architecture/code review  

**Normative requirement**

The FastAPI application shall preserve internal module boundaries consistent with the modular-monolith architecture rather than placing unrelated domain logic in route handlers.

**Acceptance criteria**

1. Domain logic is separated from route definitions to a reasonable project-appropriate degree.
2. AI inference is not embedded throughout routes.
3. Cross-module interactions are reviewable.

---

### NFR-MAINT-002 — Consistent domain terminology

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

Code and documentation shall use the defined terms detection, track, zone, rule, event, alert, evidence, incident, and acknowledgement consistently.

**Acceptance criteria**

1. A track is not named `user` or `identity` without reason.
2. An event and alert are not casually interchanged if the domain design distinguishes them.
3. API/database/UI naming is reconciled with the glossary.

---

### NFR-MAINT-003 — No undocumented magic thresholds

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

Operational thresholds that affect event behavior shall be defined in configuration/specification and shall not exist only as unexplained numeric literals in code.

**Acceptance criteria**

1. Loitering threshold source is identifiable.
2. Crowd threshold source is identifiable.
3. Confidence thresholds are documented.
4. Cooldown/offline thresholds are documented.

---

### NFR-MAINT-004 — Documentation synchronized with contract changes

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Document/code review  

**Normative requirement**

A change to API, database schema, model contract, or externally visible behavior shall update the corresponding authoritative documentation in the same change set or before merge.

**Acceptance criteria**

1. PR/change review identifies affected docs.
2. Merged implementation matches current spec.
3. Known temporary divergence is explicitly recorded, not hidden.

---

### NFR-MAINT-005 — Reproducible setup

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Clean-environment setup test  

**Normative requirement**

A contributor using the supported development environment shall be able to set up the application using repository documentation without relying on undocumented chat-only instructions.

**Acceptance criteria**

1. Required runtime versions are documented.
2. Configuration keys are documented.
3. Database/model setup steps are documented.
4. Known prerequisites are listed.

---

### NFR-TEST-001 — Requirement-linked tests

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

Tests that verify formal SRS requirements shall reference the applicable requirement ID where practical.

**Acceptance criteria**

1. Core MVP requirement tests contain IDs in names/docstrings/metadata.
2. Traceability matrix links requirements to tests.
3. Retired IDs are not silently reused for different behavior.

---

### NFR-TEST-002 — Deterministic rule tests

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Unit/integration test  

**Normative requirement**

Intrusion, loitering, crowd, duplicate-suppression, and camera-offline logic shall be testable using controlled deterministic inputs without requiring a live camera.

**Acceptance criteria**

1. Synthetic/recorded inputs can drive each rule.
2. Tests control timestamps/coordinates.
3. A rule failure can be reproduced.

---

### NFR-TEST-003 — Vertical-slice integration test

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §28  
**Verification:** Integration/system test  

**Normative requirement**

The project shall maintain at least one repeatable end-to-end or integration scenario covering video/AI result → rule → persisted event → operator-visible state → acknowledgement.

**Acceptance criteria**

1. The scenario is documented.
2. Each component boundary is exercised at an agreed fidelity.
3. Final demo uses the same or equivalent validated flow.

---

### NFR-USAB-001 — Event comprehension

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Usability/system test  

**Normative requirement**

The event UI shall allow an operator to determine the event type, source, occurrence time, current state, and available action without inspecting raw backend payloads.

**Acceptance criteria**

1. Required context is visibly presented.
2. The operator can open evidence where available.
3. Acknowledgement action is distinguishable from mere navigation.

---

### NFR-USAB-002 — Status distinction

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** UI system test  

**Normative requirement**

The UI shall visually or textually distinguish at minimum loading, empty, error, and valid-content states for core data views.

**Acceptance criteria**

1. A network error is not shown as zero events.
2. Loading is not shown as stale success.
3. An empty history is explicitly indicated.

---

### NFR-USAB-003 — Responsive minimum usability

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** System test  

**Normative requirement**

The core operator workflows shall remain usable at the desktop browser resolution selected for the academic demonstration.

**Clarification / constraints**

A broader responsive/mobile requirement is not in MVP.

**Acceptance criteria**

1. No critical action is inaccessible due to layout overflow.
2. Alert/event text remains readable.
3. Zone editor remains operable.

---

### NFR-OBS-001 — Structured diagnostic logging

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection + fault test  

**Normative requirement**

Backend and AI-worker logs shall include enough structured context to diagnose processing failures without exposing secrets.

**Acceptance criteria**

1. Logs identify component and time.
2. Relevant source/job/event identifiers are included where available.
3. Secrets/tokens are not intentionally logged.

---

### NFR-OBS-002 — Correlation identifier

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** System test  

**Normative requirement**

If processing is asynchronous or concurrent, the system shall use a correlation/job identifier that can trace a processing unit across worker and backend logs/contracts.

**Acceptance criteria**

1. A worker result can be correlated with originating processing request/source window.
2. The identifier is present in relevant diagnostics.
3. Two concurrent jobs do not share an accidental identifier.

---

### NFR-COMPAT-001 — Supported browser

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `SHOULD`  
**Source:** SEN-VS §18  
**Verification:** System test  

**Normative requirement**

The project shall document at least one browser/version family in which the final web application is verified for the demonstration.

**Acceptance criteria**

1. The browser family is named in deployment/operator docs.
2. Core flows are tested there.
3. The project does not claim universal browser support without testing.

---

### NFR-COMPAT-002 — Supported Python version

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Inspection  

**Normative requirement**

The backend and AI worker shall document the supported Python version used for development and final verification.

**Acceptance criteria**

1. The version is recorded.
2. Dependency installation is tested with that version.
3. The final report/setup guide uses the same version.

---

### NFR-DATA-001 — Unique stable identifiers

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Integration test  

**Normative requirement**

Persisted first-class entities that require cross-component reference shall have stable unique identifiers according to the database design.

**Acceptance criteria**

1. Events have unique IDs.
2. Camera/source IDs are stable.
3. IDs used in APIs map unambiguously to stored entities.

---

### NFR-DATA-002 — Timestamp consistency

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `TBD_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Integration test  

**Normative requirement**

The system shall use a documented time-zone and timestamp strategy for persisted event and audit times.

**Acceptance criteria**

1. Stored format/zone policy is documented.
2. Server and client agree on conversion semantics.
3. Occurrence-time ordering remains correct across UI/API.

---

### NFR-DATA-003 — Transactional event creation

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `PROPOSED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Integration test  

**Normative requirement**

Where event creation requires multiple persistent records that must remain mutually consistent, the persistence design shall use transactional or compensating behavior sufficient to avoid reporting a fully created event with missing mandatory state.

**Acceptance criteria**

1. Forced failure during dependent persistence does not leave an apparently successful but invalid event.
2. Success is reported only after mandatory state is durable.
3. Behavior is documented/tested for the chosen database.

---

### NFR-ACAD-001 — Measured claims only

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §48–49  
**Verification:** Document review  

**Normative requirement**

All quantitative claims in the final report or presentation that describe Sentinel performance shall be backed by recorded test or evaluation evidence.

**Acceptance criteria**

1. Reported accuracy/F1/mAP values correspond to actual Sentinel evaluation.
2. Reported latency/FPS values correspond to actual measured environment.
3. External-paper metrics are explicitly labeled as external comparison.

---

### NFR-ACAD-002 — Implemented-versus-proposed distinction

**Requirement lifecycle:** `DRAFT`  
**Scope status:** `CONFIRMED_SCOPE`  
**Priority:** `MUST`  
**Source:** SEN-VS §18  
**Verification:** Document review  

**Normative requirement**

Final documentation shall distinguish implemented, partially implemented, tested, deferred, and future-work capabilities.

**Acceptance criteria**

1. Deferred features are not listed as completed.
2. Mocked functionality is disclosed.
3. Known limitations are documented.

---


# 7. External Interface Requirements

## 7.1 User interface

The final UI specification shall define exact page structure.

At SRS level, the system shall provide interfaces sufficient for:

- monitoring configured sources;
- viewing event alerts;
- reviewing event details/evidence;
- acknowledging eligible events;
- searching historical events;
- viewing analytics;
- configuring zones/rules where the corresponding administrative features are baselined.

## 7.2 Backend application interface

The backend shall expose structured interfaces to the web frontend.

Exact:

- paths;
- HTTP methods;
- payload schemas;
- error schemas;
- real-time message names;

belong in `07-api-specification.md`.

## 7.3 AI-worker interface

The backend and AI worker shall exchange structured machine-readable data.

The contract must define at minimum, where relevant:

```text
source identity
processing/correlation identity
source/frame/window timestamp
model identity/version
result type
class/result
score/confidence
geometry
track identity
processing status/error
```

The exact schema remains an API/AI-design responsibility.

## 7.4 Camera/video interface

Supported input mode is `TBD`.

The SRS shall not claim RTSP, USB, file upload, webcam, or multi-protocol support until the team selects and implements the relevant mode.

## 7.5 Storage interface

The final architecture shall define:

- application database;
- evidence storage;
- model artifact storage;
- local dataset location.

No SRS requirement currently mandates cloud object storage.

---

# 8. Data Requirements

## 8.1 Required conceptual entities

The following conceptual records are expected, but exact schema belongs in `06-database-design.md`:

- user;
- role/permission;
- camera/source;
- zone;
- rule;
- detection or derived AI observation where persistence is required;
- track context where persistence is required;
- event;
- alert;
- evidence;
- acknowledgement;
- event status history;
- model/version;
- audit entry.

## 8.2 Data minimization

The database shall not persist raw frame-level detections indefinitely merely because they are available.

The AI/data design shall justify which low-level observations are persisted.

## 8.3 Historical interpretability

When configuration changes over time, historical events shall retain enough context to remain interpretable.

This may require:

- reference to immutable versioned configuration;
- snapshot fields;
- event metadata;

as decided by the database design.

## 8.4 Media integrity

Database metadata shall not claim that evidence exists when the media artifact is missing unless the metadata explicitly represents a missing/deleted/failed state.

---

# 9. State and Lifecycle Requirements

## 9.1 Event lifecycle

Exact event lifecycle is `TBD`.

Candidate states discussed in project governance include:

```text
OPEN
ACKNOWLEDGED
INVESTIGATING
RESOLVED
FALSE_POSITIVE
```

These are not yet baselined enum values.

The SRS shall not force implementation of this candidate state model until team acceptance.

## 9.2 Camera lifecycle

The system shall distinguish:

```text
intentionally disabled
```

from:

```text
enabled but offline/unhealthy
```

Exact state names remain design choices.

## 9.3 Rule lifecycle

At minimum:

- enabled;
- disabled;

must be representable if administrative rule configuration is implemented.

---

# 10. Error and Exception Requirements

## 10.1 Invalid user input

Invalid user input shall:

- be rejected;
- return a safe error;
- not partially persist invalid configuration.

## 10.2 Missing referenced entity

An operation referencing a nonexistent camera, zone, event, or rule shall produce a defined not-found/invalid-reference outcome.

Exact HTTP status codes belong in the API specification.

## 10.3 AI-worker failure

AI-worker failure shall be explicit and observable.

## 10.4 Database failure

The application shall not report successful persistence if the mandatory database operation failed.

## 10.5 Evidence failure

An event may still exist if evidence generation fails, but the evidence state shall not falsely indicate success.

## 10.6 Client connection failure

If a real-time connection fails, the UI shall not continue presenting itself as connected/live.

---

# 11. Requirements Traceability Seeds

The following mapping shall be expanded in `15-requirements-traceability.md`.

| Vision goal | Requirement families |
|---|---|
| G-01 Integrated workflow | FR-CAM, FR-DET, FR-TRK, FR-RULE, FR-EVT, FR-ALT |
| G-02 AI-assisted event extraction | MLR-DET, MLR-TRK, MLR-VIO |
| G-03 Deterministic event rules | FR-INT, FR-LOIT, FR-CROWD |
| G-04 Web operator interaction | FR-UI, FR-ALT, FR-HIST, FR-ANL |
| G-05 Evidence-linked records | FR-EVD |
| G-06 Academic traceability | NFR-TEST, NFR-ACAD |
| G-07 Reproducible AI | MLR-DATA, MLR-EXP, MLR-MOD |
| G-08 Responsible claims | NFR-ACAD, NFR-PRIV |

---

# 12. MVP Verification Matrix

The following is a minimum system-level verification plan.

| MVP capability | Minimum verification |
|---|---|
| Person detection | recorded-video AI-worker test |
| Person tracking | representative continuity test |
| Restricted intrusion | deterministic coordinate + integration test |
| Loitering | controlled-time rule test |
| Crowd threshold | deterministic count/threshold test |
| Violence/fighting | formal held-out evaluation + integration test |
| Camera offline | forced source failure test |
| Alert generation | backend + client integration test |
| Evidence | snapshot/clip association test |
| Acknowledgement | authenticated persistence test |
| History/search | query/filter tests |
| Analytics | persisted-data aggregation comparison |

---

# 13. Open Requirement Decisions

These must be resolved before the affected requirements become `BASELINED`.

| Decision ID | Question | Affected requirements |
|---|---|---|
| RD-001 | Which frontend framework? | UI implementation; not most behavioral requirements |
| RD-002 | PostgreSQL or alternative DB? | persistence/deployment details |
| RD-003 | Authentication mechanism? | FR-AUTH, NFR-SEC |
| RD-004 | Exact roles and permissions? | FR-USER, protected operations |
| RD-005 | Primary MVP video input? | FR-CAM, AI worker |
| RD-006 | Detector/model library? | MLR-DET, licensing |
| RD-007 | Tracker? | MLR-TRK, loitering |
| RD-008 | Violence dataset? | MLR-VIO/DATA |
| RD-009 | Violence architecture? | MLR-VIO |
| RD-010 | Worker/backend transport? | FR-INTG |
| RD-011 | Evidence storage? | FR-EVD |
| RD-012 | Event/incident relationship? | FR-INC |
| RD-013 | Event lifecycle? | FR-EVT |
| RD-014 | Intrusion geometry method? | FR-INT |
| RD-015 | Loitering threshold/reset? | FR-LOIT |
| RD-016 | Crowd counting semantics/threshold? | FR-CROWD |
| RD-017 | Real-time transport? | FR-ALT, NFR-REL |
| RD-018 | Camera offline timeout/criteria? | FR-CAM |
| RD-019 | Evidence pre/post-roll duration? | FR-EVD |
| RD-020 | Timestamp/time-zone strategy? | NFR-DATA |
| RD-021 | Retention period? | NFR-PRIV, FR-EVD |

---

# 14. Requirements Baseline Checklist

Before changing this SRS to `BASELINED`, the team shall review:

- [ ] Each `MUST` requirement is feasible within the 2–3 week window.
- [ ] No requirement accidentally introduces a deferred feature.
- [ ] Authentication/authorization decisions are resolved or explicitly excluded from baseline.
- [ ] Camera/video input is resolved.
- [ ] Detector/tracker candidate is resolved.
- [ ] Violence dataset/model approach is feasible.
- [ ] Worker/backend contract is defined.
- [ ] Database choice is resolved.
- [ ] Intrusion geometry semantics are resolved.
- [ ] Loitering threshold/reset/retrigger semantics are resolved.
- [ ] Crowd counting/threshold semantics are resolved.
- [ ] Camera-offline semantics are resolved.
- [ ] Evidence storage and clip policy are resolved.
- [ ] Event/incident lifecycle is resolved.
- [ ] Every quantitative target has a source or remains `TBD`.
- [ ] Every `MUST` requirement has a verification method.
- [ ] Requirement IDs are stable.
- [ ] No API endpoint or DB column is implied without its own design document.
- [ ] The team agrees that unimplemented requirements will be disclosed rather than faked.

---

# 15. Requirement Statistics

This draft contains the following generated requirement groups:

- Functional requirements: **88**
- AI/ML requirements: **25**
- Non-functional requirements: **42**
- Total formal requirements: **155**

These counts are informational and shall be updated automatically or manually if the document changes.

---

# 16. Source Notes

## 16.1 Project sources

Primary internal sources:

- `PROJECT_HANDBOOK.md`
- `01-vision-and-scope.md`

## 16.2 Requirements engineering

ISO/IEC/IEEE 29148:2018  
Systems and software engineering — Life cycle processes — Requirements engineering

Official source:

https://www.iso.org/standard/72089.html

Use in this SRS:

- disciplined requirements structure;
- verifiability;
- traceability;
- separation of requirement from implementation where practical.

The project does not claim formal certification.

---

# 17. Final SRS Rule

> **A requirement is not complete merely because it sounds plausible.**
>
> Every baselined Sentinel requirement must be:
>
> - necessary;
> - understandable;
> - sufficiently unambiguous;
> - feasible;
> - verifiable;
> - traceable;
> - consistent with scope;
> - honest about unresolved values.
>
> If a developer or AI assistant must invent a threshold, field, status, role permission, transport, dataset, or model behavior to implement a requirement, then that requirement or its supporting design decision is not yet sufficiently specified.
