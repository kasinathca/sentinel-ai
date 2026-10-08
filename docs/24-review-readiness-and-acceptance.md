---
title: "Sentinel AI — Review-First Acceptance Register"
document_id: "SEN-REVIEW-ACPT-2026-10-08"
status: "PLANNED_NOT_EXECUTED"
recorded_at: "2026-10-08"
review_date: "2026-10-09"
---

# Review-First Acceptance Register

**Critical rule:** Every item below starts `NOT_VERIFIED`. This document is a checklist for evidence collection, not a record of passed tests.

| ID | Review-first test | Minimum observable evidence | Current status |
|---|---|---|---|
| R0-01 | `staging` verified and promoted without rewriting history | exact refs, test log, safe merge commit | NOT_VERIFIED |
| R0-02 | frozen model/artifact preflight | paths from environment, checksum, qualified runtime output | NOT_VERIFIED |
| R1-01 | positive clip selected by `clip_id` | registered manifest, source state and visible video | NOT_VERIFIED |
| R1-02 | clip loops twice | real FFmpeg/video timing, loop count, no false offline | NOT_VERIFIED |
| R1-03 | stop/restart | visible stream stops, restarts; no stray processes | NOT_VERIFIED |
| R2-01 | actual model processes currently displayed source | matching `camera_id`, `source_session_id`, timestamps and model identity | NOT_VERIFIED |
| R2-02 | negative fixture processed | actual model output; no hardcoded labels or score | NOT_VERIFIED |
| R3-01 | fighting condition drives visible alert | backend qualification plus UI evidence tied to current source/session | NOT_VERIFIED |
| R3-02 | stop/source change invalidates stale results | no previous-session alert attributed to current session | NOT_VERIFIED |
| R4-01 | corrupt/missing clip fails visibly | error state rather than normal score | NOT_VERIFIED |
| R4-02 | worker unavailable fails visibly | clear failure rather than fabricated no-fighting | NOT_VERIFIED |
| R4-03 | install/setup repeatable | clean runbook evidence; external assets still configurable | NOT_VERIFIED |

## Honest review fallback hierarchy

- **Target:** Actual browser playback + actual model result + actual visible fighting alert.
- **If AI artifacts are missing:** demonstrate only verified camera/video capabilities, clearly identify live AI inference as blocked, and present *historical* model qualification results as historical. Do not show canned inference as if live.
- **If video playback is unavailable:** demonstrate only tested APIs/controllers and identify real video delivery as blocked. Never claim the end-to-end flow works.

## Minimal demo operating sequence

1. Initialize the existing database/seed and start FastAPI and React using the repository runbook.
2. Register two approved local clips in `SENTINEL_DEMO_MEDIA_ROOT/manifest.json` (one fighting-like, one non-fighting), keeping clips outside Git.
3. Open the separate Demo Control Panel and the normal operator view.
4. Select a clip, start the virtual camera, and verify the browser is showing it through the backend stream.
5. Show the true worker state, model identity, candidate result, and alert (if actual integration is ready).
6. Let the clip loop and show that it remains online.
7. Stop and repeat with the contrasting fixture.
8. Explain limitations with measured evidence, not speculative claims.

## No hardcoded path and no unnecessary implementation rule

All paths to fixtures, FFmpeg, Python environments, model artifacts, checkpoint, and workspace must be determined by repository location, `PATH`, approved environment variables, or runtime discovery. No authored default may be a developer's home directory. Do not introduce login/role management, a tracking model, multiple cameras, cloud infrastructure, a large analytics dashboard, or any other unrelated capability as part of this review milestone.
