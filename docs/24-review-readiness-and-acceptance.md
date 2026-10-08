---
title: "Sentinel AI — Review-First Acceptance Register"
document_id: "SEN-REVIEW-ACPT-2026-10-08"
status: "EXECUTED"
recorded_at: "2026-10-08"
review_date: "2026-10-09"
---

# Review-First Acceptance Register

Evidence below was executed on 2026-10-08 against the implementation branch based on `1cfbed950547d48d8a804347cf8e94d5114bc5e0`. `PASS` means the stated real/component evidence was observed; unexecuted cases remain explicit.

| ID | Review-first test | Minimum observable evidence | Current status |
|---|---|---|---|
| R0-01 | `main`/`staging` synchronized before branch work | all three refs at `1cfbed9`; clean dedicated branch | PASS |
| R0-02 | frozen model/artifact preflight | checkpoint/training SHA matched; extractor/model `ready` | PASS |
| R1-01 | positive clip selected by `clip_id` | folder catalog, API state, Chrome-visible fighting video | PASS |
| R1-02 | clip loops twice | real FFmpeg loop counter reached four; no offline transition | PASS |
| R1-03 | stop/restart | browser stop; real restart retained the same session; no surviving worker process | PASS |
| R2-01 | actual model processes displayed source | canonical camera and matching source-session/correlation ID | PASS |
| R2-02 | negative fixture processed | 26 genuine windows, zero qualified state/event | PASS |
| R3-01 | fighting condition drives visible alert | 19 genuine windows, persisted event, red Chrome alert | PASS |
| R3-02 | stale session invalidated | session-key tests, canonical 409 guard, stop cleanup | PASS |
| R4-01 | corrupt/missing clip fails visibly | real corrupt-file injection showed source `FAILED` and the ffprobe error in Chrome | PASS |
| R4-02 | worker unavailable fails visibly | normal video remained visible while Chrome showed the worker-start failure | PASS |
| R4-03 | install/setup repeatable | portable environment/runbook and full integration gate | PASS |

## Exact observed evidence

```text
database migration/readiness = PASS
backend unittest             = 88/88 PASS
AI-worker unittest           = 19/19 PASS
frontend lint/build          = PASS
npm audit                    = 0 vulnerabilities
checkpoint SHA-256           = 1fa01d1be82ab3c63d33b4d5f1d5ef4ab2a176d1d2842afc842955ff72896772 PASS
training script SHA-256      = 630c913060c7800c96214438e8e36064b946679aa83aad4b8fd4943b6717690c PASS
normal fixture               = 26 windows; no event PASS
fighting fixture             = 19 windows; one event; browser alert PASS
natural replay               = 4 completed loops; source remained playing PASS
restart                      = same source-session UUID; playback and AI restarted PASS
corrupt media                = source failed; ffprobe error visible in browser PASS
worker unavailable           = video playing; AI failure visible in browser PASS
```

The UI and worker use one catalog-resolved clip and the same active session UUID. Filesystem paths appear only in machine-local configuration/runtime memory and were not exposed through browser APIs or committed.

## Honest review fallback hierarchy

- **Target:** Actual browser playback + actual model result + actual visible fighting alert.
- **If AI artifacts are missing:** demonstrate only verified camera/video capabilities, clearly identify live AI inference as blocked, and present *historical* model qualification results as historical. Do not show canned inference as if live.
- **If video playback is unavailable:** demonstrate only tested APIs/controllers and identify real video delivery as blocked. Never claim the end-to-end flow works.

## Minimal demo operating sequence

1. Initialize the existing database/seed and start FastAPI and React using the repository runbook.
2. Place approved local clips directly in `SENTINEL_DEMO_MEDIA_ROOT` (one fighting-like, one non-fighting), keeping clips outside Git. No manifest is used.
3. Open the separate Demo Control Panel and the normal operator view.
4. Select a clip, start the virtual camera, and verify the browser is showing it through the backend stream.
5. Show the true worker state, model identity, candidate result, and alert (if actual integration is ready).
6. Let the clip loop and show that it remains online.
7. Stop and repeat with the contrasting fixture.
8. Explain limitations with measured evidence, not speculative claims.

## 2026-10-09 dynamic-ingest continuation evidence

The controlled top-level media directory is now the only catalog authority.
The browser receives deterministic opaque clip IDs, state, normalization mode,
and safe media metadata; it never receives a filesystem path. Stable inputs
are inspected with FFprobe and noncanonical inputs are atomically normalized
under `.sentinel` before they become selectable.

Real Chrome acceptance used `launch_sentinel_demo.cmd`, the qualified external
XD-Violence workspace, and the frozen model. A noncanonical 340×256, 28-FPS MOV
source outside the media root was copied as `sir_live_test.mov` while the
application was running. Refresh Videos showed waiting/preparing and then
ready without a manifest edit, backend restart, database edit, or manual
FFmpeg command. The resulting public metadata was 1280×720, H.264, yuv420p,
30 FPS, constant frame rate. Replay and the AI source map resolved the same
`.sentinel/processed/demo-1b22db93f2f45658897ac058d6978cff.mp4` asset.

The three identical external source bytes copied as `fight_video.mp4`,
`normal_video.mp4`, and `banana_123.mov` produced identical canonical SHA-256
`2b982044e472440515cdf68f29c05f7abd5c1aca5eeec232a6deac5542e32d53`.
`sir_live_test.mov` and `fight_video.mp4` also produced the same first-pass
score sequence and final score `0.40805870294570923`; filename text had no
effect on inference.

Executed browser sessions produced one event each for FIGHT 1, FIGHT 2, and
FIGHT 3. FIGHT 1 and FIGHT 2 first qualified across natural replay passes and
later showed a truthful nonqualifying current 2/5 window while the session
detection and original event ID remained latched. NOR-FIGHT 1, NOR-FIGHT 2,
NORMAL, NORMAL 2, NORMAL 3, and NORMAL 4 produced no event; repeated looping
alone did not create one. Returning to Dashboard showed the current session's
event without a browser reload and kept historical events separate.

Ctrl+C during a real 69-second normalization removed both listeners and left
zero `.partial.mp4` files. Immediate relaunch recovered the input as a valid
canonical derivative, with no address conflict or stale source session.

Final automated evidence: disposable migration/readiness PASS; backend
96/96 PASS; AI-worker 19/19 PASS; frontend view-model 5/5 PASS; lint PASS;
production build PASS; npm audit 0 vulnerabilities; frozen runtime preflight
ready for model version `6d22f83d-17f8-5ecf-9f0f-246fa326ec72`.

## No hardcoded path and no unnecessary implementation rule

All paths to fixtures, FFmpeg, Python environments, model artifacts, checkpoint, and workspace must be determined by repository location, `PATH`, approved environment variables, or runtime discovery. No authored default may be a developer's home directory. Do not introduce login/role management, a tracking model, multiple cameras, cloud infrastructure, a large analytics dashboard, or any other unrelated capability as part of this review milestone.
