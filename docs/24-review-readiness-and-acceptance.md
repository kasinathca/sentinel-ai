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
| R1-01 | positive clip selected by `clip_id` | manifest, API state, Chrome-visible Fighting video | PASS |
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
2. Register two approved local clips in `SENTINEL_DEMO_MEDIA_ROOT/manifest.json` (one fighting-like, one non-fighting), keeping clips outside Git.
3. Open the separate Demo Control Panel and the normal operator view.
4. Select a clip, start the virtual camera, and verify the browser is showing it through the backend stream.
5. Show the true worker state, model identity, candidate result, and alert (if actual integration is ready).
6. Let the clip loop and show that it remains online.
7. Stop and repeat with the contrasting fixture.
8. Explain limitations with measured evidence, not speculative claims.

## No hardcoded path and no unnecessary implementation rule

All paths to fixtures, FFmpeg, Python environments, model artifacts, checkpoint, and workspace must be determined by repository location, `PATH`, approved environment variables, or runtime discovery. No authored default may be a developer's home directory. Do not introduce login/role management, a tracking model, multiple cameras, cloud infrastructure, a large analytics dashboard, or any other unrelated capability as part of this review milestone.
