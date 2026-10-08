---
title: "Sentinel AI — Review-First Academic Violence Demo Scope"
document_id: "SEN-SCOPE-2026-10-08"
version: "1.0.0"
status: "PROJECT_LEAD_SCOPE_DECISION"
project: "Sentinel AI"
decision_date: "2026-10-08"
review_date: "2026-10-09"
status_of_code: "NOT_VERIFIED_BY_THIS_DOCUMENT"
---

# Sentinel AI — Review-First Academic Violence Demo Scope

## 1. Decision and authority

On 2026-10-08, the project lead narrowed the academic deliverable to a demonstrable **single-source virtual CCTV violence-detection and alert workflow**, to be prioritized for the review on 2026-10-09. Every implementation change made for the review must also contribute directly to the final academic deliverable; the review is not an excuse for throwaway code.

This scope decision supersedes the broader multi-feature MVP requirements **for the current academic deliverable only**. Older documents are retained for design history and model/evaluation provenance. They must not be used by agents to add unrelated features without a later explicit scope decision. In particular, a `MUST` in an older un-reconciled draft does not independently authorize adding an excluded feature.

This decision **does not** revoke the frozen violence-model qualification record, code quality requirements, nonfabrication principles, or the requirement to disclose unverified behavior.

## 2. Required observable workflow

```text
approved clip in a configured local media folder
  -> manifest registration by opaque clip_id
  -> single virtual CCTV controller
  -> paced video display in the normal operator interface
  -> actual qualified I3D extractor + frozen temporal violence model
  -> frozen candidate criterion / state
  -> visible operator-facing fighting alert when qualified
```

A recorded clip is presented as a *virtual CCTV feed*. Documentation and demonstrations must **never** claim that the source is a physically installed live CCTV camera.

### Required features

1. Exactly one canonical logical camera (`DEMO-CAM-01`), with its existing UUID identity preserved.
2. Approved clip catalog inside a machine-configured media root; a separate minimal source-control panel for selecting, starting, stopping, and restarting footage.
3. Automatic continuous looping at EOF with realistic pacing and without an erroneous offline state.
4. Actual browser-visible video of the same selected source/session that is analyzed by the worker.
5. Actual frozen violence/fighting inference with accurate model state, threshold semantics, and explicit worker failures.
6. Fighting-positive and fighting-negative clips with honest interpretation of model results.
7. A visible UI alert/state update derived from *actual* model qualification; a static banner, hard-coded score, fixture label, or mock API response is not acceptable proof.
8. Repeatable local startup and shutdown, minimal negative tests, and honest documentation of observed results.

### Alert contract for the current academic release

A **visible, non-durable live alert** is sufficient if it is clearly labeled as a live detection and is driven by the qualified backend/worker result. Durable acknowledgement, a generalized incident state machine, broad event search, complex evidence storage, and realtime WebSocket infrastructure are **not prerequisites**. Polling the existing local backend or using a narrowly scoped event stream is acceptable if state consistency and source/session freshness are handled correctly. Do not claim event persistence unless it is actually implemented and verified.

The previous backend currently distinguishes `candidate_condition=true` from `event_persisted=false`. Preserve that truthfulness; never rename a candidate as a saved incident without implementing the persistence boundary.

## 3. Explicitly not required for this release

- Login, user-account management, JWT/session infrastructure, RBAC, password reset, or formal authentication flows.
- Person detector, multi-object tracking, virtual zones, intrusion, loitering, crowd events, or comprehensive camera management beyond the one virtual source.
- Multi-camera grids, cross-camera analytics, RTSP, ONVIF, USB cameras, physical surveillance equipment.
- Evidence clips/snapshots, durable acknowledgement, audit log, historical search and analytics dashboards.
- WebSocket architecture solely for the sake of using WebSockets; use it only if it materially simplifies the required live alert.
- Cloud deployment, distributed systems, message brokers, Redis, Docker orchestration, mobile/PWA, SMS/email.
- New model training, checkpoint replacement, threshold search, or unofficial repeat evaluation of the held-out TEST split.
- Appearance-only UI redesign and feature scaffolding that does not support the required demonstration.

These omissions are a deliberate reduction of project scope, **not** evidence that the older requirements were implemented.

## 4. Minimal safeguards retained

The project runs on an academic/local workstation, with demo HTTP services bound to loopback by default. Use narrow, necessary controls only:

- Validate opaque clip identifiers against a server-controlled catalog. Resolve paths beneath a configured root and reject traversal, absolute browser-supplied paths, and escapes.
- Validate worker payloads, timestamps, camera/session identity, and model-version identity before showing results.
- Return explicit unavailable/degraded states rather than fabricating negative predictions or hiding failures.
- Do not commit secrets, private footage, large restricted datasets, or unlicensed artifacts.
- Avoid gratuitous internet/network exposure; protect a local-only controller from external access.

These are correctness/reliability boundaries, not a mandate to build a generalized enterprise security subsystem.

## 5. Machine-independent configuration (no hardcoded developer paths)

Honor the existing configuration keys where applicable:

- `SENTINEL_DEMO_MEDIA_ROOT`: absolute, machine-configured path to approved media and manifest.
- `SENTINEL_VIOLENCE_ROOT`: absolute, machine-configured path to the qualified external XD-Violence workspace.
- `SENTINEL_FFMPEG_BINARY`: optional executable path, otherwise discover on `PATH`.
- `SENTINEL_TEMPORAL_CHECKPOINT`, `SENTINEL_TEMPORAL_TRAIN_SCRIPT`, `SENTINEL_EXTRACTOR_PYTHON`, `SENTINEL_EXTRACTOR_WORKER`, `SENTINEL_RUNTIME_WORK_DIR`: existing qualified-artifact path overrides.
- `VITE_API_PROXY_TARGET`: frontend development API proxy configuration.

No source code, tracked JSON, documentation command, or startup script may require another contributor's `C:\\Users\\...`, personal workspace directory, or other hardcoded home path. Documentation may show symbolic placeholders but must not treat them as defaults. Use repository-relative paths for tracked code and environment-supplied paths for external media/models. The existing frozen checkpoint hash and model criterion must remain unchanged.

## 6. Frozen model invariant

Existing qualified record: `docs/19-violence-model-and-runtime-qualification.md`.

- Experiment: `EXP-VIO-TEMPORAL-001`.
- Model label: `MODEL-VIO-BIGRU-ATTN-XD-V1`.
- Model version ID: `6d22f83d-17f8-5ecf-9f0f-246fa326ec72`.
- Checkpoint SHA-256: `1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772`.
- Frozen live policy: threshold `0.906`, positive when at least 3 of the most recent 5 observations qualify, stride 1 feature step.

The sigmoid score is an uncalibrated model output; it is **not** a universal probability of real-world violence. Preserve the exact qualified extractor and downstream policy. If the artifacts cannot be located, report a blocker rather than substituting a synthetic worker or retraining the model.

## 7. Sequencing: first usable review milestone, then final completion

**R0 — Repository/docs baseline**: PRs and `staging` consolidated safely into `main`; this decision and the branch audit committed and visible; no hidden paths.

**R1 — Presentable source**: actual approved clip plays visibly in browser, can be stopped/restarted, and loops at least twice; loading/error states truthful.

**R2 — Presentable AI**: qualified runtime preflight passes on the selected machine, same source/session is processed by the real worker, and model observations are visible.

**R3 — Presentable alert**: positive fixture produces a qualified UI alert, negative fixture produces contrast, and stale results from a previous source/session cannot be shown as current.

**R4 — Final academic release**: negative/failure tests, clean setup, recorded test evidence, documentation, and reproducible walkthrough.

Prioritize R0–R3 for 2026-10-09. Do not postpone integration in order to implement excluded features.

## 8. Acceptance and evidence rule

Only mark a milestone `PASS` when the real integrated system has been observed and evidence retained. An isolated mock test is `COMPONENT_PASS`, not `END_TO_END_PASS`. Do not claim a live inference demo if only the model's earlier experimental metrics are available. Keep feature status as `NOT_VERIFIED`, `BLOCKED`, or `NOT_IMPLEMENTED` until proven otherwise.

## 9. Impact on earlier documents

Treat the older broad-scope sections of `docs/PROJECT_HANDBOOK.md`, `docs/01-vision-and-scope.md`, `docs/02-srs.md`, `docs/03-use-case-specification.md`, `docs/12-ui-ux-specification.md`, `docs/14-test-plan.md`, `docs/15-requirements-traceability.md`, `docs/16-deployment-guide.md`, `docs/17-operator-manual.md`, and `docs/18-final-technical-report.md` as historical planning for non-demo features unless explicitly reaffirmed here. `docs/21-virtual-cctv-replay-integration.md` remains authoritative for single-source replay mechanics where consistent with this decision. `docs/19-violence-model-and-runtime-qualification.md` remains authoritative for the frozen AI evidence and is not changed by this scope decision.

This is a change-control addendum, not a false claim that every older draft requirement has been implemented.
