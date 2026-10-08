---
title: "Sentinel AI — Single-Camera Virtual CCTV Replay Integration"
document_id: "SEN-VCAM-REPLAY"
version: "1.0.0"
status: "CONFIRMED_TARGET_BASELINE"
project: "Sentinel AI"
academic_context: "Advanced Web Technologies course project"
last_updated: "2026-10-07"
decision_owner: "Project team"
authoritative_for:
  - "single-camera input scope"
  - "virtual CCTV replay behavior"
  - "looping recorded-video behavior"
  - "demo-controller separation"
  - "camera-source abstraction"
  - "demo media registration"
  - "virtual-camera API target"
  - "virtual-camera acceptance criteria"
---

# Sentinel AI — Single-Camera Virtual CCTV Replay Integration

## 0. Authority and implementation status

This document records an explicitly accepted project decision for the academic Sentinel AI system.

The decision is **authoritative as a target requirement and architecture baseline**.

It does **not** claim that every behavior in this document is already implemented. Implementation status shall be recorded only after code, tests, and integration evidence exist.

Where this document conflicts with older planning text that assumed physical CCTV access, multiple cameras, a camera selector, or RTSP/IP-camera availability for the academic demonstration, this document supersedes those assumptions for the current academic baseline.

The frozen violence model and its qualified evidence remain governed by `19-violence-model-and-runtime-qualification.md`.

---

# 1. Decision Summary

Sentinel AI shall use **one logical camera only** for the academic project.

The project does not require access to a physical CCTV installation.

Instead, a controlled local recorded video shall be presented to the application through a **looping virtual CCTV source**.

The selected video behaves as the active camera feed:

```text
approved local video file
        ↓
single virtual CCTV source
        ↓
camera-source abstraction
        ↓
AI worker + backend processing
        ↓
normal Sentinel operator panel
```

The file is selected from a **separate Demo Control Panel**.

The Demo Control Panel may know the source is a local recorded file. The downstream operational pipeline shall not require special business logic based on whether the source originated from a file or physical camera hardware.

When the selected video reaches EOF while the virtual camera is active, playback shall automatically restart from the beginning and continue until the operator stops or changes the source.

---

# 2. Scope Decisions

## 2.1 Exactly one camera

The academic baseline supports exactly one camera.

Canonical display identity:

```text
DEMO-CAM-01
```

The backend may continue to use a UUID internally when required by existing camera contracts, but the system shall not expose or implement multi-camera behavior merely because the database schema or earlier specifications were generalized for multiple cameras.

The following are out of scope for this baseline:

- camera grids;
- camera switching inside the normal operator panel;
- multiple concurrent camera feeds;
- multi-camera assignment;
- cross-camera tracking;
- camera groups;
- camera failover;
- camera discovery;
- multi-camera analytics.

## 2.2 No physical CCTV dependency

MVP completion does not depend on:

- access to a university CCTV system;
- RTSP credentials;
- ONVIF;
- NVR/DVR integration;
- IP-camera discovery;
- USB capture hardware;
- physical camera networking.

These may be documented as future adapters only.

## 2.3 Looping is required

A selected clip shall loop automatically at EOF while the feed remains active.

Expected state:

```text
START
  ↓
PLAYING
  ↓
EOF
  ↓
LOOP_RESTART
  ↓
PLAYING
  ↓
...
  ↓
STOP
```

EOF is not a camera failure.

A natural loop restart shall not be reported as `camera_offline`.

---

# 3. Product Separation

## 3.1 Demo Control Panel

The Demo Control Panel is a separate project/demo surface.

Its responsibilities are limited to source control and demo diagnostics:

- list approved demo clips;
- select one clip;
- start the virtual camera;
- stop the virtual camera;
- restart from the beginning;
- show source-controller status;
- optionally show developer diagnostics such as current loop count.

It shall not become the normal surveillance/operator interface.

## 3.2 Normal Sentinel Operator Panel

The normal operator panel shall behave as the operational CCTV interface.

It shall show the one logical camera and the AI/system state.

It shall **not** expose:

- a filesystem path;
- a raw filename picker;
- arbitrary upload controls;
- dataset terminology;
- training/test labels;
- XD-Violence workspace details.

The normal operator panel may display the logical source status:

```text
ONLINE
STARTING
STOPPED
ERROR
```

The fact that the physical origin is a local file is an adapter-level/demo-controller concern.

---

# 4. Terminology

| Term | Meaning |
|---|---|
| `Virtual CCTV Source` | Adapter that presents an approved recorded video as the single camera feed. |
| `Demo Control Panel` | Separate UI used to select/control the approved recorded source. |
| `Operator Panel` | Normal Sentinel monitoring UI; no file-selection controls. |
| `Demo clip` | Approved local media asset registered for system-integration demonstration. |
| `Loop` | Restart of the selected clip from the beginning after EOF while feed state remains active. |
| `Camera session` | Active lifecycle of the single virtual camera from start to stop. |
| `Source locator` | Opaque application identifier resolving server-side to an approved media path. |
| `Physical CCTV` | Actual network/USB/IP camera hardware; not required in the academic baseline. |

---

# 5. Functional Requirements

## FR-VCAM-001 — Single camera

The system shall expose exactly one operational camera in the academic baseline.

**Acceptance:** the normal UI does not provide a multi-camera selector/grid and the demo controller controls only the configured single camera.

## FR-VCAM-002 — Approved file source

The virtual camera shall use a clip from a server-side approved catalog.

**Acceptance:** the browser never submits an arbitrary absolute filesystem path.

## FR-VCAM-003 — Separate demo controller

The system shall provide a Demo Control Panel that is separate from the normal operator panel.

**Acceptance:** source selection exists only in the demo-control surface.

## FR-VCAM-004 — Start feed

Starting the feed shall activate the selected clip as the virtual camera source.

## FR-VCAM-005 — Stop feed

Stopping the feed shall stop frame production and AI processing for the camera session.

## FR-VCAM-006 — Loop at EOF

EOF shall restart the selected clip from the beginning automatically while the session remains active.

**Acceptance:** at least two complete passes of a short fixture can be observed without manual restart.

## FR-VCAM-007 — Real-time pacing

The replay adapter shall emit/advance source time at approximately the clip's natural media rate rather than presenting the entire file instantaneously as one offline batch.

Implementation may compensate for processing load, but the visible feed shall remain comprehensible as CCTV-like playback.

## FR-VCAM-008 — Shared source identity

The video shown to the operator and the video analyzed by the AI pipeline shall originate from the same selected `clip_id` and camera session.

## FR-VCAM-009 — Downstream source abstraction

AI/domain consumers shall not require special conditional behavior such as:

```text
if source_is_recorded:
    use_demo_detection_rules
```

The source adapter owns the file-specific behavior.

## FR-VCAM-010 — Loop is not camera failure

Natural EOF and automatic loop restart shall not create a camera-offline condition.

## FR-VCAM-011 — No arbitrary path exposure

Source selection shall use opaque IDs such as:

```text
fight-01
normal-01
scenario-03
```

Server-side configuration resolves those IDs to trusted local paths.

## FR-VCAM-012 — Model freeze preserved

The replay design shall not modify the frozen model identity, checkpoint, threshold, score semantics, temporal policy, or official evaluation split.

## FR-VCAM-013 — Explicit failure behavior

Unreadable/corrupt/unsupported media shall produce a source failure state rather than a successful negative AI result.

## FR-VCAM-014 — No multi-camera feature creep

No component shall introduce multiple simultaneous cameras without a future explicit scope decision.

---

# 6. Non-Functional Requirements

## NFR-VCAM-001 — Determinism

Given the same registered clip, model artifacts, and runtime policy, replay shall be reproducible enough for academic demonstration and debugging.

## NFR-VCAM-002 — Responsiveness

Long-running decoding/inference shall not block ordinary FastAPI interactive request handling.

## NFR-VCAM-003 — Path safety

No endpoint shall accept unrestricted absolute paths, path traversal, or client-controlled source-root changes.

## NFR-VCAM-004 — Honest claims

Documentation/presentation may state that the application uses a **virtual CCTV replay source**. It shall not claim that a physical live CCTV deployment was integrated when none was used.

## NFR-VCAM-005 — Repository hygiene

Demo videos, model checkpoints, extracted features, and machine-local path maps shall remain outside Git unless redistribution is explicitly permitted and project governance later approves inclusion.

## NFR-VCAM-006 — Observable lifecycle

The system shall expose enough status to distinguish:

```text
idle
starting
playing
loop-restarting
stopped
failed
```

---

# 7. Logical Architecture

```text
┌────────────────────────────────────┐
│ Separate Demo Control Panel        │
│                                    │
│ Clip list → Select → Start/Stop    │
└─────────────────┬──────────────────┘
                  │ clip_id/control
                  ▼
┌────────────────────────────────────┐
│ Virtual Camera Controller          │
│ exactly one camera session         │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Approved Clip Resolver             │
│ clip_id → trusted local path       │
└─────────────────┬──────────────────┘
                  │
                  ▼
┌────────────────────────────────────┐
│ Looping Replay Source Adapter      │
│ decode → pace → EOF → seek/reopen  │
└──────────────┬───────────────┬─────┘
               │               │
               │               │
               ▼               ▼
     Operator video path    AI processing path
               │               │
               │               ▼
               │       exact I3D + temporal model
               │               │
               └───────┬───────┘
                       ▼
                 FastAPI/domain
                       │
                       ▼
              Normal Sentinel UI
```

The implementation may optimize internal transport, but the logical ownership boundary shall remain.

---

# 8. Component Responsibilities

## 8.1 Demo Control Panel

Owns:

- displaying approved clip choices;
- issuing select/start/stop/restart actions;
- showing controller errors;
- demo-only diagnostics.

Does not own:

- violence scoring;
- model threshold;
- event semantics;
- camera-domain truth;
- filesystem traversal.

## 8.2 Approved Clip Resolver

Owns:

- parsing the registered manifest;
- resolving `clip_id`;
- ensuring resolved paths remain beneath the configured media root;
- rejecting missing or unregistered clips.

## 8.3 Replay Source Adapter

Owns:

- opening the selected media;
- extracting frame timing/FPS metadata;
- pacing replay;
- loop restart;
- maintaining source/session position;
- clean shutdown;
- surfacing decode errors.

## 8.4 AI Worker

Owns the existing AI responsibilities:

- qualified preprocessing;
- exact I3D feature extraction;
- frozen temporal violence scoring;
- explicit worker failures;
- structured model results.

The virtual-camera work shall not silently retrain or recalibrate the model.

## 8.5 Backend Domain

Owns:

- current single-camera state;
- model-result validation;
- rolling criterion;
- eventual event-domain policy;
- application APIs.

## 8.6 Operator Frontend

Owns:

- presenting the one camera feed;
- showing system/camera/AI states;
- presenting event/history views that are actually implemented.

It does not own source selection.

---

# 9. Camera and Loop State Model

Recommended logical state machine:

```text
IDLE
  │ select clip
  ▼
READY
  │ start
  ▼
STARTING
  │ first valid frame
  ▼
PLAYING
  │ EOF
  ▼
LOOP_RESTARTING
  │ seek/open success
  └──────────────► PLAYING

PLAYING ──stop──► STOPPED
PLAYING ──fatal decode error──► FAILED
LOOP_RESTARTING ──fatal reopen error──► FAILED
```

A loop restart may increment:

```text
loop_count = 1, 2, 3, ...
```

for diagnostics.

The camera remains logically online through a normal loop transition.

---

# 10. Timing Rules

The replay source shall use source timestamps/FPS where available.

Preferred pacing rule:

```text
target_wall_time(frame_n)
=
session_wall_start
+
source_pts(frame_n)
```

If source timestamps are unavailable, the adapter may use validated FPS metadata.

The system should avoid unconstrained `while read frame` playback that causes a 60-second clip to finish in a few seconds merely because decoding is faster than real time.

The exact tolerance is an implementation/test decision and shall be measured rather than invented.

---

# 11. Loop Semantics for AI

Looping creates repeated exposure to the same scene.

Therefore:

1. model scoring may naturally repeat on every loop;
2. the loop itself does not reset or change the frozen model;
3. rolling-state reset behavior at loop boundary must be explicit in implementation;
4. event deduplication/cooldown/episode grouping remains an event-domain concern.

Recommended target for the demonstration adapter:

- reset transient per-source temporal buffering cleanly at session start;
- preserve a valid continuous camera session across loop restart;
- do not treat EOF as worker failure;
- do not fabricate a negative window during restart.

Until automatic violence-event lifecycle policy is implemented, the demo may show the candidate fighting condition without claiming durable incident deduplication.

---

# 12. Demo Media Organization

Recommended machine-local layout:

```text
Sentinel-Demo-Media/
├── fight/
│   ├── fight_01.mp4
│   └── ...
├── non_violence/
│   ├── normal_01.mp4
│   └── ...
└── manifest.json
```

The folder is external to Git.

Recommended environment variable:

```text
SENTINEL_DEMO_MEDIA_ROOT=<absolute local path>
```

The path is machine-local configuration.

---

# 13. Demo Media Manifest

Example only:

```json
{
  "schema_version": "1",
  "clips": [
    {
      "clip_id": "scenario-01",
      "relative_path": "fight/fight_01.mp4",
      "display_name": "Scenario 01",
      "expected_class": "fighting",
      "sha256": "TBD_FROM_ACTUAL_FILE",
      "duration_ms": null,
      "provenance": "TBD",
      "permission_status": "TBD"
    }
  ]
}
```

Values marked `TBD` shall be replaced from actual files/evidence.

Do not fabricate hashes, durations, provenance, or redistribution permission.

For presentation, the Demo Control Panel may hide `expected_class` and show neutral names such as `Scenario 01`.

---

# 14. API Target

The following is the target demo-control contract. It is not to be described as implemented until code exists.

## 14.1 List clips

```http
GET /api/v1/demo/clips
```

Response concept:

```json
{
  "data": [
    {
      "clip_id": "scenario-01",
      "display_name": "Scenario 01"
    }
  ]
}
```

No absolute path is returned.

## 14.2 Select source

```http
PUT /api/v1/demo/source
Content-Type: application/json

{
  "clip_id": "scenario-01"
}
```

Selection while playing should either be rejected with a stable conflict response or perform an explicitly documented controlled restart. The initial implementation should prefer the simpler rule: **stop before changing source**.

## 14.3 Start

```http
POST /api/v1/demo/source/start
```

## 14.4 Stop

```http
POST /api/v1/demo/source/stop
```

## 14.5 Restart

```http
POST /api/v1/demo/source/restart
```

Restarts current clip at time zero without changing clip selection.

## 14.6 Status

```http
GET /api/v1/demo/source/status
```

Conceptual response:

```json
{
  "data": {
    "state": "playing",
    "clip_id": "scenario-01",
    "position_ms": 12450,
    "loop_count": 2
  }
}
```

The normal camera API should expose operational camera state without requiring the normal operator UI to call demo-controller endpoints.

---

# 15. Operator Video Delivery

The normal operator panel shall consume a normal camera-view abstraction.

The concrete browser transport may be selected during implementation according to simplicity and compatibility. Examples include:

- MJPEG endpoint;
- HLS;
- another browser-compatible local streaming mechanism.

The academic requirement is not tied to one transport.

Whichever transport is selected shall satisfy:

- one camera only;
- same selected source/session as the AI pipeline;
- looping at EOF;
- no file picker in operator UI;
- no arbitrary filesystem path disclosure.

---

# 16. Security Boundary

The browser shall never send:

```text
C:\Users\...
/home/user/...
..\..\...
```

as a source path.

Required flow:

```text
browser sends clip_id
        ↓
backend reads approved manifest
        ↓
backend resolves under SENTINEL_DEMO_MEDIA_ROOT
        ↓
canonical-path containment check
        ↓
open media
```

Reject:

- unknown IDs;
- absolute-path injection;
- traversal;
- symlink escape where applicable;
- unsupported extension/media;
- missing files.

The demo controller should be bound to local/development use unless authentication is later implemented.

---

# 17. Dataset and Provenance Rules

Demo fixtures are system-integration/demo data, not silently part of the formal model evaluation set.

Each final clip shall record:

- fixture ID;
- clip ID;
- original filename;
- local relative path;
- SHA-256;
- duration;
- codec/container if useful;
- provenance/source;
- permission/redistribution status;
- expected scenario;
- whether used in training/validation/test;
- whether safe to redistribute.

If a clip originates from a formal model dataset, its split membership must remain documented to avoid falsely presenting familiar evaluation material as evidence of field generalization.

---

# 18. Frozen Violence Runtime Compatibility

Current frozen identity remains:

```text
experiment_id:
EXP-VIO-TEMPORAL-001

model:
MODEL-VIO-BIGRU-ATTN-XD-V1

model_version_id:
6d22f83d-17f8-5ecf-9f0f-246fa326ec72

checkpoint_sha256:
1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772

threshold:
0.906

backend candidate criterion:
3 positives among latest 5 observations

stride:
1 feature step
```

The model output remains an uncalibrated sigmoid score for the fighting positive class, not a calibrated real-world probability.

The replay-camera integration is transport/orchestration work and shall not alter these frozen values.

---

# 19. Current Implementation Boundary at Decision Time

At the 2026-10-07 documentation decision point, the repository already has:

- FastAPI application/backend modules;
- SQLAlchemy/Alembic persistence foundation;
- camera metadata APIs;
- event list/detail APIs;
- a development violence-result HTTP adapter;
- separate AI worker code;
- controlled file-source runtime capability;
- source-locator mapping;
- frozen model validation;
- rolling 0.906 / 3-of-5 violence criterion;
- React/Vite operator frontend;
- current operator camera view placeholder rather than a completed video-stream connection.

The following virtual-camera items are **target work**, not yet to be claimed as complete unless later verification proves otherwise:

- looping real-time-paced replay adapter;
- singleton virtual-camera controller;
- demo source-control APIs;
- separate Demo Control Panel;
- normal operator video streaming from the virtual camera;
- source synchronization between displayed feed and AI processing;
- loop-specific tests.

### Current backend foundation update

The backend now contains an internal schema-version-1 manifest loader and path resolver at `backend/app/demo/clip_catalog.py`. It rejects absolute/traversal paths, verifies resolved clip paths remain beneath the configured media root, rejects missing files and duplicate IDs, and omits local paths from its public DTO helper. This helper is not wired to an API or replay source and does not validate decoding, provenance, or redistribution permission. It does not satisfy the virtual-camera acceptance tests by itself.

---

# 20. Team Ownership and Parallel Work

## Kasi — AI/runtime integration lead

Can proceed immediately:

- obtain/configure the external qualified XD-Violence workspace;
- verify raw-video preflight;
- validate fighting and non-violence fixtures;
- define/implement replay-source → AI worker integration;
- verify score/window behavior during repeated loops;
- ensure no model retuning.

## Gouri — backend/domain

Can proceed immediately:

- singleton virtual-camera controller;
- approved clip catalog/manifest loader;
- safe path resolution;
- start/stop/restart/status APIs;
- lifecycle/error handling;
- backend integration boundary to AI worker;
- operational camera status mapping.

## Aaditi — frontend

Can proceed immediately:

- separate Demo Control Panel;
- one-camera operator view;
- source-control loading/error states;
- normal camera video surface integration;
- AI state/result presentation using agreed contracts.

No team member needs to wait for physical CCTV access.

---

# 21. Implementation Sequence

Recommended sequence:

```text
1. Documentation baseline
2. Finalize demo fixture registry fields
3. AI raw-video preflight
4. Backend singleton virtual-camera controller
5. Replay source loop implementation
6. Demo API
7. Demo Control Panel
8. Normal operator video-view connection
9. AI integration with same selected source
10. Positive + negative + loop E2E tests
11. Integration verification
12. Promote staging → main
```

Work on steps 3, 4, and 7 can occur in parallel after the contract is stable.

---

# 22. Acceptance Test Set

Minimum required tests:

| Test | Expected |
|---|---|
| registered fighting clip starts | camera reaches playing state |
| registered non-violence clip starts | camera reaches playing state |
| clip reaches EOF | source loops automatically |
| two loops | feed remains online |
| stop during playback | frame production/inference stops cleanly |
| restart | current clip restarts from zero |
| unknown clip ID | rejected |
| traversal attempt | rejected |
| missing registered file | explicit source failure |
| corrupt media | explicit source failure; not “normal” AI result |
| fighting fixture | frozen model produces fighting-like observations and target candidate behavior |
| negative fixture | does not satisfy target fighting candidate behavior under documented test expectation |
| normal operator screen | contains no file picker |
| demo panel | contains source selector/control |
| one-camera scope | no multi-camera selector/grid |
| model identity | frozen IDs/hash/policy unchanged |

Formal pass/fail values for timing tolerance must be measured and then baselined; they shall not be invented here.

---

# 23. Demonstration Walkthrough

Recommended academic demo:

```text
1. Open normal Sentinel operator dashboard.
2. Open separate Demo Control Panel.
3. Select Scenario 01.
4. Start feed.
5. Show DEMO-CAM-01 becoming active in normal operator view.
6. Show footage playing as the camera feed.
7. Show AI results progressing while footage plays.
8. Allow clip to reach EOF and visibly loop.
9. Stop the feed.
10. Select another scenario.
11. Start again.
12. Demonstrate contrasting fighting/non-violence behavior.
```

The presentation should describe the source as:

> “a controlled looping virtual CCTV feed backed by prerecorded video because the academic environment does not provide access to a physical CCTV installation.”

Do not claim physical CCTV integration.

---

# 24. Explicit Non-Goals

The following are not required for this milestone:

- multi-camera support;
- physical CCTV hardware;
- RTSP integration;
- ONVIF;
- NVR/DVR;
- camera discovery;
- cloud video ingestion;
- cross-camera tracking;
- production surveillance deployment;
- model retraining;
- threshold retuning;
- new violence benchmark selection.

---

# 25. Future Scope

Possible future adapters:

```text
VideoSource
├── LoopingRecordedVideoSource   [current academic target]
├── RtspVideoSource              [future]
└── UsbCameraSource              [future]
```

A future adapter must not require changes to violence model semantics merely because the transport changes.

---

# 26. Definition of Done

The single-camera virtual CCTV milestone is complete only when:

- exactly one logical camera is presented;
- a separate Demo Control Panel can choose an approved clip;
- start/stop/restart work;
- EOF loops automatically;
- operator view displays the virtual camera;
- AI analyzes the same selected source;
- frozen model identity/policy remains unchanged;
- fighting/non-violence fixtures are demonstrated;
- unsafe path input is rejected;
- loop does not produce false camera-offline state;
- documentation reflects measured implementation status;
- automated tests cover the core lifecycle;
- integration verification passes.

Anything not demonstrated by code/tests remains documented as target work rather than completed work.

---

# 2026-10-08 Backend Controller/API Boundary Update

The backend branch now includes:

- local-only routes for approved clip listing, selection, start, stop, restart, and status;
- a process-local singleton controller with explicit states and callbacks for first frame, playback position, loop restart, and source failure;
- safe error envelopes and tests using a fake replay adapter.

The default application has no real replay adapter configured. Consequently, list/select/status and controller-boundary tests are available, but `POST .../start` returns `SOURCE_UNAVAILABLE` in the default app. No video is decoded or looped by this implementation. No operator video is delivered, no AI worker receives frames from the selected clip, and normal camera health remains `unknown` because a mapping from `DEMO-CAM-01` to a persisted camera UUID has not been specified/configured.

The implementation also records several lifecycle/API details as `PROPOSED` for team review in `docs/07-api-specification.md`; they are not new accepted product decisions. Real replay, playback pacing, EOF tests, camera-status mapping, and shared-source AI integration remain required before claiming the virtual-camera milestone complete.
