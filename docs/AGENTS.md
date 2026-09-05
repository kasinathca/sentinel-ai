---
title: "Sentinel AI — AI Agent Operating Contract"
document_id: "SEN-AGENT"
version: "0.1.0"
status: "DRAFT_FOR_TEAM_REVIEW"
project: "Sentinel AI"
applies_to:
  - "GPT"
  - "Claude"
  - "Codex"
  - "GitHub Copilot agents"
  - "other autonomous or semi-autonomous coding assistants"
last_updated: "2026-09-05"
---

# Sentinel AI — `AGENTS.md`

> **Purpose**
>
> This file defines mandatory operating rules for any AI assistant working on the Sentinel AI repository.
>
> It is intentionally strict.
>
> An AI assistant is an implementation aid, not a product owner, architect of record, requirements authority, data-governance authority, or source of academic truth.

---

## 1. Read This Before Doing Anything

Before modifying code, configuration, tests, data contracts, documentation, dependencies, schemas, or model logic:

1. Read `PROJECT_HANDBOOK.md`.
2. Read the specification(s) relevant to the requested change.
3. Identify all affected contracts.
4. Identify unresolved `TBD`, `PROPOSED`, `DEFERRED`, or `REJECTED` items.
5. Inspect existing implementation before proposing replacement code.
6. Inspect tests before changing observable behavior.
7. Do not assume missing project details from conventions or personal preference.

If any of these files are missing, do **not** fabricate their contents.

Report the missing source of truth and proceed only within the boundaries that are actually documented.

---

# 2. Authority Order

When determining project behavior, use the following source-of-truth hierarchy.

## 2.1 Scope and governance

Primary:

- `PROJECT_HANDBOOK.md`
- `docs/01-vision-and-scope.md`

These define what Sentinel AI is and what is in or out of scope.

## 2.2 Requirements

Primary:

- `docs/02-srs.md`

This is the authoritative source for mandatory system behavior.

## 2.3 Use-case behavior

Primary:

- `docs/03-use-case-specification.md`

## 2.4 Architecture

Primary:

- accepted ADRs in `docs/adr/`
- `docs/04-system-architecture.md`

## 2.5 System models

Primary:

- `docs/05-uml-and-system-models.md`

## 2.6 Database

Primary:

- `docs/06-database-design.md`

## 2.7 API / message contracts

Primary:

- `docs/07-api-specification.md`

## 2.8 AI / ML behavior

Primary:

- `docs/08-ai-ml-design.md`

## 2.9 Dataset acquisition

Primary:

- `docs/09-dataset-acquisition.md`

## 2.10 Dataset actually used

Primary:

- `docs/10-dataset-registry.md`

## 2.11 Model identity and measured results

Primary:

- `docs/11-model-card-and-evaluation.md`

## 2.12 UI behavior

Primary:

- `docs/12-ui-ux-specification.md`

## 2.13 Security and privacy

Primary:

- `docs/13-security-and-privacy.md`

## 2.14 Testing

Primary:

- `docs/14-test-plan.md`
- `docs/15-requirements-traceability.md`

## 2.15 Deployment

Primary:

- `docs/16-deployment-guide.md`

## 2.16 Operator behavior

Primary:

- `docs/17-operator-manual.md`

## 2.17 Final academic claims

Primary:

- `docs/18-final-technical-report.md`

The technical report shall reflect verified implementation and measured results. It does not override the actual requirements/design documents.

---

# 3. Conflict Rule

If authoritative sources conflict:

**STOP.**

Do not decide which document is "probably correct."

Report:

1. the conflicting files;
2. the exact conflicting statements;
3. the implementation areas affected;
4. a proposed resolution;
5. which authoritative document should be updated if the team accepts the resolution.

Do not implement behavior that silently resolves a specification conflict.

---

# 4. Decision Status Vocabulary

Interpret these labels strictly.

| Status | Meaning | Agent behavior |
|---|---|---|
| `CONFIRMED` | accepted project decision | may implement |
| `PROPOSED` | candidate awaiting acceptance | may discuss/prototype only when clearly isolated |
| `TBD` | unresolved | do not guess |
| `DEFERRED` | intentionally postponed | do not implement |
| `REJECTED` | explicitly excluded | do not implement |
| `EXPERIMENTAL` | isolated experiment | do not promote to production contract without approval |

## 4.1 `TBD` handling

When a required implementation detail is `TBD`, do not fill it with a plausible value.

Bad:

```text
The requirement has no threshold, so use 30 seconds.
```

Correct:

```text
ASSUMPTION REQUIRING APPROVAL:
The current specification does not define the loitering duration threshold.
Implementation cannot safely hard-code a production value.
```

## 4.2 Proposal language

When proposing a design not yet accepted, prefix it clearly:

```text
PROPOSED:
```

or:

```text
ASSUMPTION REQUIRING APPROVAL:
```

Never present a suggestion as if it already exists in the project.

---

# 5. Project Architecture That Must Not Be Silently Replaced

The following architecture is already accepted.

## 5.1 Confirmed

- FastAPI backend.
- Modular-monolith application architecture.
- Separate AI worker.
- AI worker shall not be embedded as long-running inference inside ordinary web request handlers.
- Rule-driven events shall be separated from raw detections.
- Facial recognition is excluded from the MVP.
- Deferred features shall not be implemented without explicit scope reopening.

Do not replace this with:

- a full microservice architecture;
- serverless-only architecture;
- Node-only backend;
- frontend-direct-to-model calls;
- model inference inside every HTTP request;
- arbitrary cloud services;
- a monolithic file containing routes, database, rules, and inference logic.

If an architectural change appears necessary, propose an ADR. Do not implement the new architecture first.

---

# 6. MVP Capability Boundary

Current MVP capabilities:

- person detection;
- person tracking;
- restricted-area intrusion;
- loitering;
- crowd threshold;
- violence/fighting;
- camera-offline detection;
- alert generation;
- evidence snapshots/clips;
- operator acknowledgement;
- incident/event history and search;
- analytics dashboard.

Deferred:

- fall detection;
- fire/smoke detection;
- sound anomaly detection;
- SMS/email notifications;
- PWA/mobile interface;
- multiple-site monitoring.

Rejected for MVP:

- facial recognition / identity recognition.

AI assistants must not expand the MVP because a library makes a deferred feature easy.

---

# 7. Core Domain Separation

The following concepts must not be collapsed into one object without an approved design change:

```text
Frame
Detection
Track
Zone
Rule
Event
Alert
Evidence
Incident
Acknowledgement
Audit entry
Model result
```

## 7.1 Detection is not an event

A person detection is a low-level observation.

Example:

```text
class = person
confidence = ...
bbox = ...
```

It does **not** automatically mean:

- intrusion;
- loitering;
- violence;
- suspicious behavior;
- crime;
- unauthorized access.

## 7.2 Track is not identity

A track ID such as:

```text
track_id = 17
```

must never be interpreted as a real-world human identity.

## 7.3 Rule output is not legal truth

A generated `RESTRICTED_AREA_INTRUSION` event means a configured system rule was satisfied.

It does not prove criminal intent or legal wrongdoing.

## 7.4 Violence result must remain model-scoped

A violence/fighting output must identify the model/version that produced it where the approved contract requires this.

Do not present uncalibrated model scores as universal probabilities.

---

# 8. No Hallucination Rules

An AI assistant shall never fabricate any of the following.

## 8.1 APIs

Never invent:

- endpoint paths;
- request fields;
- response fields;
- WebSocket event names;
- status codes;
- authentication headers;
- pagination rules;
- error codes.

If not specified, label as unresolved.

## 8.2 Database

Never invent:

- table names;
- columns;
- data types;
- constraints;
- foreign keys;
- enum values;
- indexes;
- migrations.

A proposed schema must be labeled `PROPOSED` until accepted.

## 8.3 Requirements

Never invent:

- requirement IDs;
- mandatory behavior;
- performance thresholds;
- role permissions;
- alert severity logic;
- retention periods;
- timeout values;
- duplicate cooldowns.

## 8.4 AI/ML

Never invent:

- model architecture;
- accuracy;
- precision;
- recall;
- F1-score;
- mAP;
- FPS;
- inference latency;
- class counts;
- dataset size;
- train/validation/test split;
- augmentation;
- hyperparameters;
- GPU type;
- training duration;
- model license.

## 8.5 Research and citations

Never invent:

- papers;
- authors;
- DOI values;
- official URLs;
- dataset licenses;
- publication dates;
- standard clauses.

If an external fact matters and cannot be verified, state that it requires verification.

## 8.6 Testing

Never write:

```text
All tests pass.
```

unless tests were actually executed and the result was observed.

If tests were not run:

```text
Tests not executed.
```

If only some tests were run:

```text
Executed:
- ...

Not executed:
- ...
```

## 8.7 Runtime state

Never claim:

- server is running;
- database migrated;
- camera connected;
- worker running;
- model downloaded;
- package installed;

unless verified from actual environment output.

---

# 9. Before Editing Code

For every non-trivial change, inspect:

1. target file;
2. directly related module;
3. tests for the affected behavior;
4. public/internal interfaces used by other components;
5. relevant specification;
6. relevant ADR;
7. configuration/dependency metadata if applicable.

Do not replace a function merely from its name without reading how it is used.

---

# 10. Change Scope Rule

Make the smallest coherent change that satisfies the request.

Do not combine:

- feature implementation;
- framework migration;
- formatting changes;
- unrelated renaming;
- dependency upgrades;
- broad refactoring;

unless explicitly requested and justified.

Broad AI-generated refactors are particularly risky in a 2–3 week project.

---

# 11. Dependency Rule

Do not add a dependency merely because it makes implementation easier.

Before proposing a major dependency, identify:

```text
Name
Purpose
Version
Official source
License
Why existing dependencies are insufficient
Security implications
Bundle/runtime impact where relevant
Alternative considered
```

## 11.1 AI/model licensing

Before installing or integrating an AI framework or model:

1. verify package license;
2. verify pretrained weight/model license;
3. verify dataset usage terms;
4. identify redistribution restrictions;
5. record decision in docs/ADR where significant.

Do not assume that "open source" means "no obligations."

## 11.2 Ultralytics-specific rule

Ultralytics/YOLO may be evaluated technically, but it is **not automatically approved**.

Its licensing must be reviewed before adoption.

Do not silently add `ultralytics` to project dependencies unless the corresponding decision has been accepted.

---

# 12. Dataset Rule

## 12.1 Acquisition

Datasets shall be acquired only according to:

- `docs/09-dataset-acquisition.md`

## 12.2 Registry

The exact dataset used shall be recorded in:

- `docs/10-dataset-registry.md`

## 12.3 No silent mirrors

If an official dataset is unavailable:

- do not silently use a random mirror;
- record provenance;
- verify terms;
- distinguish original source from mirror;
- document any uncertainty.

## 12.4 Never commit large datasets

By default, do not commit:

- dataset archives;
- raw surveillance video;
- processed training sets;
- large model artifacts.

Use local paths / documented acquisition / registries.

## 12.5 Evaluation integrity

Do not:

- train on test data;
- tune repeatedly on test data;
- mix duplicate clips across train/test;
- report training metrics as test metrics;
- cherry-pick examples and call them evaluation.

---

# 13. AI Experiment Rule

Every meaningful model experiment should be reproducible.

Record:

```text
experiment_id
purpose
date
code_commit
dataset_id
split
preprocessing
augmentation
base_model
weights_source
hyperparameters
seed
hardware
metrics
artifact_location
notes
```

If a value is unknown:

```text
TBD
```

Do not fabricate completeness.

---

# 14. Model Integration Rule

A model is not integrated merely because inference runs.

Before calling model integration complete, verify:

1. model artifact loads reproducibly;
2. input preprocessing is defined;
3. output schema is defined;
4. confidence/score semantics are defined;
5. failure behavior is defined;
6. model version is traceable;
7. backend/worker contract is tested;
8. performance is measured in the actual target environment;
9. limitations are documented.

---

# 15. Worker Rules

The AI worker owns AI/video-processing responsibilities.

It may include:

- frame preprocessing;
- detector inference;
- tracking;
- violence/fighting inference;
- AI result serialization;
- model loading;
- model health.

It must not own:

- user authentication;
- role authorization;
- user management;
- frontend routing;
- incident policy;
- arbitrary database writes;
- product requirement decisions.

## 15.1 Worker failure

If the worker fails:

- report failure explicitly;
- do not fabricate empty successful results;
- backend should not treat missing inference as "no incident" unless specification explicitly says so.

---

# 16. FastAPI Backend Rules

## 16.1 Separation

Prefer:

```text
route/controller
    ↓
application/service layer
    ↓
domain/repository boundary
    ↓
persistence
```

Avoid route handlers containing:

- direct model inference;
- large SQL blocks;
- complex rule engines;
- evidence-generation internals;
- authorization rules duplicated in multiple endpoints.

## 16.2 Validation

Validate:

- path/query/body input;
- enum-like values;
- identifiers;
- file metadata where applicable;
- zone geometry;
- timestamps;
- worker payload schema.

Do not trust frontend validation as security.

## 16.3 Error responses

Do not expose:

- stack traces;
- environment variables;
- database credentials;
- model paths containing sensitive info;
- internal secrets.

---

# 17. Database Rules

Until `docs/06-database-design.md` is baselined:

- schema changes are proposals;
- do not treat inferred entities as final.

Once migrations are established:

- use migration tooling;
- do not edit applied shared migrations casually;
- do not manually mutate shared/demo database schema without documenting it.

## 17.1 Media storage

Do not store large video clips as database BLOBs unless an accepted architecture decision requires it.

Default conceptual direction:

```text
database -> media metadata/reference
storage -> actual media
```

but exact implementation remains subject to design approval.

---

# 18. Frontend Rules

Frontend technology remains `TBD` until accepted.

Regardless of framework:

- do not hard-code fake analytics in production views;
- do not hard-code alert/event examples as if they are live data;
- do not enforce authorization only in UI;
- handle loading/error/empty states;
- distinguish disconnected/live states;
- do not swallow backend errors;
- do not invent API fields.

If mock data is used during development, it must be clearly isolated and removable.

---

# 19. Real-Time Communication Rules

WebSockets are currently a proposed approach.

Do not invent the final real-time contract before `docs/07-api-specification.md` defines it.

The final design should explicitly address:

- authentication;
- connection lifecycle;
- reconnection;
- duplicate messages;
- stale events;
- ordering assumptions;
- event identifiers;
- schema versioning;
- authorization.

Do not assume WebSocket messages are guaranteed exactly once.

---

# 20. Event and Alert Rules

## 20.1 Event creation

An event should result from:

- a defined deterministic rule;
- a defined model condition;
- a defined system-health condition.

Not from vague AI interpretation.

## 20.2 Duplicate suppression

Video produces repeated observations.

Do not create one event per frame unless the SRS explicitly requires it.

The design must define:

- opening condition;
- duplicate suppression;
- cooldown;
- persistence;
- closing condition;
- re-trigger behavior.

If values are not specified, keep them `TBD`.

## 20.3 Acknowledgement

Acknowledgement must be persistent and authenticated if the SRS requires it.

Do not implement acknowledgement as a frontend-only state change.

---

# 21. Security Rules

Security requirements shall be informed by project security documentation and relevant OWASP guidance.

Mandatory baseline:

1. do not commit secrets;
2. do not return secrets through APIs;
3. do not log passwords/tokens;
4. enforce authorization server-side;
5. validate untrusted input;
6. protect media/evidence routes;
7. restrict file uploads if present;
8. use safe path handling;
9. avoid debug exposure in final deployment;
10. pin dependency versions;
11. use principle of least privilege where practical.

If a requested change weakens security to "make it work," reject that approach and propose a safe alternative.

---

# 22. Privacy Rules

Camera/video content may contain identifiable individuals even without facial recognition.

Therefore:

- do not expose footage publicly by default;
- do not commit sensitive footage;
- do not use real-world private CCTV clips without documented permission/legitimate source;
- do not add facial recognition;
- do not create biometric profiles;
- do not infer protected or sensitive personal attributes from appearance;
- document retention/access where evidence is stored.

---

# 23. Logging Rules

Logs may include:

- timestamp;
- component;
- correlation/job ID;
- event ID;
- camera ID;
- error code;
- operation status.

Logs must not intentionally include:

- passwords;
- full access tokens;
- API keys;
- unnecessary PII;
- raw video frames;
- secret camera URLs.

---

# 24. Time and Timestamp Rules

Do not casually mix:

- camera source time;
- frame timestamp;
- server receive time;
- inference completion time;
- event creation time;
- persistence time;
- client display time.

The approved timestamp semantics must be documented.

Until then, preserve source timestamps rather than silently converting or overwriting them.

---

# 25. Testing Rules

## 25.1 Requirement linkage

When a test verifies a formal requirement, reference the requirement ID.

Example:

```python
def test_acknowledgement_requires_authorized_user():
    """Verifies FR-ALT-XXX."""
```

## 25.2 Test levels

Use applicable layers:

- unit;
- module/service;
- API;
- DB integration;
- AI worker;
- worker/backend contract;
- frontend;
- end-to-end;
- security;
- performance;
- AI evaluation.

## 25.3 No false test claims

Do not mark work complete based on:

- static reading only;
- generated tests that were never executed;
- one happy-path manual run;
- mocked behavior when the requirement concerns real integration.

## 25.4 Failure tests

Test relevant failures, including:

- worker unavailable;
- invalid camera;
- malformed payload;
- unauthorized acknowledgement;
- duplicate event input;
- invalid zone;
- database failure handling where feasible;
- evidence write failure where feasible.

---

# 26. Definition of Done Enforcement

Before describing a feature as "done," check the applicable requirements from `PROJECT_HANDBOOK.md`.

At minimum:

- behavior implemented;
- acceptance criteria met;
- tests executed;
- docs updated;
- interfaces synchronized;
- security implications reviewed;
- no hidden `TBD` assumptions;
- no fabricated metrics;
- no scope creep.

For AI features additionally:

- model identified;
- dataset identified;
- evaluation recorded;
- limitation recorded;
- license checked.

---

# 27. Vertical Slice Priority

The first integrated milestone is:

```text
video
↓
AI worker detects/tracks person
↓
structured result reaches backend
↓
restricted-zone rule evaluates
↓
event persists
↓
frontend receives/displays alert
↓
operator acknowledges
↓
acknowledgement persists
```

When choosing between polishing an isolated component and making this slice work, prefer the integrated slice unless the team explicitly changes priority.

---

# 28. 2–3 Week Delivery Discipline

This is a short project.

Agents shall avoid:

- premature abstractions;
- speculative architecture;
- unnecessary design patterns;
- framework migrations;
- elaborate plugin systems;
- implementing all future features;
- complex distributed infrastructure.

Prefer:

- clear module boundaries;
- small explicit contracts;
- reproducible setup;
- integrated MVP;
- deterministic tests;
- documented limitations.

---

# 29. Performance Claims

Never use terms such as:

- real-time;
- low latency;
- high accuracy;
- scalable;
- robust;
- production ready;

as measured claims unless supported by defined tests.

If used descriptively in project intent, clearly distinguish that from measured performance.

## 29.1 Measurement context

Any measured performance value should record:

```text
hardware
OS
runtime
CPU
GPU
memory, if relevant
video resolution
input FPS
model
model input resolution
stream count
software commit
measurement method
```

---

# 30. Academic Integrity

Agents shall preserve a truthful distinction between:

- team-authored implementation;
- third-party library use;
- pretrained model use;
- fine-tuning;
- external datasets;
- external code samples;
- proposed future work;
- actual measured results.

## 30.1 Prohibited wording

Do not write:

> "We trained the model from scratch"

if pretrained weights were used.

Do not write:

> "Sentinel detects crime"

unless the system actually contains a rigorously defined, validated capability matching that claim.

Preferred wording:

> "Sentinel detects configured surveillance events and model-classified behaviors for operator review."

Do not write:

> "The system is 95% accurate"

without an actual defined metric and test set.

---

# 31. Documentation Editing and Synchronization Rules

Documentation is part of the implementation contract, not a later reporting task.

## 31.1 Repository source of truth

The current GitHub repository version of a project document is the authoritative working copy.

ChatGPT Project uploads, exported files, pasted copies, and local snapshots may be used as historical/reference material, but they shall **not** override a newer repository version merely because they are available in an assistant context.

Before editing an authoritative document, an AI assistant shall:

1. fetch/read the current repository copy;
2. compare the requested change against the current source-of-truth hierarchy;
3. make the smallest coherent documentation change;
4. preserve existing requirement IDs, experiment IDs, decision statuses, and traceability unless an explicit controlled change requires otherwise.

## 31.2 Mandatory documentation-impact pass

After any of the following becomes factually established:

- implementation behavior changes;
- an experiment completes;
- a dataset is acquired, derived, split, activated, retired, or invalidated;
- a model is trained, evaluated, selected, rejected, or re-qualified;
- a test is executed;
- an ADR is accepted;
- a deployment/runtime decision is fixed;
- measured performance or security evidence changes;

perform a documentation-impact pass before the task is considered complete.

The pass shall:

1. identify every authoritative document materially affected;
2. update only those documents;
3. leave unaffected documents unchanged;
4. distinguish `CONFIRMED`, `PROPOSED`, `TBD`, `EXPERIMENTAL`, measured, and not-yet-verified state accurately;
5. update `15-requirements-traceability.md` when verification evidence changes;
6. update `18-final-technical-report.md` only with claims supported by authoritative evidence;
7. record unresolved incompatibilities rather than smoothing them over;
8. commit the documentation changes with a descriptive message when repository write access is available.

## 31.3 Documentation-complete rule

A coding, dataset, model, experiment, or testing task is **not documentation-complete** merely because code or artifacts exist.

Completion requires one of:

```text
DOCUMENTATION IMPACT: UPDATED
```

with the affected files listed, or:

```text
DOCUMENTATION IMPACT: NONE
```

with a short reason.

Do not rewrite documentation after the fact merely to legitimize accidental implementation. If implementation conflicts with a baselined contract, report the conflict and follow the conflict/change-control rules instead.

---

# 32. ADR Rule

Create/propose an ADR for decisions involving:

- database selection;
- detector selection;
- tracker selection;
- violence-model selection;
- worker transport;
- real-time transport;
- media storage;
- authentication strategy;
- major dependency;
- deployment architecture;
- licensing implications.

An ADR must contain:

- context;
- decision;
- alternatives;
- consequences;
- status;
- date;
- references where relevant.

---

# 33. Pull Request / Change Summary Format

When an AI agent prepares a change, summarize:

```md
## Purpose

...

## Requirements

- FR-...
- NFR-...

## Files Changed

- ...

## Contract Changes

API:
- None / ...

Database:
- None / ...

Worker:
- None / ...

## Tests Executed

- ...

## Test Results

- ...

## Documentation Updated

- ...

## Known Limitations

- ...

## Decisions Needed

- None / ...
```

Do not hide decisions needed inside prose.

---

# 34. Code Quality Rules

Prefer code that is:

- readable;
- typed where practical;
- explicit;
- testable;
- modular;
- unsurprising.

Avoid cleverness that makes a short academic project harder to maintain.

## 34.1 Comments

Comments should explain:

- why;
- assumptions;
- invariants;
- external constraints.

Do not comment every obvious line.

## 34.2 Naming

Use domain terminology from project specifications.

Do not alternate between:

```text
incident
event
alert
anomaly
warning
```

as interchangeable words unless the domain model explicitly makes them equivalent.

---

# 35. Configuration Defaults

Do not invent production defaults for unresolved thresholds.

Examples requiring explicit specification:

- loitering seconds;
- crowd threshold count;
- event cooldown;
- evidence pre-roll;
- evidence post-roll;
- camera-offline timeout;
- confidence thresholds;
- WebSocket heartbeat;
- session lifetime;
- retention period.

Temporary development defaults must be clearly labeled and must not be presented as requirements.

---

# 36. Mocking Rules

Mocks are allowed for:

- isolated unit tests;
- frontend development before backend contract exists;
- worker contract testing;
- fault injection.

Mocks are not acceptable evidence that:

- real model integration works;
- real persistence works;
- actual WebSocket integration works;
- actual camera input works;
- actual evidence generation works.

Label mock/demo mode clearly.

---

# 37. Demo Integrity

The final demonstration shall not fake unavailable functionality.

Do not:

- play a prerecorded video while showing unrelated hard-coded alerts;
- show static dashboard metrics as live analytics without labeling them;
- manually inject a model result and claim live model detection unless injection mode is disclosed;
- hide errors to make the UI appear successful.

If a subsystem is incomplete, document it as a limitation.

---

# 38. Camera Input Rule

The first supported input type is still `TBD`.

Do not build support for every possible source simultaneously.

Once selected, keep at least one deterministic recorded-video test path where feasible so that event behavior can be reproduced.

---

# 39. Analytics Rule

Analytics must be derived from real persisted project data or clearly labeled demonstration fixtures.

Do not generate arbitrary numbers to make charts attractive.

Every chart should have:

- clear metric definition;
- correct time range;
- correct grouping;
- meaningful labels;
- empty-state behavior.

---

# 40. Evidence Rule

Evidence may include:

- snapshot;
- short video clip;
- metadata.

Exact storage is unresolved.

Agents shall not assume:

- local disk;
- cloud object storage;
- DB blob;
- fixed clip duration;

without an accepted design.

---

# 41. Human Feedback Rule

If operator false-positive feedback is implemented:

- store it as operator feedback;
- do not automatically retrain from it;
- do not treat one click as validated training ground truth;
- preserve model/version/event association.

Online self-learning is outside MVP.

---

# 42. Model Update Rule

A model update must be identifiable and reversible where practical.

Record:

- model ID;
- version;
- artifact;
- base weights;
- dataset;
- configuration;
- metrics;
- date;
- code commit.

Do not overwrite `model.pt` repeatedly without provenance.

---

# 43. Repository Hygiene

Do not commit:

- `.env`;
- secrets;
- database dumps containing sensitive data;
- huge model binaries by default;
- raw research datasets;
- large surveillance videos;
- local virtual environments;
- generated caches;
- IDE-specific junk unless team-approved.

Do commit:

- `.env.example`;
- dependency manifests;
- migrations;
- reproducibility scripts;
- dataset manifests/metadata;
- model registry metadata;
- tests;
- docs.

---

# 44. Commands and Environment

Project-specific run/test/build commands shall be added only after the repository actually defines them.

Until then, do not invent commands such as:

```text
make start
docker compose up
npm run dev
pytest
```

as guaranteed project commands.

Once established, document verified commands here.

## 44.1 Verified backend commands

`TBD`

## 44.2 Verified AI worker commands

`TBD`

## 44.3 Verified frontend commands

`TBD`

## 44.4 Verified full-stack commands

`TBD`

---

# 45. Agent Response Discipline

When asked to implement a change, an AI assistant should report:

1. what it inspected;
2. what authoritative requirements apply;
3. what it changed;
4. tests executed;
5. unresolved questions;
6. deviations from specification, if any.

Do not bury failures.

---

# 46. Refusal Conditions for the Agent

An agent should refuse to silently proceed when asked to:

- fabricate metrics;
- fake test results;
- cite nonexistent research;
- claim unimplemented features;
- bypass authentication;
- commit real secrets;
- use private footage without authority;
- add facial recognition to the MVP without scope change;
- train on the formal test set and report it as independent evaluation;
- ignore incompatible licensing;
- rewrite requirements simply to fit already-written code.

The correct behavior is to explain the conflict and propose a compliant path.

---

# 47. Initial Open Decisions

Do not resolve these by inference:

| ID | Decision | Status |
|---|---|---|
| OD-001 | Frontend framework | `TBD` |
| OD-002 | Database technology | `PROPOSED: PostgreSQL` |
| OD-003 | Authentication approach | `TBD` |
| OD-004 | User roles/permissions | `PROPOSED` |
| OD-005 | MVP video input protocol | `TBD` |
| OD-006 | Detector model/library | `TBD` |
| OD-007 | Tracker implementation | `TBD` |
| OD-008 | Violence dataset | `TBD` |
| OD-009 | Violence model architecture | `TBD` |
| OD-010 | Worker/backend transport | `TBD` |
| OD-011 | Evidence storage | `TBD` |
| OD-012 | Event/incident relationship | `TBD` |
| OD-013 | Event state machine | `PROPOSED` |
| OD-014 | Rule threshold semantics | `TBD` |
| OD-015 | Real-time client transport | `PROPOSED: WebSocket` |
| OD-016 | Repository license | `TBD` |
| OD-017 | Deployment target | `TBD` |
| OD-018 | Team role assignments | `TBD` |

---

# 48. Stop Conditions Before Major Implementation

An AI agent shall stop and request/flag a decision when the requested work depends materially on:

- an undefined API contract;
- an undefined DB schema;
- an undefined security model;
- an undefined dataset;
- an undefined model architecture;
- an unresolved license;
- a direct conflict in authoritative docs;
- a deferred/rejected capability.

Small isolated scaffolding may be proposed, but must not encode the unresolved choice as fact.

---

# 49. Baseline Integration Priority

If priorities conflict, protect the first end-to-end slice:

```text
video
→ AI result
→ backend rule
→ persisted event
→ client notification
→ operator acknowledgement
→ persisted acknowledgement
```

This vertical slice has priority over:

- visual polish;
- additional analytics;
- deferred features;
- premature optimization;
- complex model-management UI;
- elaborate deployment architecture.

---

# 50. Final Rule

> **Never make Sentinel AI look more complete than it actually is.**
>
> The repository must remain a truthful engineering record.
>
> If something is unknown, write `TBD`.
>
> If something is proposed, write `PROPOSED`.
>
> If something failed, report the failure.
>
> If something was not tested, say it was not tested.
>
> If a model is pretrained, say it is pretrained.
>
> If a dataset is externally sourced, cite the original source.
>
> If the specification conflicts with the implementation, resolve the conflict explicitly.
>
> Accuracy of the engineering record is more important than making the project appear sophisticated.

